from __future__ import annotations

import logging
import statistics
from datetime import datetime, timedelta, tzinfo, date

import pytz
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import (ConfigEntry)
from homeassistant.const import CURRENCY_EURO
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify, utcnow
from pytz.tzinfo import StaticTzInfo

from . import OMIECoordinators
from .const import DOMAIN, CET
from .model import OMIESources, OMIEModel
from .translations import ENTITY_NAMES, DEVICE_NAMES

_LOGGER = logging.getLogger(__name__)

_TZ_LISBON = pytz.timezone('Europe/Lisbon')
_TZ_MADRID = pytz.timezone('Europe/Madrid')


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up OMIE from its config entry."""
    coordinators: OMIECoordinators = hass.data[DOMAIN]

    device_names = DEVICE_NAMES.get_all(hass.config.language)
    device_info = DeviceInfo(
        configuration_url=f"https://www.omie.es/{DEVICE_NAMES.lang(hass.config.language)}/market-results",
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, entry.entry_id)},
        manufacturer=device_names.device_manufacturer,
        name=device_names.device_name,
        model=device_names.device_model,
    )

    entity_names = ENTITY_NAMES.get_all(hass.config.language)

    class PriceEntity(SensorEntity):
        def __init__(self, sources: OMIESources, key: str, tz: tzinfo):
            """Initialize the sensor."""
            self._attr_device_info = device_info
            self._attr_native_unit_of_measurement = f"{CURRENCY_EURO}/{UnitOfEnergy.MEGA_WATT_HOUR}"
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_unique_id = slugify(f'omie_{key}')
            self._attr_name = getattr(entity_names, f'{key}')
            self._attr_icon = "mdi:currency-eur"
            self._attr_should_poll = False
            self._key = key
            self._sources = sources
            self._tz = tz
            self.entity_id = f"sensor.{self._attr_unique_id}"

        async def async_added_to_hass(self) -> None:
            """Register callbacks."""

            @callback
            def update() -> None:
                """Update this sensor's state."""
                today_data = self._sources.today.data
                tomorrow_data = self._sources.tomorrow.data
                yesterday_data = self._sources.yesterday.data

                if None in [today_data, yesterday_data]:
                    # not all necessary data available yet
                    self._attr_native_value = None
                    self._attr_extra_state_attributes = None
                    return

                series_name = f'{self._key}_hourly'

                cet_today_hourly_data = _localize_hourly_data(today_data, series_name)
                cet_tomorrow_hourly_data = _localize_hourly_data(tomorrow_data, series_name)
                cet_yesterday_hourly_data = _localize_hourly_data(yesterday_data, series_name)
                cet_hourly_data = cet_yesterday_hourly_data | cet_today_hourly_data | cet_tomorrow_hourly_data

                local_tz = pytz.timezone(self.hass.config.time_zone)
                now = utcnow().astimezone(local_tz)
                today = now.date()
                tomorrow = today + timedelta(days=1)

                local_today_hourly_data = {h: cet_hourly_data.get(h.astimezone(CET)) for h in _day_hours(today, local_tz)}
                local_tomorrow_hourly_data = {h: cet_hourly_data.get(h.astimezone(CET)) for h in _day_hours(tomorrow, local_tz)}
                local_start_of_hour = local_tz.normalize(now.replace(minute=0, second=0, microsecond=0))

                self._attr_native_value = local_today_hourly_data.get(local_start_of_hour)
                self._attr_extra_state_attributes = {
                    'OMIE_today_average': _day_average(cet_today_hourly_data),
                    'today_provisional': None in local_today_hourly_data.values(),
                    'today_average': _day_average(local_today_hourly_data),
                    'today_hours': local_today_hourly_data,
                    'OMIE_tomorrow_average': _day_average(cet_tomorrow_hourly_data),
                    'tomorrow_provisional': len(local_tomorrow_hourly_data) == 0 or None in local_tomorrow_hourly_data.values(),
                    'tomorrow_average': _day_average(local_tomorrow_hourly_data),
                    'tomorrow_hours': local_tomorrow_hourly_data if len(local_tomorrow_hourly_data) > 0 else None,
                }

                self.async_schedule_update_ha_state()

            self.async_on_remove(self._sources.today.async_add_listener(update))
            self.async_on_remove(self._sources.tomorrow.async_add_listener(update))
            self.async_on_remove(self._sources.yesterday.async_add_listener(update))

    sensors = [
        PriceEntity(sources=coordinators.spot, key="spot_price_pt", tz=_TZ_LISBON),
        PriceEntity(sources=coordinators.spot, key="spot_price_es", tz=_TZ_MADRID),
        PriceEntity(sources=coordinators.adjustment, key="adjustment_price_pt", tz=_TZ_LISBON),
        PriceEntity(sources=coordinators.adjustment, key="adjustment_price_es", tz=_TZ_MADRID),
    ]

    async_add_entities(sensors, update_before_add=True)
    for c in [coordinators.spot, coordinators.adjustment]:
        await c.today.async_config_entry_first_refresh()
        await c.tomorrow.async_config_entry_first_refresh()
        await c.yesterday.async_config_entry_first_refresh()

    return True


def _localize_hourly_data(results: OMIEModel, key: str) -> dict[datetime, float]:
    """Localize incoming hourly data to the CET timezone."""
    if results is None:
        return {}
    else:
        market_date = results.market_date
        hourly_data: list[float] = results.contents[key]

        hours_in_day = len(hourly_data)  # between 23 and 25 (inclusive) due to DST changeover
        midnight = CET.localize(datetime(market_date.year, market_date.month, market_date.day))
        return {CET.normalize(midnight + timedelta(hours=h)): hourly_data[h] for h in range(hours_in_day)}


def _day_hours(day: date, tz: StaticTzInfo) -> list[datetime]:
    """Returns a list of every hour in the given date, normalized to the given time zone."""
    zero = tz.localize(datetime(day.year, day.month, day.day))
    hours = [tz.normalize(zero + timedelta(hours=h)) for h in range(25)]
    return [h for h in hours if h.date() == day]  # 25th hour only occurs once a year


def _day_average(hours_in_day: dict[datetime, float]) -> float | None:
    """Returns the arithmetic mean of the hours' prices if possible."""
    values = [] if hours_in_day is None else list(filter(lambda elem: elem is not None, hours_in_day.values()))
    if len(values) == 0:
        return None
    else:
        return round(statistics.mean(values), 2)
