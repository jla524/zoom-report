from urllib.parse import urljoin, quote_plus
from zoom_report.api.zoom import Zoom
from zoom_report.logger.pkg_logger import Logger


def get_meeting_info(instances) -> list:
    Logger.info("Retrieving list of meeting info...")
    if 'meetings' not in instances:
        Logger.error("Unable to retrieve meeting info")
        return None
    meetings = instances['meetings']
    uuids = [[meeting['uuid'], meeting['start_time']] for meeting in meetings]
    return uuids


def encode_uuid(uuid) -> str:
    if uuid.startswith('/') or '//' in uuid:
        uuid = quote_plus(quote_plus(uuid))
    return uuid
