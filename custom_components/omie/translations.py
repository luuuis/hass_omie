from typing import NamedTuple, TypeVar, Generic

T = TypeVar('T')


class Translated(Generic[T]):
    en: T
    es: T
    pt: T

    def __init__(self, en: T, es: T, pt: T) -> None:
        super().__init__()
        self.en = en
        self.es = es
        self.pt = pt

    @staticmethod
    def lang(locale: str) -> str:
        """Returns the best language for the provided locale string (e.g. `en-GB`)."""
        lang = locale.split('-')[0]
        return lang if lang in ['en', 'es', 'pt'] else 'en'

    def get_all(self, locale: str) -> T:
        """Returns the translations for the given lang or the default language if lang is unknown."""
        return getattr(self, Translated.lang(locale))


class EntityNames(NamedTuple):
    """Translations used by the sensors."""
    spot_price_es: str
    spot_price_pt: str
    adjustment_price_es: str
    adjustment_price_pt: str
    adjustment_unit_price: str
    spot_price_es_tomorrow: str
    spot_price_pt_tomorrow: str
    adjustment_price_es_tomorrow: str
    adjustment_price_pt_tomorrow: str
    adjustment_unit_price_tomorrow: str


class DeviceNames(NamedTuple):
    """Translations used by the Device."""
    device_manufacturer: str
    device_name: str
    device_model: str


ENTITY_NAMES: Translated[EntityNames] = Translated(
    en=EntityNames(
        spot_price_es="Marginal price - Spain",
        spot_price_pt="Marginal price - Portugal",
        adjustment_price_es="Adjustment mechanism price - Spain",
        adjustment_price_pt="Adjustment mechanism price - Portugal",
        adjustment_unit_price="Adjustment unit amount for production facilities",
        spot_price_es_tomorrow="Marginal price tomorrow - Spain",
        spot_price_pt_tomorrow="Marginal price tomorrow - Portugal",
        adjustment_price_es_tomorrow="Adjustment mechanism price tomorrow - Spain",
        adjustment_price_pt_tomorrow="Adjustment mechanism price tomorrow - Portugal",
        adjustment_unit_price_tomorrow="Adjustment unit amount for production facilities tomorrow",
    ),
    es=EntityNames(
        spot_price_es="Precio marginal - España",
        spot_price_pt="Precio marginal - Portugal",
        adjustment_price_es="Precio del mecanismo de ajuste - España",
        adjustment_price_pt="Precio del mecanismo de ajuste - Portugal",
        adjustment_unit_price="Cuantía unitaria del ajuste para instalaciones de producción",
        spot_price_es_tomorrow="Precio marginal mañana - España",
        spot_price_pt_tomorrow="Precio marginal mañana - Portugal",
        adjustment_price_es_tomorrow="Precio del mecanismo de ajuste mañana - España",
        adjustment_price_pt_tomorrow="Precio del mecanismo de ajuste mañana - Portugal",
        adjustment_unit_price_tomorrow="Cuantía unitaria del ajuste para instalaciones de producción mañana",
    ),
    pt=EntityNames(
        spot_price_es="Preço marginal - Espanha",
        spot_price_pt="Preço marginal - Portugal",
        adjustment_price_es="Preço do mecanismo de ajuste - Espanha",
        adjustment_price_pt="Preço do mecanismo de ajuste - Portugal",
        adjustment_unit_price="Valor unitário do ajuste para instalações de produção",
        spot_price_es_tomorrow="Preço marginal amanhã - Espanha",
        spot_price_pt_tomorrow="Preço marginal amanhã - Portugal",
        adjustment_price_es_tomorrow="Preço do mecanismo de ajuste amanhã - Espanha",
        adjustment_price_pt_tomorrow="Preço do mecanismo de ajuste amanhã - Portugal",
        adjustment_unit_price_tomorrow="Valor unitário do ajuste para instalações de produção amanhã",
    ),
)

DEVICE_NAMES: Translated[DeviceNames] = Translated(
    en=DeviceNames(
        device_manufacturer="OMI Group",
        device_name="OMIE",
        device_model="MIBEL market results",
    ),
    es=DeviceNames(
        device_manufacturer="Grupo OMI",
        device_name="OMIE",
        device_model="Resultados del MIBEL",
    ),
    pt=DeviceNames(
        device_manufacturer="Grupo OMI",
        device_name="OMIE",
        device_model="Resultados do MIBEL",
    ),
)
