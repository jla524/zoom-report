import dropbox
from pathlib import Path


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from: Path, file_to: Path):
        """upload a file to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)

        with file_from.open('rb') as file:
            dbx.files_upload(file.read(), str(file_to))
