from __future__ import annotations

import logging
from datetime import datetime, date, timedelta
from typing import Any, Awaitable, NamedTuple, Callable

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (DOMAIN, DEFAULT_UPDATE_INTERVAL, DEFAULT_TIMEOUT)
from .coordinator import spot_price, adjustment_price

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
    spot: dict[str, Any] | None
    adjustment: dict[str, Any] | None


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
