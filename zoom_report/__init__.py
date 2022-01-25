"""
Package wide configurations
"""
import sys
from typing import Optional
from pathlib import Path
from threading import Lock
from dotenv import dotenv_values, find_dotenv, set_key


class ThreadSafeMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances: dict = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ThreadSafeMeta):
    """
    @description: Global program configuration, uses the dotenv package
     to load runtime configuration from a .env file, once and
     only once into this object, this object can be used through-out
     the code base
    """
    try:
        __package = 'zoom_report'
        __version = '0.2.0'
        __default_env = 'dev'
        __logfile_name = f'{__package}-{__version}.log'
        __config = dotenv_values(find_dotenv())
        __env = __config['APP_ENV']
        __dropbox_api_key = __config['DROPBOX_API_KEY']
        __ragic_api_key = __config['RAGIC_API_KEY']
        __zoom_api_key = __config['ZOOM_API_KEY']
        __zoom_api_secret = __config['ZOOM_API_SECRET']
        __zoom_jwt_token_key = 'ZOOM_JWT_TOKEN'
        __zoom_jwt_token = __config[__zoom_jwt_token_key]
        __timezone = 'America/Vancouver'
        __datetime_format = '%Y-%m-%d %H:%M:%S'
        __config_dir = Path().home() / '.config' / __package
        __base_dir = Path(__file__).resolve(strict=True).parent.parent
        __meeting_id_file = __base_dir / 'assets' / 'meeting_id.txt'
        __output_dir = Path().home() / 'participants'
        __dropbox_storage_dir = Path('/VS-AV/Zoom Meeting Participants')
        __ragic_attendance_route = 'lynvolunteer/cogv/18'
        __ragic_participants_route = 'lynvolunteer/cogv/19'
    except KeyError as error:
        sys.stderr.write(f"Dotenv config error: {error} is missing\n")
        sys.exit(1)

    @classmethod
    def package(cls) -> str:
        """
        @description: getter for package name
        """
        return cls.__package

    @classmethod
    def version(cls) -> str:
        """
        @description: getter for version of package
        """
        return cls.__version

    @classmethod
    def default_env(cls) -> str:
        """
        @description: getter for the default env
        """
        return cls.__default_env

    @classmethod
    def logfile_name(cls) -> str:
        """
        @description: getter for the logging file name
        """
        return cls.__logfile_name

    @classmethod
    def env(cls) -> Optional[str]:
        """
        @description: getter for config
        """
        return cls.__env

    @classmethod
    def dropbox_api_key(cls) -> Optional[str]:
        """
        @description: getter for dropbox api key
        """
        return cls.__dropbox_api_key

    @classmethod
    def ragic_api_key(cls) -> Optional[str]:
        """
        @description: getter for ragic api key
        """
        return cls.__ragic_api_key

    @classmethod
    def zoom_api_key(cls) -> Optional[str]:
        """
        @description: getter for zoom api key
        """
        return cls.__zoom_api_key

    @classmethod
    def zoom_api_secret(cls) -> Optional[str]:
        """
        @description: getter for zoom api secret
        """
        return cls.__zoom_api_secret

    @classmethod
    def zoom_jwt_token(cls) -> Optional[str]:
        """
        @description: getter for zoom jwt token
        """
        return cls.__zoom_jwt_token

    @classmethod
    def update_jwt_token(cls, new_token: str) -> None:
        """
        @description: update the expired token with the new one
        """
        if new_token and isinstance(new_token, str):
            set_key(find_dotenv(), cls.__zoom_jwt_token_key, new_token)
            cls.__zoom_jwt_token = new_token

    @classmethod
    def timezone(cls) -> str:
        """
        @description: getter for timzone
        """
        return cls.__timezone

    @classmethod
    def datetime_format(cls) -> str:
        """
        @description; getter for datetime format
        """
        return cls.__datetime_format

    @classmethod
    def config_dir(cls) -> Path:
        """
        @description: getter for config directory
        """
        return cls.__config_dir

    @classmethod
    def base_dir(cls) -> Path:
        """
        @description: getter for base directory
        """
        return cls.__base_dir

    @classmethod
    def meeting_id_file(cls) -> Path:
        """
        @description: getter for meeting id file
        """
        return cls.__meeting_id_file

    @classmethod
    def output_dir(cls) -> Path:
        """
        @description: getter for output directory
        """
        return cls.__output_dir

    @classmethod
    def dropbox_storage_dir(cls) -> Path:
        """
        @description: getter for dropbox storage directory
        """
        return cls.__dropbox_storage_dir

    @classmethod
    def ragic_attendance_route(cls) -> str:
        """
        @description: getter for ragic attendance route
        """
        return cls.__ragic_attendance_route

    @classmethod
    def ragic_participants_route(cls) -> str:
        """
        @description: getter for ragic participants route
        """
        return cls.__ragic_participants_route
