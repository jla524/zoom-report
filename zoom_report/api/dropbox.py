from pathlib import Path
from dropbox import Dropbox, files


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from: Path, file_to: Path):
        """upload a file to Dropbox using API v2"""
        dbx = Dropbox(self.access_token)
        mode = files.WriteMode.overwrite
        with file_from.open('rb') as file:
            dbx.files_upload(file.read(), str(file_to), mode=mode)
