"""
A wrapper for the Dropbox SDK
"""
from pathlib import Path
from dropbox import Dropbox, files


class TransferData:
    """
    Use the dropbox library to talk to Dropbox API v2.
    """
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from: Path, file_to: Path) -> None:
        """
        Upload a file to Dropbox.
        :param file_from: a Path of the file to upload
        :param file_to: a Path in Dropbox to save the file
        :returns: None
        :raises: FileNotFoundError if file_from is not a file
        """
        if not file_from.is_file():
            raise FileNotFoundError("The file to upload does not exist.")
        dbx = Dropbox(self.access_token)
        mode = files.WriteMode.overwrite
        with file_from.open('rb') as file:
            dbx.files_upload(file.read(), str(file_to), mode=mode)
