"""
Write attendance data to storage
"""
from pathlib import Path

from pandas import DataFrame

from zoom_report import Config
from zoom_report.api.ragic import Ragic
from zoom_report.sdk.transfer_data import TransferData
from zoom_report.logger.pkg_logger import Logger


def generate_filepath(topic: str, uuid: str, start_time: str) -> Path:
    """
    Generate a file path using a topic, start time, and UUID.
    :param topic: topic of an instance
    :param start_time: start time of an instance
    :param uuid: UUID of an instance
    :returns: a generated file path
    """
    Logger.info("Generating file name...")
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    date = start_time.split(" ")[0]
    topic = topic.replace(" ", "-").replace("/", "-")
    uuid = uuid.replace("/", "-")
    file_name = f"{topic}_{date}_{uuid}.csv"
    output_file = output_dir / file_name
    return output_file


def save_csv(frame: DataFrame, file_path: Path) -> None:
    """
    Save a given DataFrame as a CSV file.
    :param frame: a DataFrame to save as CSV
    :returns: None
    """
    Logger.info("Saving report as CSV...")
    frame.to_csv(file_path, index=False)
    Logger.info("Report saved in " + str(file_path))


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


def write_to_ragic(frame: DataFrame, meeting_info: dict) -> bool:
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


def save_report(data: DataFrame, meeting: dict, instance: tuple[str, str]) -> None:
    """
    Write attendance report into storage.
    :param data: a DataFrame with attendance data to write
    :param meeting: meeting info from Zoom
    :param instance: instance info fromr Zoom
    """
    if data.empty:
        Logger.warn("Nothing to write, DataFrame is empty.")
        return
    uuid, start_time = instance
    path = generate_filepath(meeting["topic"], uuid, start_time)
    if file_path.exists():
        Logger.info("File already exists in storage.")
        return
    payload_info = {
        "uuid": uuid,
        "start_time": start_time,
        "topic": meeting["topic"],
        "meeting_id": meeting["id"],
    }
    if write_to_ragic(data, payload_info):
        save_csv(data, path):
        upload_to_dropbox(path)
