"""
Package wide configurations
"""
# pylint: disable=R0904
import os
import sys
from pathlib import Path
from threading import Lock
from typing import Optional

from dotenv import dotenv_values, find_dotenv, set_key


class ThreadSafeMeta(type):
    """
    A thread-safe implementation of Singleton
    """

    _instances: dict = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
          the returned instance
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ThreadSafeMeta):
    """
    Global program configuration, uses the dotenv package to load runtime
      configuration from a .env file, once and only once into this object,
      this object can be used through-out the code base
    """

    __package = "zoom_report"
    __version = "1.0.0"
    __default_env = "dev"
    __logfile_name = f"{__package}-{__version}.log"
    __timezone = "America/Vancouver"
    __datetime_format = "%Y-%m-%d %H:%M:%S"

    __config_dir = (
        Path().home() / "AppData" / "Local" / __package
        if os.name == "nt"
        else Path().home() / ".config" / __package
    )
    __base_dir = Path(__file__).resolve(strict=True).parent.parent
    __meeting_id_file = __base_dir / "assets" / "meeting_id.txt"
    __output_dir = Path().home() / "participants"
    __dropbox_storage_dir = "/VS-AV/Zoom Meeting Participants"

    __ragic_attendance_route = "lynvolunteer/cogv/18"
    __ragic_participants_route = "lynvolunteer/cogv/19"
    __config = dotenv_values(find_dotenv())

    try:
        __env = __config["APP_ENV"]
        __dropbox_key = __config["DROPBOX_KEY"]
        __dropbox_secret = __config["DROPBOX_SECRET"]
        __dropbox_token = __config["DROPBOX_TOKEN"]
        __ragic_api_key = __config["RAGIC_API_KEY"]
        __zoom_client_id = __config["ZOOM_CLIENT_ID"]
        __zoom_client_secret = __config["ZOOM_CLIENT_SECRET"]
        __zoom_refresh_token = __config["ZOOM_REFRESH_TOKEN"]
    except KeyError as error:
        sys.stderr.write(f"Dotenv config error: {error} is missing\n")
        sys.exit(1)

    @classmethod
    def package(cls) -> str:
        """
        Getter for package name
        """
        return cls.__package

    @classmethod
    def version(cls) -> str:
        """
        Getter for version of package
        """
        return cls.__version

    @classmethod
    def default_env(cls) -> str:
        """
        Getter for default env
        """
        return cls.__default_env

    @classmethod
    def logfile_name(cls) -> str:
        """
        Getter for logging file name
        """
        return cls.__logfile_name

    @classmethod
    def env(cls) -> Optional[str]:
        """
        Getter for config
        """
        return cls.__env

    @classmethod
    def dropbox_key(cls) -> Optional[str]:
        """
        Getter for Dropbox key
        """
        return cls.__dropbox_key

    @classmethod
    def dropbox_secret(cls) -> Optional[str]:
        """
        Getter for Dropbox secret
        """
        return cls.__dropbox_secret

    @classmethod
    def dropbox_token(cls) -> Optional[str]:
        """
        Getter for Dropbox token
        """
        return cls.__dropbox_token

    @classmethod
    def ragic_api_key(cls) -> Optional[str]:
        """
        Getter for Ragic API key
        """
        return cls.__ragic_api_key

    @classmethod
    def zoom_client_id(cls) -> Optional[str]:
        """
        Getter for Zoom client ID
        """
        return cls.__zoom_client_id

    @classmethod
    def zoom_client_secret(cls) -> Optional[str]:
        """
        Getter for Zoom client secret
        """
        return cls.__zoom_client_secret

    @classmethod
    def zoom_refresh_token(cls) -> Optional[str]:
        """
        Getter for Zoom refresh token
        """
        return cls.__zoom_refresh_token

    @classmethod
    def update_refresh_token(cls, new_token: str) -> None:
        """
        Setter for Zoom refresh token
        """
        if new_token:
            set_key(find_dotenv(), "ZOOM_REFRESH_TOKEN", new_token)
            cls.__zoom_refresh_token = new_token

    @classmethod
    def timezone(cls) -> str:
        """
        Getter for timezone
        """
        return cls.__timezone

    @classmethod
    def datetime_format(cls) -> str:
        """
        Getter for datetime format
        """
        return cls.__datetime_format

    @classmethod
    def config_dir(cls) -> Path:
        """
        Getter for config directory
        """
        return cls.__config_dir

    @classmethod
    def base_dir(cls) -> Path:
        """
        Getter for base directory
        """
        return cls.__base_dir

    @classmethod
    def meeting_id_file(cls) -> Path:
        """
        Getter for meeting id file
        """
        return cls.__meeting_id_file

    @classmethod
    def output_dir(cls) -> Path:
        """
        Getter for output directory
        """
        return cls.__output_dir

    @classmethod
    def dropbox_storage_dir(cls) -> str:
        """
        Getter for dropbox storage directory
        """
        return cls.__dropbox_storage_dir

    @classmethod
    def ragic_attendance_route(cls) -> str:
        """
        Getter for ragic attendance route
        """
        return cls.__ragic_attendance_route

    @classmethod
    def ragic_participants_route(cls) -> str:
        """
        Getter for ragic participants route
        """
        return cls.__ragic_participants_route
