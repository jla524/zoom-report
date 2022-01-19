from pathlib import Path
from datetime import datetime
import pandas as pd
from zoom_report import Config
from zoom_report.common.enums import Cogv
from zoom_report.api.ragic import Ragic
from zoom_report.api.dropbox import TransferData
from zoom_report.logger.pkg_logger import Logger


def save_report(report, meeting_uuid) -> Path:
    Logger.info("Saving report as CSV...")
    output_dir = Config.output_dir()
    output_dir.mkdir(exist_ok=True)
    date = datetime.today().date()
    file_name = f'{meeting_uuid}_{date}.csv'.replace('/', '%f')
    output_file = output_dir / file_name
    report.to_csv(output_file, index=False)
    Logger.info("Report saved in " + str(output_file))
    return output_file


def upload_file(source_file: Path) -> None:
    transfer = TransferData(Config.dropbox_api_key())
    target_file = Config.dropbox_storage_dir() / source_file.name
    transfer.upload_file(source_file, target_file)
    Logger.info("File uploaded to " + str(target_file))


def write_records(source_file: Path) -> None:
    frame = pd.read_csv(source_file)
    for _, row in frame.iterrows():
        payload = {Cogv.MEETING_NUMBER: row['uuid'],
                   Cogv.TOPIC: row['topic'],
                   Cogv.DURATION: row['total_duration'],
                   Cogv.MEETING_ID: row['meeting_id'],
                   Cogv.START_TIME: row['start_time'],
                   Cogv.NAME: row['name'],
                   Cogv.EMAIL: row['user_email'],
                   Cogv.TOTAL_DURATION: row['total_duration'],
                   Cogv.JOIN_TIME: row['join_time'],
                   Cogv.LEAVE_TIME: row['leave_time']}
        Logger.debug(payload)
        Ragic().send_data(payload)
