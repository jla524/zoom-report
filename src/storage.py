from pathlib import Path
from config import Config
from api.dropbox import TransferData
from logger.pkg_logger import Logger


def upload_file(source_file: Path) -> None:
    transfer = TransferData(Config.dropbox_api_key())
    target_file = Config.dropbox_storage_dir() / source_file.name
    transfer.upload_file(source_file, target_file)
    Logger.info("File uploaded to " + str(target_file))
