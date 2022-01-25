"""
Helper functions
"""
from datetime import datetime
from urllib.parse import quote_plus
from zoom_report import Config


def encode_uuid(uuid: str) -> str:
    """
    Double encode a Zoom uuid if it starts with / or contains //.
    :param uuid: the uuid to encode
    :returns: the encoded uuid
    """
    if uuid.startswith('/') or '//' in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid


def localize(timestamp: str) -> str:
    """
    Convert an ISO timestamp from UTC time to local time.
    :param timestamp: the timestamp to convert
    :returns: a timestamp in local time
    """
    timestamp = timestamp.replace('Z', '+00:00')
    timestamp = datetime.fromisoformat(timestamp) \
        .astimezone(None) \
        .strftime(Config.datetime_format())
    return timestamp
