"""
Customized system wide logger
Adapted from https://github.com/mattcoding4days/kickstart
"""
# pylint: disable=R0903
import sys
import logging
from logging.config import dictConfig
from pathlib import Path

from colorama import init, Back, Fore

from zoom_report import ThreadSafeMeta, Config
from zoom_report.logger import LOGGING_CONFIG


init(autoreset=True)


class LoggerLoader(metaclass=ThreadSafeMeta):
    """
    A global singleton logger loader
    """

    def __init__(self):
        self.__log_dump: Path = Config.config_dir()
        self.__load_config()

    def __load_config(self):
        """
        Load the config dictionary
        :returns: none
        """
        # if dump site doesn't exist, create it,
        # and all parent folders leading up to it
        if not self.__log_dump.is_dir():
            self.__log_dump.mkdir(parents=True)

        try:
            # if syntax is wrong, logging module will raise ValueError,
            # catch, and exit execution
            dictConfig(LOGGING_CONFIG)
        except ValueError as error:
            sys.stderr.write(
                f"{Fore.RED}Loading default logging config failed, "
                f"syntax error\n\n{error}"
            )
            sys.exit(1)
        except KeyError as error:
            sys.stderr.write(
                f"{Fore.RED}Loading logging config failed, " f"syntax error\n\n{error}"
            )
            sys.exit(1)

    @staticmethod
    def load() -> logging.Logger:
        """
        Return a logger by name.
        :returns: an instance of Logger configured by custom params
        """
        # first test to see if the name is a valid defined logger name
        valid: bool = False
        try:
            for logger_name in LOGGING_CONFIG["loggers"]:
                if logger_name == Config.env():
                    valid = True
        except KeyError as error:
            sys.stderr.write(f"{error}")

        if not valid:
            # name passed is not a valid listed logger,
            # return dev as default logger
            sys.stderr.write(
                f"\n{Back.BLACK}{Fore.RED}{Config.env()}: "
                "IS NOT A VALID LOGGER\n"
                f"{Back.BLACK}{Fore.YELLOW}FALLING BACK TO "
                f"{Config.default_env()}\n"
            )
            logger = logging.getLogger(Config.default_env())
            return logger

        logger = logging.getLogger(Config.env())
        return logger


class Logger(metaclass=ThreadSafeMeta):
    """
    The actual logger class to use
    """

    __logger = LoggerLoader().load()

    @classmethod
    def debug(cls, msg: str):
        """
        Wrapper around the logging object
        :param msg: the message to log
        """
        cls.__logger.debug(msg)

    @classmethod
    def info(cls, msg: str):
        """
        Wrapper around the logging object
        :param msg: the message to log
        """
        cls.__logger.info(msg)

    @classmethod
    def warn(cls, msg: str):
        """
        Wrapper around the logging object
        :param msg: the message to log
        """
        cls.__logger.warning(msg)

    @classmethod
    def error(cls, msg: str):
        """
        Wrapper around the logging object
        :param msg: the message to log
        """
        cls.__logger.error(msg)
