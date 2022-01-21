import argparse
from zoom_report import ThreadSafeMeta


class Cli(metaclass=ThreadSafeMeta):
    def __init__(self):
        self.__parser = argparse.ArgumentParser(
            prog='zoom_report',
            usage='%(prog)s [options]',
            description="A Zoom attendance automation system."
        )
        self.__parser.add_argument('-a', '--all', action='store_true')
        self.__parser.add_argument('-n', '--new', action='store_true')
        self.__parser.add_argument('-m', '--meeting', type=int)
        self.args = self.__parser.parse_args()
