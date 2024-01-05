"""
Helper functions
"""
from typing import Any
from datetime import datetime
from urllib.parse import quote_plus

import pytz

from zoom_report import Config

JSON = dict[str, Any]
Instance = tuple[str, str]


def encode_uuid(uuid: str) -> str:
    """
    Double encode a given UUID if it starts with / or contains //.
    :param uuid: a UUID to encode
    :returns: an encoded UUID
    """
    if uuid.startswith("/") or "//" in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid
