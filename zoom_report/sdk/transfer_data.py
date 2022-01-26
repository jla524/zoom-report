"""
A wrapper for the Dropbox SDK
"""
from pathlib import Path
from dropbox import Dropbox, files


class TransferData:
    """
    Use the dropbox library to talk to Dropbox API v2.
    """
    def __init__(self, access_token: str):
        self.__access_token = access_token
        self.__overwrite = True

    @classmethod
    def set_overwrite(cls, value: bool) -> None:
        """
        Set the value of overwrite
        :param value: a boolean value
        :returns: None
        """
        cls.__overwrite = value

    def upload_file(self, source: Path, target: str) -> None:
        """
        Upload a file to Dropbox.
        :param source: a Path of the file to upload
        :param target: a Path in Dropbox to save the file
        :returns: None
        :raises: FileNotFoundError if file_from is not a file
        """
        if not source.is_file():
            raise FileNotFoundError("The file to upload does not exist.")
        client = Dropbox(self.__access_token)
        mode = (files.WriteMode.overwrite
                if self.__overwrite
                else files.WriteMode.add)
        with source.open('rb') as file:
            client.files_upload(file.read(), target, mode=mode)
