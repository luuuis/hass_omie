from __future__ import annotations

import logging
from datetime import date, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (DOMAIN, DEFAULT_UPDATE_INTERVAL, DEFAULT_TIMEOUT)
from .coordinator import spot_price, adjustment_price, OMIEDailyCoordinator
from .model import OMIECoordinators

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    today = date.today
    tomorrow = lambda: today() + timedelta(days=1)

    hass.data[DOMAIN] = OMIECoordinators(
        spot=OMIEDailyCoordinator(hass,
                                  "spot",
                                  market_updater=spot_price,
                                  market_date=today),

        spot_next=OMIEDailyCoordinator(hass,
                                       "spot_next",
                                       market_updater=spot_price,
                                       market_date=tomorrow,
                                       none_before="13:30"),

        adjustment=OMIEDailyCoordinator(hass,
                                        "adjustment",
                                        market_updater=adjustment_price,
                                        market_date=today,
                                        update_interval=timedelta(hours=1)),

        adjustment_next=OMIEDailyCoordinator(hass,
                                             "adjustment_next",
                                             market_updater=adjustment_price,
                                             market_date=tomorrow,
                                             update_interval=timedelta(hours=1),
                                             none_before="13:30"),
    )

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data.pop(DOMAIN)
    hass.async_create_task(hass.config_entries.async_forward_entry_unload(entry, "sensor"))
    return True
