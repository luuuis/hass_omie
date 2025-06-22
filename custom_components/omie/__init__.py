from __future__ import annotations

__version__ = "1.0.11-beta.1"

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.util import utcnow

from .const import DOMAIN, CET
from .coordinator import spot_price, OMIEDailyCoordinator, DateFactory
from .model import OMIECoordinators, OMIESources

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""

    # OMIE data is in the CET timezone so today's date locally may be tomorrow
    # or yesterday in that timezone. we fetch (today-1,today,today+1) as that is
    # needed to correctly handle the hours when PT and ES are on different dates.
    cet_today = lambda: utcnow().astimezone(CET).date()
    cet_tomorrow = lambda: cet_today() + timedelta(days=1)
    cet_yesterday = lambda: cet_today() - timedelta(days=1)

    # These are asking to be rewritten into coordinators that do 3 fetches for each
    # OMIE source file: previous, current and next day.

    spot = OMIEDailyCoordinator(hass,
                                "spot",
                                market_updater=spot_price,
                                market_date=cet_today)

    spot_next = OMIEDailyCoordinator(hass,
                                     "spot_next",
                                     market_updater=spot_price,
                                     market_date=cet_tomorrow,
                                     none_before="13:30")

    spot_previous = OMIEDailyCoordinator(hass,
                                         "spot_previous",
                                         market_updater=spot_price,
                                         market_date=cet_yesterday)

    hass.data[DOMAIN] = OMIECoordinators(
        spot=OMIESources(today=spot, tomorrow=spot_next, yesterday=spot_previous),
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data.pop(DOMAIN)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok
