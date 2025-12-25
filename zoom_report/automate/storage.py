"""
Write attendance data to storage
"""
from time import sleep

import pandas as pd

from zoom_report.logger.pkg_logger import Logger
from zoom_report.api.ragic import Ragic
from zoom_report.common.helpers import JSON, handle_api_status

API_DELAY = 2.5


def write_to_ragic(frame: pd.DataFrame, meeting_info: JSON, delay: float = API_DELAY) -> bool:
    """
    Write a given attendance report to a pre-configured route in Ragic.
    :param frame: a DataFrame with attendance data to write
    :param meeting_info: relevant info for a meeting
    :returns: True if data is written successfully and False otherwise
    """
    ragic = Ragic()
    Logger.info("Writing records to Ragic...")
    response = ragic.write_attendance(meeting_info)
    if handle_api_status(response, "writing to attendance"):
        participants = ragic.read_participants(meeting_info["uuid"])
        names = [participant["Name"] for participant in participants if "Name" in participant]
        frame = frame[~frame["name"].isin(names)]
    else:
        Logger.warn("Attempting to update existing attendance...")
    for _, row in frame.iterrows():
        response = ragic.write_participant(meeting_info["uuid"], row)
        if handle_api_status(response, "writing to participants"):
            sleep(delay)  # wait a few seconds to avoid API limits
    return True


def save_report(meeting_id: str, meeting_info: JSON, attendance: pd.DataFrame) -> bool:
    """
    Write attendance report into storage.
    :param meeting_info: meeting info from Zoom
    :param attendance: a DataFrame with attendance data to write
    :returns: True if report is saved and False otherwise
    """
    if attendance.empty:
        Logger.warn("Nothing to save, DataFrame is empty.")
        return False
    payload_info = {
        "uuid": meeting_info["uuid"],
        "start_time": meeting_info["start_time"],
        "topic": meeting_info["topic"],
        "meeting_id": meeting_id,
    }
    return write_to_ragic(attendance, payload_info)
