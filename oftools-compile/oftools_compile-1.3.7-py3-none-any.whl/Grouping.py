#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to group all working directories and aggregate the logs.

Typical usage example:
  grouping = Grouping()
  grouping.run()
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from .Context import Context
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Grouping(object):
    """A class used to group all working directory in on group directory, as well as aggregating all 
    compilation logs in one group log.

    Attributes:
        _clear {boolean} -- Value of the argument clear from the CLI.
        _directory {string} -- Absolute path of the group directory.
        _log {string} -- Absolute path of the group log file.

    Methods:
        __init(clear) -- Initializes the class with all the attributes.
        _aggregate_logs() -- Performs log aggregation.
        run(): General run method for the Grouping module.
    """

    def __init__(self, clear):
        """Initializes the class with all the attributes.
        """
        self._clear = clear

        self._directory = Context().exec_working_dir
        self._log = os.path.join(self._directory, 'group.log')

    def _aggregate_logs(self):
        """Performs log aggregation.

        Arguments:
            working_dir {string} -- Absolute path of the current working directory.
        """
        working_dirs = [
            d.path for d in os.scandir(self._directory) if d.is_dir()
        ]

        with open(self._log, 'w') as group_log:

            for working_dir in working_dirs:
                files = os.listdir(working_dir)

                for file_name in files:
                    if file_name == 'oftools_compile.log':
                        # Retrieve absolute path of the current log file
                        file_path = os.path.join(working_dir, file_name)

                        with open(file_path, 'r') as oftools_compile_log:
                            # Read the log file and write to group log file
                            Log().logger.debug(
                                LogMessage.AGGREGATE_LOG_FILE.value % file_path)

                            group_log.write(oftools_compile_log.read())
                            group_log.write('\n\n')

    def run(self):
        """General run method for the Grouping module.

        Returns:
            integer -- Return code of the method.
        """
        if self._clear is True:
            rc = FileHandler().delete_directory(self._directory)
        else:
            self._aggregate_logs()
            rc = 0

        return rc