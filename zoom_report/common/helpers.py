from datetime import datetime
from urllib.parse import quote_plus
from zoom_report import Config
from zoom_report.api.zoom import Zoom
from zoom_report.logger.pkg_logger import Logger


def get_meeting_info(instances: list[dict]) -> list[list[str]]:
    Logger.info("Retrieving list of meeting info...")
    if 'meetings' not in instances:
        Logger.error("Unable to retrieve meeting info")
        return None
    meetings = instances['meetings']
    info = [(meeting['uuid'], meeting['start_time']) for meeting in meetings]
    return sorted(info, key=lambda x: x[1])


def encode_uuid(uuid: str) -> str:
    Logger.info("Encoding meeting uuid...")
    if uuid.startswith('/') or '//' in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid


def localize(timestamp: str) -> str:
    timestamp = timestamp.replace('Z', '+00:00')
    timestamp = datetime.fromisoformat(timestamp)
    timestamp = timestamp.astimezone(None)
    return timestamp.strftime(Config.datetime_format())
