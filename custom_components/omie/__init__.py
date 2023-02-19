from __future__ import annotations

import csv
import logging
import statistics
from datetime import datetime, date, timedelta
from typing import Any, Awaitable, NamedTuple, Callable

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import (DOMAIN, DEFAULT_UPDATE_INTERVAL, DEFAULT_TIMEOUT)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data[DOMAIN] = DataUpdateCoordinator[OMIEData](
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_omie(async_get_clientsession(hass)),
        update_interval=DEFAULT_UPDATE_INTERVAL,
    )

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data.pop(DOMAIN)
    hass.async_create_task(hass.config_entries.async_forward_entry_unload(entry, "sensor"))
    return True


class OMIEPrices(NamedTuple):
    spot: dict[str, Any]
    adjustment: dict[str, Any]


class OMIEData(NamedTuple):
    today: OMIEPrices
    tomorrow: OMIEPrices


def async_update_omie(session: aiohttp.ClientSession) -> Callable[[], Awaitable[OMIEData]]:
    # cached value to avoid unnecessary network calls
    last_value: tuple[datetime, OMIEData] | None = None

    async def fetch_prices(fetch_date: date) -> OMIEPrices:
        return OMIEPrices(
            spot=await spot_price(session, fetch_date),
            adjustment=await adjustment_price(session, fetch_date)
        )

    async def do_update() -> OMIEData:
        nonlocal last_value
        # if last_value is not None:
        #     pass

        now_date = date.today()
        omie_data = OMIEData(
            today=await fetch_prices(now_date),
            tomorrow=await fetch_prices(now_date + timedelta(days=1)),
        )

        last_value = (datetime.now(), omie_data)
        return omie_data

    return do_update


async def fetch_to_dict(session: aiohttp.ClientSession, source, fetch_date, short_names):
    async with await session.get(source, timeout=DEFAULT_TIMEOUT.total_seconds()) as resp:
        if resp.status is 404:
            return None

        lines = (await resp.text(encoding='iso-8859-1')).splitlines()
        header = lines[0]
        data = lines[2:]

        reader = csv.reader(data, delimiter=';', skipinitialspace=True)
        rows = {row[0]: [float(row[i + 1].replace(',', '.')) for i in list(range(24))] for row in reader if row[0] != ''}

        file_data = {
            'header': header,
            'fetched': datetime.now().isoformat(),
            'market_date': fetch_date.isoformat(),
            'source': source,
        }

        for k in rows:
            hourly = rows[k]
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

        return file_data


def explode(fetch_date: datetime.date):
    yy = fetch_date.year
    MM = str.zfill(str(fetch_date.month), 2)
    dd = str.zfill(str(fetch_date.day), 2)
    return yy, MM, dd, f'{dd}_{MM}_{yy}'


async def spot_price(client_session, fetch_date) -> dict[str, float]:
    yy, MM, dd, dd_MM_yy = explode(fetch_date)
    source = f'https://www.omie.es/sites/default/files/dados/AGNO_{yy}/MES_{MM}/TXT/INT_PBC_EV_H_1_{dd_MM_yy}_{dd_MM_yy}.TXT'

    return await fetch_to_dict(client_session, source, fetch_date, {
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


async def adjustment_price(client_session, fetch_date) -> dict[str, float]:
    yy, MM, dd, dd_MM_yy = explode(fetch_date)
    source = f'https://www.omie.es/sites/default/files/dados/AGNO_{yy}/MES_{MM}/TXT/INT_MAJ_EV_H_{dd_MM_yy}_{dd_MM_yy}.TXT'

    return await fetch_to_dict(client_session, source, fetch_date, {
        "Precio de ajuste en el sistema español (EUR/MWh)": 'adjustment_price_es',
        "Precio de ajuste en el sistema portugués (EUR/MWh)": 'adjustment_price_pt',
        "Energía horaria sujeta al MAJ a los consumidores MIBEL (MWh)": 'adjustment_energy',
        "Energía horaria sujeta al mecanismo de ajuste a los consumidores MIBEL (MWh)": 'adjustment_energy',
        "Cuantía unitaria del ajuste (EUR/MWh)": 'adjustment_unit_price',
    })
