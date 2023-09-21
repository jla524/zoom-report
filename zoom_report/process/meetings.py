"""
Process meeting instances and details from Zoom
"""
from typing import Any
from datetime import date, timedelta

from zoom_report import Config
from zoom_report.common.helpers import localize
from zoom_report.api.zoom import Zoom
from zoom_report.logger.pkg_logger import Logger


def extract_instances(info: dict) -> list[tuple[Any, str]]:
    """
    Convert meeting instances to a sorted list with UUID and local start time.
    :param instances: instances to convert
    :returns: localized instances
    """
    Logger.info("Extracting meeting UUIDs and local start times...")
    if not info or "meetings" not in info:
        return []

    instances = []
    for meeting in info["meetings"]:
        if "uuid" in meeting and "start_time" in meeting:
            instance = (meeting["uuid"], localize(meeting["start_time"]))
            instances.append(instance)

    instances = sorted(instances, key=lambda x: x[1])
    return instances


def filter_instances(
    instances: list[tuple[Any, str]], days: int = 1
) -> list[tuple[Any, str]]:
    """
    Filter meeting instances that started in the past n days.
    :param instances: a list of instances to filter
    :param days: number of days to filter
    :returns: recent instances
    """
    Logger.info(f"Filtering meetings that started in the past {days} days...")
    if instances:
        date_format = Config.datetime_format().split(" ", maxsplit=1)[0]
        start_date = (date.today() - timedelta(days=days)).strftime(date_format)
        index = len(instances) - 1
        while instances[index][1] > start_date:
            index -= 1
        instances = instances[index + 1 :]
    return instances


def get_instances(meeting_id: str, recent: bool) -> list[tuple[Any, str]]:
    """
    Get meeting instances from Zoom with UUID and localized start time.
    :param meeting_id: a meeting ID to process
    :param recent: get recent meetings only
    :returns: meeting instances
    """
    Logger.info("Retrieving meeting instances...")
    response = Zoom().get_meeting_instances(meeting_id)
    instances = extract_instances(response)
    if recent:
        instances = filter_instances(instances)
    # older meetings cannot be processed properly
    else:
        instances = filter_instances(instances, days=30)
    return instances


def get_details(meeting_id: str) -> dict[str, Any]:
    """
    Get meeting details from Zoom.
    :param meeting_id: a meeting ID to process
    :returns: meeting details
    """
    Logger.info("Retrieving meeting details...")
    response = Zoom().get_meeting_details(meeting_id)
    if "code" in response:
        Logger.warn("An error occured when retrieving meeting details.")
        Logger.error(response["message"])
        return {}
    return response
