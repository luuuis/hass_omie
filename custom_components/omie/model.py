from __future__ import annotations

import logging
from datetime import datetime
from typing import NamedTuple, Union

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

OMIEFile = dict[str, Union[float, list[float]]]
"""A dict parsed from one of the OMIE CSV file."""


class OMIEModel(NamedTuple):
    """A piece of data updated at a particular time."""
    updated_at: datetime
    contents: OMIEFile


class OMIECoordinators(NamedTuple):
    spot: DataUpdateCoordinator[OMIEModel]
    """Today's spot."""

    spot_next: DataUpdateCoordinator[OMIEModel]
    """Tomorrow's spot."""

    adjustment: DataUpdateCoordinator[OMIEModel]
    """Today's adjustment."""

    adjustment_next: DataUpdateCoordinator[OMIEModel]
    """Tomorrow's adjustment."""
