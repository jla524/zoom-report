import os
from api.dropbox import TransferData
from config import Config

def upload_file(source_file, target_dir):
    transfer = TransferData(Config.dropbox_api_key())
    # TODO: use pathlib to get file name and join
    file_name = source_file.split('/')[-1]
    target_file = os.path.join(target_dir, file_name)
    transfer.upload_file(source_file, target_file)
    print(f"File written to {target_file}")