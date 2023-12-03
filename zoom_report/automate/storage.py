"""
Write attendance data to storage
"""
from pathlib import Path
from typing import Any

from pandas import DataFrame

from zoom_report import Config
from zoom_report.api.ragic import Ragic
from zoom_report.sdk.transfer_data import TransferData
from zoom_report.local.disk import generate_filepath, save_to_disk
from zoom_report.logger.pkg_logger import Logger

JSON = dict[str, Any]

def upload_to_dropbox(source_file: Path) -> None:
    """
    Upload a given file to a pre-configured directory in DropBox.
    :param source_file: Path of the file to upload
    :returns: None
    """
    Logger.info("Uploading report to DropBox...")
    transfer = TransferData(Config.dropbox_key(), Config.dropbox_secret(), Config.dropbox_token())
    target_file = f"{Config.dropbox_storage_dir()}/{source_file.name}"
    transfer.upload_file(source_file, target_file)
    Logger.info("File uploaded to " + str(target_file))


def write_to_ragic(frame: DataFrame, meeting_info: JSON) -> bool:
    """
    Write a given attendance report to a pre-configured route in Ragic.
    :param frame: a DataFrame with attendance data to write
    :param meeting_info: relevant info for a meeting
    :returns: True if data is written successfully and False otherwise
    """
    Logger.info("Writing records to Ragic...")
    response = Ragic().write_attendance(meeting_info)
    if response["status"] == "INVALID":
        Logger.warn("An error occurred when writing to attendance.")
        Logger.error(response["msg"])
        return False
    for _, row in frame.iterrows():
        response = Ragic().write_participants(meeting_info["uuid"], row)
        if response["status"] == "INVALID":
            Logger.warn("An error occured when writing to participants.")
            Logger.error(response["msg"])
            return False
    return True


def save_report(
    meeting_id: str, attendance: DataFrame, meeting_info: JSON, instance_info: tuple[str, str]
) -> bool:
    """
    Write attendance report into storage.
    :param attendance: a DataFrame with attendance data to write
    :param meeting_info: meeting info from Zoom
    :param instance_info: instance info from Zoom
    :returns: True if report is saved and False otherwise
    """
    if attendance.empty:
        Logger.warn("Nothing to save, DataFrame is empty.")
        return False

    uuid, start_time = instance_info
    path = generate_filepath(meeting_info["topic"], uuid, start_time)
    if path.exists():
        Logger.info("File already exists in storage.")
        return False

    payload_info = {
        "uuid": uuid,
        "start_time": start_time,
        "topic": meeting_info["topic"],
        "meeting_id": meeting_id,
    }
    if not write_to_ragic(attendance, payload_info):
        return False

    save_to_disk(attendance, path)
    upload_to_dropbox(path)
    Logger.info("Report has been saved in storage.")
    return True
