import logging
import statistics

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import (ConfigEntry)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import slugify, utcnow

from . import OMIECoordinators
from .const import DOMAIN
from .model import OMIEModel

_LOGGER = logging.getLogger(__name__)

ENTITY_NAMES = {
    "en": {
        "spot_price_es": "Marginal price - Spain",
        "spot_price_pt": "Marginal price - Portugal",
        "adjustment_price_es": "Adjustment mechanism price - Spain",
        "adjustment_price_pt": "Adjustment mechanism price - Portugal",
        "adjustment_unit_price": "Adjustment unit amount for production facilities",
        "spot_price_es_tomorrow": "Marginal price tomorrow - Spain",
        "spot_price_pt_tomorrow": "Marginal price tomorrow - Portugal",
        "adjustment_price_es_tomorrow": "Adjustment mechanism price tomorrow - Spain",
        "adjustment_price_pt_tomorrow": "Adjustment mechanism price tomorrow - Portugal",
        "adjustment_unit_price_tomorrow": "Adjustment unit amount for production facilities tomorrow"
    },
    "es": {
        "spot_price_es": "Precio marginal - España",
        "spot_price_pt": "Precio marginal - Portugal",
        "adjustment_price_es": "Precio del mecanismo de ajuste - España",
        "adjustment_price_pt": "Precio del mecanismo de ajuste - Portugal",
        "adjustment_unit_price": "Cuantía unitaria del ajuste para instalaciones de producción",
        "spot_price_es_tomorrow": "Precio marginal mañana - España",
        "spot_price_pt_tomorrow": "Precio marginal mañana - Portugal",
        "adjustment_price_es_tomorrow": "Precio del mecanismo de ajuste mañana - España",
        "adjustment_price_pt_tomorrow": "Precio del mecanismo de ajuste mañana - Portugal",
        "adjustment_unit_price_tomorrow": "Cuantía unitaria del ajuste para instalaciones de producción mañana"
    },
    "pt": {
        "spot_price_es": "Preço marginal - Espanha",
        "spot_price_pt": "Preço marginal - Portugal",
        "adjustment_price_es": "Preço do mecanismo de ajuste - Espanha",
        "adjustment_price_pt": "Preço do mecanismo de ajuste - Portugal",
        "adjustment_unit_price": "Valor unitário do ajuste para instalações de produção",
        "spot_price_es_tomorrow": "Preço marginal amanhã - Espanha",
        "spot_price_pt_tomorrow": "Preço marginal amanhã - Portugal",
        "adjustment_price_es_tomorrow": "Preço do mecanismo de ajuste amanhã - Espanha",
        "adjustment_price_pt_tomorrow": "Preço do mecanismo de ajuste amanhã - Portugal",
        "adjustment_unit_price_tomorrow": "Valor unitário do ajuste para instalações de produção amanhã"
    },
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up OMIE from its config entry."""
    coordinators: OMIECoordinators = hass.data[DOMAIN]

    device_info = DeviceInfo(
        configuration_url="https://www.omie.es/es/market-results",
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, entry.entry_id)},
        manufacturer="OMIE",
        name="OMIE.es",
        model="MIBEL market results",
    )

    lang = hass.config.language.split('-')[0]
    entity_names = ENTITY_NAMES[lang if lang in ENTITY_NAMES.keys() else 'en']

    class PriceEntity(SensorEntity):
        def __init__(self, coordinator: DataUpdateCoordinator[OMIEModel], key: str, id_suffix: str = ''):
            """Initialize the sensor."""
            self._attr_device_info = device_info
            self._attr_native_unit_of_measurement = "EUR/MWh"
            self._attr_state_class = SensorStateClass.MEASUREMENT
            self._attr_unique_id = slugify(f'omie_{key}{id_suffix}')
            self._attr_name = entity_names[f'{key}{id_suffix}']
            self._attr_icon = "mdi:currency-eur"
            self._attr_should_poll = False
            self._key = key
            self._coordinator = coordinator
            self.entity_id = f"sensor.{self._attr_unique_id}"

        async def async_added_to_hass(self) -> None:
            """Register callbacks."""
            expose_attrs = ['fetched', 'market_date', 'source', 'header']

            @callback
            def update() -> None:
                """Update the state."""
                if self.enabled:
                    known = self._coordinator.data is not None
                    if known:
                        prices = self._coordinator.data.contents
                        day_hours = prices[f'{self._key}_hourly']

                        # @todo handle longer and shorter days due to DST:
                        self._attr_native_value = day_hours[utcnow().astimezone().hour]
                        self._attr_extra_state_attributes = {k: prices[k] for k in expose_attrs} | {
                            'day_hours': day_hours,
                            'day_average': round(statistics.mean(day_hours), 2)
                        }
                    else:
                        self._attr_native_value = None

                    self.async_schedule_update_ha_state()

            self.async_on_remove(self._coordinator.async_add_listener(update))

    sensors = [
        # Today
        PriceEntity(coordinators.spot, "spot_price_pt"),
        PriceEntity(coordinators.spot, "spot_price_es"),
        PriceEntity(coordinators.adjustment, "adjustment_price_es"),
        PriceEntity(coordinators.adjustment, "adjustment_price_pt"),
        PriceEntity(coordinators.adjustment, "adjustment_unit_price"),

        # Tomorrow
        PriceEntity(coordinators.spot_next, "spot_price_pt", id_suffix='_tomorrow'),
        PriceEntity(coordinators.spot_next, "spot_price_es", id_suffix='_tomorrow'),
        PriceEntity(coordinators.adjustment_next, "adjustment_price_es", id_suffix='_tomorrow'),
        PriceEntity(coordinators.adjustment_next, "adjustment_price_pt", id_suffix='_tomorrow'),
        PriceEntity(coordinators.adjustment_next, "adjustment_unit_price", id_suffix='_tomorrow'),
    ]

    async_add_entities(sensors, update_before_add=True)
    for c in [coordinators.spot, coordinators.adjustment, coordinators.spot_next, coordinators.adjustment_next]:
        await c.async_config_entry_first_refresh()

    return True
