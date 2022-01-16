from pathlib import Path
from config import Config
from api.dropbox import TransferData


def upload_file(source_file: Path) -> None:
    transfer = TransferData(Config.dropbox_api_key())
    target_file = Config.output_dir() / source_file.name
    transfer.upload_file(source_file, target_file)
    print(f"File uploaded to {target_file}")
