"""
Set up a thread safe singleton meta class
Adapted from https://github.com/mattcoding4days/kickstart
"""
from typing import Any

from zoom_report import Config

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": ("%(log_color)s%(levelname)-8s%(reset)s " "%(blue)s%(message)s"),
        },
        "simple": {"format": "%(levelname)s - %(message)s"},
        "pedantic": {
            "format": (
                "%(asctime)s - %(module)s - %(funcName)s - %(name)s - "
                "%(lineno)d - %(levelname)s - %(message)s"
            )
        },
    },
    "handlers": {
        "console-color": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": str(Config.config_dir() / Config.logfile_name()),
            "formatter": "pedantic",
        },
    },
    "loggers": {
        "dev": {
            "handlers": [
                "console-color",
                "file_handler",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
        "prod": {
            "handlers": [
                "file_handler",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {"handlers": ["file_handler"]},
}
