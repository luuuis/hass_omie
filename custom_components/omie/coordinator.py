from __future__ import annotations

import logging
import random
from datetime import timedelta, date
from typing import Callable, Awaitable, TypeVar

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant, callback, HassJob, HassJobType
from homeassistant.helpers import event
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import utcnow
from pyomie.main import spot_price as pyomie_spot
from pyomie.model import OMIEResults, SpotData

from .const import DOMAIN, CET

_LOGGER = logging.getLogger(__name__)
_HOURS = list(range(25))
"""Max number of hours in a day (on the day that DST ends)."""

_SCHEDULE_MAX_DELAY = timedelta(seconds=3)
"""The maximum delay after the scheduled time that we will fetch from OMIE to avoid thundering herd."""

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

_DataT = TypeVar("_DataT")

DateFactory = Callable[[], date]
"""Used by the coordinator to work out the market date to fetch."""

UpdateMethod = Callable[[], Awaitable[OMIEResults[_DataT] | None]]
"""Method that updates this coordinator's data."""


class OMIEDailyCoordinator(DataUpdateCoordinator[OMIEResults[_DataT] | None]):
    """Coordinator that fetches new data once per day at the specified time, optionally refreshing it throughout the day."""

    def __init__(self,
                 hass: HomeAssistant,
                 name: str,
                 market_updater: Callable[[ClientSession, DateFactory], UpdateMethod[_DataT]],
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

    async def _async_update_data(self) -> OMIEResults[_DataT] | None:
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


def spot_price(client_session: ClientSession, get_market_date: DateFactory) -> UpdateMethod[SpotData]:
    async def fetch() -> OMIEResults[SpotData] | None:
        return await pyomie_spot(client_session, get_market_date())

    return fetch
