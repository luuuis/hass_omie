from __future__ import annotations

import logging
from datetime import datetime, date
from typing import NamedTuple, Union

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

OMIEFile = dict[str, Union[float, list[float]]]
"""A dict parsed from one of the OMIE CSV file."""


class OMIEModel(NamedTuple):
    """OMIE market results for a given date."""
    updated_at: datetime
    """The fetch date/time."""

    market_date: date
    """The day that the data relates to."""

    contents: OMIEFile
    """Data fetched from OMIE."""


class OMIESources(NamedTuple):
    """Pair of coordinators that source OMIE market results for today and tomorrow."""
    today: DataUpdateCoordinator[OMIEModel]
    """Today's market results (CET)."""

    tomorrow: DataUpdateCoordinator[OMIEModel]
    """Tomorrow's market results (CET)."""

    yesterday: DataUpdateCoordinator[OMIEModel]
    """Yesterday's market results (CET)."""


class OMIECoordinators(NamedTuple):
    spot: OMIESources
    """Spot prices."""

    adjustment: OMIESources
    """Adjustment mechanism prices."""
