"""OMIE constants."""
from datetime import timedelta
from typing import Final

import pytz

DOMAIN: Final = "omie"
DEFAULT_NAME: Final = "OMIE"
DEFAULT_UPDATE_INTERVAL = timedelta(minutes=1)
DEFAULT_TIMEOUT = timedelta(seconds=10)

CET = pytz.timezone("CET")
