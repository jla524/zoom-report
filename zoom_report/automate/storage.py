"""
Write attendance data to storage
"""
from pathlib import Path
from pandas import DataFrame
from zoom_report import Config
from zoom_report.api.ragic import Ragic
from zoom_report.sdk.transfer_data import TransferData
from zoom_report.logger.pkg_logger import Logger


def write_csv(data: DataFrame, topic: str, timestamp: str, uuid: str) -> Path:
    """
    Save a given DataFrame as a CSV file with topic, timestamp, and UUID.
    :param data: a DataFrame to save
    :param topic: topic of an instance
    :param timestamp: start time of an instance
    :param uuid: UUID of an instance
    :returns: Path where the CSV file is stored
    """
    Logger.info("Saving report as CSV...")
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    date = timestamp.split(' ')[0]
    topic = topic.replace(' ', '-').replace('/', '-')
    uuid = uuid.replace('/', '-')
    file_name = f'{topic}_{date}_{uuid}.csv'
    output_file = output_dir / file_name
    data.to_csv(output_file, index=False)
    Logger.info("Report saved in " + str(output_file))
    return output_file


def to_dropbox(source_file: Path) -> None:
    """
    Upload a given file to a pre-configured directory in DropBox.
    :param source_file: Path of the file to upload
    :returns: None
    """
    Logger.info("Uploading report to DropBox...")
    transfer = TransferData(str(Config.dropbox_api_key()))
    target_file = f"{Config.dropbox_storage_dir()}/{source_file.name}"
    transfer.upload_file(source_file, target_file)
    Logger.info("File uploaded to " + str(target_file))


def to_ragic(frame: DataFrame, meeting_info: dict) -> None:
    """
    Write a given attendance report to a pre-configured route in Ragic.
    :param frame: a DataFrame with attendance data to write
    :param meeting_info: relevant info for a meeting
    :returns: None
    """
    Logger.info("Writing records to Ragic...")
    response = Ragic().write_attendance(meeting_info)
    if response['status'] == 'INVALID':
        Logger.warn("An error occurred when writing to attendance.")
        Logger.error(response['msg'])
        return
    for _, row in frame.iterrows():
        response = Ragic().write_participants(meeting_info['uuid'], row)
        if response['status'] == 'INVALID':
            Logger.warn("An error occured when writing to participants.")
            Logger.error(response['msg'])


def save_report(data: DataFrame, meeting: dict,
                instance: tuple[str, str]) -> None:
    """
    Write a given DataFrame into storage.
    :param data: a DataFrame with attendance data to write
    :param meeting: meeting info from Zoom
    :param instance: instance info fromr Zoom
    """
    if data.empty:
        Logger.error("DataFrame is empty")
        return
    uuid, start_time = instance
    file_path = write_csv(data, meeting['topic'], start_time, uuid)
    to_dropbox(file_path)
    payload_info = {'uuid': uuid,
                    'start_time': start_time,
                    'topic': meeting['topic'],
                    'meeting_id': meeting['id']}
    to_ragic(data, payload_info)
