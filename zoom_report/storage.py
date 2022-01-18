from pathlib import Path
from datetime import datetime
from zoom_report import Config
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
