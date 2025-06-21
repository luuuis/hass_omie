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
    spot_price_es_tomorrow: str
    spot_price_pt_tomorrow: str


class DeviceNames(NamedTuple):
    """Translations used by the Device."""
    device_manufacturer: str
    device_name: str
    device_model: str


ENTITY_NAMES: Translated[EntityNames] = Translated(
    en=EntityNames(
        spot_price_es="Marginal price - Spain",
        spot_price_pt="Marginal price - Portugal",
        spot_price_es_tomorrow="Marginal price tomorrow - Spain",
        spot_price_pt_tomorrow="Marginal price tomorrow - Portugal",
    ),
    es=EntityNames(
        spot_price_es="Precio marginal - España",
        spot_price_pt="Precio marginal - Portugal",
        spot_price_es_tomorrow="Precio marginal mañana - España",
        spot_price_pt_tomorrow="Precio marginal mañana - Portugal",
    ),
    pt=EntityNames(
        spot_price_es="Preço marginal - Espanha",
        spot_price_pt="Preço marginal - Portugal",
        spot_price_es_tomorrow="Preço marginal amanhã - Espanha",
        spot_price_pt_tomorrow="Preço marginal amanhã - Portugal",
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
