"""This module provides logging abstraction over Python's logging module"""

import logging

class Log:

    def __init__(self, Filename=None, Level=None):
        """Constructor"""

        self.Level = Level
        self.Filename = Filename

        if self.Level == 'DEBUG':
            logging.basicConfig(filename=self.Filename, level=logging.DEBUG)
        elif self.Level == 'INFO':
            logging.basicConfig(filename=self.Filename, level=logging.INFO)
        elif self.Level == 'WARNING':
            logging.basicConfig(filename=self.Filename, level=logging.WARNING)
        elif self.Level == 'ERROR':
            logging.basicConfig(filename=self.Filename, level=logging.ERROR)
        elif self.Level == 'CRITICAL':
            logging.basicConfig(filename=self.Filename, level=logging.CRITICAL)
        else:
            raise Exception('Invalid log level ' + self.Level)

    def TeeLog(self, msg=None, level=0):
        """print to console and log"""

        if msg != None:
            print(msg)
            logging.info(msg) if level == 0 else logging.warning(msg)
