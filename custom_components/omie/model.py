from __future__ import annotations

import logging
from typing import NamedTuple, Union, TypeVar, Generic

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyomie.model import OMIEResults

_LOGGER = logging.getLogger(__name__)

OMIEFile = dict[str, Union[float, list[float]]]
"""A dict parsed from one of the OMIE CSV file."""

_DataT = TypeVar("_DataT")


class OMIESources(NamedTuple, Generic[_DataT]):
    """Pair of coordinators that source OMIE market results for today and tomorrow."""
    today: DataUpdateCoordinator[OMIEResults[_DataT]]
    """Today's market results (CET)."""

    tomorrow: DataUpdateCoordinator[OMIEResults[_DataT]]
    """Tomorrow's market results (CET)."""

    yesterday: DataUpdateCoordinator[OMIEResults[_DataT]]
    """Yesterday's market results (CET)."""


class OMIECoordinators(NamedTuple):
    spot: OMIESources
    """Spot prices."""
