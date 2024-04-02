from __future__ import annotations

import csv
import logging
import random
import statistics
from datetime import timedelta, datetime, date
from typing import Callable, Awaitable, Optional, NamedTuple

import aiohttp
from aiohttp import ClientSession
from homeassistant.core import HomeAssistant, callback, HassJob, HassJobType
from homeassistant.helpers import event
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import utcnow

from .const import DOMAIN, DEFAULT_TIMEOUT, CET
from .model import OMIEModel

_LOGGER = logging.getLogger(__name__)
_HOURS = list(range(25))
"""Max number of hours in a day (on the day that DST ends)."""

_SCHEDULE_MAX_DELAY = timedelta(seconds=3)
"""The maximum delay after the scheduled time that we will fetch from OMIE to avoid thundering herd."""

ADJUSTMENT_END_DATE = date(2024, 1, 1)
"""The date on which the adjustment mechanism is no longer applicable."""

# language=Markdown
#
# OMIE market sessions and the values that they influence. Time shown below is publication time in the CET timezone plus 10 minutes.
#
# ```
# | Time  | Name        | Spot | Adj  | Spot+1 | Ajd+1 |
# |-------|-------------|------|------|--------|-------|
# | 02:30 | Intraday 4  |  X   |  X   |        |       |
# | 05:30 | Intraday 5  |  X   |  X   |        |       |
# | 10:30 | Intraday 6  |  X   |  X   |        |       |
# | 13:30 | Day-ahead   |      |      |   X    |   X   |
# | 16:30 | Intraday 1  |      |      |   X    |   X   |
# | 18:30 | Intraday 2  |  X   |  X   |   X    |   X   |
# | 22:30 | Intraday 3  |      |      |   X    |   X   |
# ```
#
# References:
# - https://www.omie.es/en/mercado-de-electricidad
# - https://www.omie.es/sites/default/files/inline-files/intraday_and_continuous_markets.pdf

DateFactory = Callable[[], date]
"""Used by the coordinator to work out the market date to fetch."""

UpdateMethod = Callable[[], Awaitable[OMIEModel]]
"""Method that updates this coordinator's data."""


class OMIEDailyCoordinator(DataUpdateCoordinator[OMIEModel]):
    """Coordinator that fetches new data once per day at the specified time, optionally refreshing it throughout the day."""

    def __init__(self,
                 hass: HomeAssistant,
                 name: str,
                 market_updater: Callable[[ClientSession, DateFactory], UpdateMethod],
                 market_date: Callable[[], date],
                 none_before: str | None = None,
                 update_interval: timedelta | None = None) -> None:
        super().__init__(hass, _LOGGER, name=f'{DOMAIN}.{name}', update_interval=update_interval,
                         update_method=market_updater(async_get_clientsession(hass), market_date))
        self._market_date = market_date
        self._none_before = list(map(int, none_before.split(":"))) if none_before is not None else [0, 0]
        delay_μs = random.randint(0, _SCHEDULE_MAX_DELAY.seconds * 10 ** 6)
        self._schedule_second = delay_μs // 10 ** 6
        self._schedule_microsecond = delay_μs % 10 ** 6
        self.__job = HassJob(
            self._handle_refresh_interval,
            f'OMIEDailyCoordinator {name}',
            job_type=HassJobType.Coroutinefunction)

    async def _async_update_data(self) -> OMIEModel | None:
        if self._wait_for_none_before():
            # no results can possibly be available at this time of day
            _LOGGER.debug("%s: _async_update_data returning None before %s CET", self.name, self._none_before)
            return None

        if self._data_is_fresh():
            # current data is still fresh, don't update:
            _LOGGER.debug("%s: _async_update_data returning cached (market_date=%s, updated_at=%s, update_interval=%s)", self.name,
                          self.data.market_date, self.data.updated_at, self.update_interval)
            return self.data

        else:
            _LOGGER.debug("%s: _async_update_data refreshing data", self.name)
            return await super()._async_update_data()

    @callback
    def _schedule_refresh(self) -> None:
        """Schedule a refresh."""
        if self.config_entry and self.config_entry.pref_disable_polling:
            return

        if self._unsub_refresh:
            self._unsub_refresh()
            self._unsub_refresh = None

        self._omie_schedule_refresh()

    def _omie_schedule_refresh(self):
        cet_hour, cet_minute = self._none_before
        now_cet = utcnow().astimezone(CET)
        none_before = now_cet.replace(hour=cet_hour, minute=cet_minute, second=self._schedule_second,
                                      microsecond=self._schedule_microsecond)
        next_hour = now_cet.replace(minute=0, second=self._schedule_second, microsecond=self._schedule_microsecond) + timedelta(hours=1)

        # next hour or the none_before time, whichever is soonest
        next_refresh = (none_before if cet_hour == now_cet.hour and none_before > now_cet else next_hour).astimezone()

        _LOGGER.debug("%s: _schedule_refresh scheduling an update at %s (none_before=%s, next_hour=%s)", self.name,
                      next_refresh,
                      none_before, next_hour)
        self._unsub_refresh = event.async_track_point_in_utc_time(self.hass, self.__job, next_refresh)

    def _wait_for_none_before(self) -> bool:
        """Whether the coordinator should wait for `none_before`."""
        cet_now = utcnow().astimezone(tz=CET)
        cet_hour, cet_minute = self._none_before
        none_before = cet_now.replace(
            hour=cet_hour,
            minute=cet_minute,
            second=self._schedule_second,
            microsecond=self._schedule_microsecond)

        return cet_now < none_before and none_before.date() == cet_now.date()

    def _data_is_fresh(self) -> bool:
        return self.data is not None and self.data.market_date == self._market_date() and (
                self.update_interval is None or utcnow() < (self.data.updated_at + self.update_interval))


async def fetch_to_dict(session: aiohttp.ClientSession, source: str, market_date: date, short_names: dict[str, str]) -> Optional[OMIEModel]:
    async with await session.get(source, timeout=DEFAULT_TIMEOUT.total_seconds()) as resp:
        if resp.status == 404:
            return None

        lines = (await resp.text(encoding='iso-8859-1')).splitlines()
        header = lines[0]
        csv_data = lines[2:]

        reader = csv.reader(csv_data, delimiter=';', skipinitialspace=True)
        rows = [row for row in reader]
        hourly_values = {row[0]: [_to_float(row[h + 1]) for h in _HOURS if len(row) > h + 1 and row[h + 1] != ''] for row in rows}

        file_data = {
            'header': header,
            'fetched': utcnow().isoformat(),
            'market_date': market_date.isoformat(),
            'source': source,
        }

        for k in hourly_values:
            hourly = hourly_values[k]
            if k in short_names:
                # hourly & daily avg/sum
                key = short_names[k]

                suffix, daily = ['average', round(statistics.mean(hourly), 2)] if "(EUR/MWh)" in k else ['total', round(sum(hourly), 1)]
                file_data.update({
                    f'{key}_day_{suffix}': daily,
                    f'{key}_hourly': hourly,
                })
            else:
                # unknown rows, do not process
                file_data.update({k: hourly})

        return OMIEModel(
            updated_at=utcnow(),
            market_date=market_date,
            contents=file_data
        )


class DateComponents(NamedTuple):
    """A Date formatted for use in OMIE data file names."""
    date: date
    yy: str
    MM: str
    dd: str
    dd_MM_yy: str

    @staticmethod
    def decompose(a_date: datetime.date) -> DateComponents:
        year = a_date.year
        month = str.zfill(str(a_date.month), 2)
        day = str.zfill(str(a_date.day), 2)
        return DateComponents(date=a_date, yy=year, MM=month, dd=day, dd_MM_yy=f'{day}_{month}_{year}')


def spot_price(client_session: ClientSession, get_market_date: DateFactory) -> UpdateMethod:
    async def fetch() -> OMIEModel:
        dc = DateComponents.decompose(get_market_date())
        source = f'https://www.omie.es/sites/default/files/dados/AGNO_{dc.yy}/MES_{dc.MM}/TXT/INT_PBC_EV_H_1_{dc.dd_MM_yy}_{dc.dd_MM_yy}.TXT'

        return await fetch_to_dict(client_session, source, dc.date, {
            "Energía total con bilaterales del mercado Ibérico (MWh)": 'energy_with_bilaterals_es_pt',
            "Energía total de compra sistema español (MWh)": 'energy_purchases_es',
            "Energía total de compra sistema portugués (MWh)": 'energy_purchases_pt',
            "Energía total de venta sistema español (MWh)": 'energy_sales_es',
            "Energía total de venta sistema portugués (MWh)": 'energy_sales_pt',
            "Energía total del mercado Ibérico (MWh)": 'energy_es_pt',
            "Exportación de España a Portugal (MWh)": 'energy_export_es_to_pt',
            "Importación de España desde Portugal (MWh)": 'energy_import_es_from_pt',
            "Precio marginal en el sistema español (EUR/MWh)": 'spot_price_es',
            "Precio marginal en el sistema portugués (EUR/MWh)": 'spot_price_pt',
        })

    return fetch


def adjustment_price(client_session: ClientSession, get_market_date: DateFactory) -> UpdateMethod:
    async def fetch():
        market_date = get_market_date()
        if market_date < ADJUSTMENT_END_DATE:
            dc = DateComponents.decompose(market_date)
            source = f'https://www.omie.es/sites/default/files/dados/AGNO_{dc.yy}/MES_{dc.MM}/TXT/INT_MAJ_EV_H_{dc.dd_MM_yy}_{dc.dd_MM_yy}.TXT'

            return await fetch_to_dict(client_session, source, market_date, {
                "Precio de ajuste en el sistema español (EUR/MWh)": 'adjustment_price_es',
                "Precio de ajuste en el sistema portugués (EUR/MWh)": 'adjustment_price_pt',
                "Energía horaria sujeta al MAJ a los consumidores MIBEL (MWh)": 'adjustment_energy',
                "Energía horaria sujeta al mecanismo de ajuste a los consumidores MIBEL (MWh)": 'adjustment_energy',
                "Cuantía unitaria del ajuste (EUR/MWh)": 'adjustment_unit_price',
            })

        else:
            # adjustment mechanism ended in 2023
            return None

    return fetch


def _to_float(n: str) -> float | None:
    return n if n is None else float(n.replace(',', '.'))
