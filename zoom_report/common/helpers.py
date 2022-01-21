from datetime import datetime
from urllib.parse import quote_plus
from zoom_report import Config


def encode_uuid(uuid: str) -> str:
    if uuid.startswith('/') or '//' in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid


def localize(timestamp: str) -> str:
    timestamp = timestamp.replace('Z', '+00:00')
    timestamp = datetime.fromisoformat(timestamp)
    timestamp = timestamp.astimezone(None)
    return timestamp.strftime(Config.datetime_format())
