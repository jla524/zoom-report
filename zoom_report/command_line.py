"""
Parse command line arguments for this app
"""
# pylint: disable=R0903
import argparse
from zoom_report import ThreadSafeMeta


class Cli(metaclass=ThreadSafeMeta):
    """
    App specific arguments
    """
    def __init__(self):
        self.__parser = argparse.ArgumentParser(
            prog='zoom_report',
            usage='%(prog)s [options]',
            description="A Zoom attendance automation system."
        )
        self.__parser.add_argument('-a', '--all', action='store_true')
        self.__parser.add_argument('-r', '--recent', action='store_true')
        self.__parser.add_argument('-m', '--meeting', type=int)
        self.args = self.__parser.parse_args()
