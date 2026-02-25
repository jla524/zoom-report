"""
Process meeting instances and details from Zoom
"""
from datetime import date, timedelta

from zoom_report import Config
from zoom_report.logger.pkg_logger import Logger
from zoom_report.common.helpers import JSON, Instance
from zoom_report.api.zoom import Zoom


def extract_instances(info: dict) -> list[Instance]:
    """
    Convert meeting instances to a sorted list with UUID and local start time.
    :param instances: instances to convert
    :returns: extracted instances
    """
    Logger.info("Extracting meeting UUIDs and local start times...")
    if not info or "meetings" not in info:
        return []
    instances = []
    for meeting in info["meetings"]:
        if "uuid" in meeting and "start_time" in meeting:
            instance = (meeting["uuid"], meeting["start_time"])
            instances.append(instance)
    instances = sorted(instances, key=lambda x: x[1])
    return instances


def filter_instances(instances: list[Instance], days: int = 365) -> list[Instance]:
    """
    Filter meeting instances that started in the past n days.
    :param instances: a list of instances to filter
    :param days: number of days to filter
    :returns: recent instances
    """
    text = "day" if days == 1 else f"{days} days"
    Logger.info(f"Filtering meetings that started in the past {text}...")
    if instances:
        date_format = Config.datetime_format().split(" ", maxsplit=1)[0]
        start_date = (date.today() - timedelta(days=days)).strftime(date_format)
        index = len(instances) - 1
        while index >= 0 and instances[index][1] > start_date:
            index -= 1
        instances = instances[index+1:]
    return instances


def get_instances(meeting_id: str, filter_days: int) -> list[Instance]:
    """
    Get meeting instances from Zoom with UUID and localized start time.
    :param meeting_id: a meeting ID to process
    :param recent: get recent meetings only
    :returns: meeting instances
    """
    response = Zoom().get_meeting_instances(meeting_id)
    instances = extract_instances(response)
    instances = filter_instances(instances, filter_days)
    return instances


def get_info(uuid: str, max_pages: int = 100) -> list[JSON]:
    """
    Get an attendance info for a given UUID.
    :param uuid: a meeting UUID to retrieve info from
    :param max_pages: maximum number of pages to retrieve
    :returns: participants info
    """
    zoom = Zoom()
    response = zoom.get_participants(uuid)
    participants = response.get("participants", [])
    page_count = 0
    while token := response.get("next_page_token"):
        page_count += 1
        if page_count > max_pages:
            Logger.error(f"Exceeded maximum page limit ({max_pages}) for UUID {uuid}")
            break
        response = zoom.get_participants(uuid, next_page_token=token)
        participants.extend(response.get("participants", []))
    return participants


def get_details(meeting_id: str) -> JSON:
    """
    Get meeting details from Zoom.
    :param meeting_id: a meeting ID to process
    :returns: meeting details
    """
    response = Zoom().get_meeting_details(meeting_id)
    if "code" in response:
        Logger.warn("An error occurred when retrieving meeting details.")
        Logger.error(response.get("message", "Unknown error."))
        return {}
    return response
