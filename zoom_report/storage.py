from pathlib import Path
from datetime import datetime
import pandas as pd
from zoom_report import Config
from zoom_report.common.enums import Cogv
from zoom_report.api.ragic import Ragic
from zoom_report.api.dropbox import TransferData
from zoom_report.logger.pkg_logger import Logger


def save_report(report, meeting_topic: str, meeting_uuid: str) -> Path:
    Logger.info("Saving report as CSV...")
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    date = datetime.today().date()
    meeting_topic = meeting_topic.replace(' ', '-')
    meeting_uuid = meeting_uuid.replace('/', '-')
    file_name = f'{meeting_topic}_{date}_{meeting_uuid}.csv'
    output_file = output_dir / file_name
    report.to_csv(output_file, index=False)
    Logger.info("Report saved in " + str(output_file))
    return output_file


def upload_report(source_file: Path) -> None:
    Logger.info("Uploading report to DropBox...")
    transfer = TransferData(Config.dropbox_api_key())
    target_file = Config.dropbox_storage_dir() / source_file.name
    transfer.upload_file(source_file, target_file)
    Logger.info("File uploaded to " + str(target_file))


def write_records(source_file: Path, meeting_info: dict) -> None:
    Logger.info("Writing records to Ragic...")
    response = Ragic().write_attendance(meeting_info)
    if response['status'] == 'INVALID':
        Logger.info("An error occurred when writing to attendance.")
        Logger.error(response['msg'])
        return
    frame = pd.read_csv(source_file)
    for _, row in frame.iterrows():
        response = Ragic().write_participants(meeting_info['uuid'], row)
        if response['status'] == 'INVALID':
            Logger.info("An error occured when writing to participants.")
            Logger.error(response['msg'])
