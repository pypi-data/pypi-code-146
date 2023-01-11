#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to handle all source related tasks.

Typical usage example:
  source = Source(source_path)
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Source(object):
    """A class used to initialize the source and analyze it, to see if this is a file or a directory.

    Attributes:
        _source_path {string} -- Absolute path of the source.
        _source_type {string} -- Type of source specified, whether a list, a file, or default.
        _file_paths {list[string]} - List of files found in the source provided.

    Methods:
        __init__(source_path) -- Initializes the class with all the attributes.
        _analyze() -- Creates the source list based on the input.
    """

    def __init__(self, source_path):
        """Initializes the class with all the attributes.
        """
        self._source_path = source_path
        self._source_type = ''
        self._file_paths = []

        self._analyze()

    @property
    def file_paths(self):
        """Getter method for the attribute _file_paths.
        """
        return self._file_paths

    def _get_source_type(self):
        """Identifies the type of source specified by the user.
        """
        if ':' in self._source_path:
            self._source_type = 'list'
        elif self._source_path.endswith('.txt'):
            self._source_type = 'file'
        else:
            self._source_type = 'default'

        Log().logger.debug(LogMessage.SOURCE_TYPE.value % self._source_type)

    def _analyze(self):
        """Creates the source list based on the input.

        It checks whether source is a file, list of files or a directory and then creates the source list.

        Returns:
            integer -- Return code of the method.
        """
        self._get_source_type()

        if self._source_type == 'list' or self._source_type == 'file':
            if self._source_type == 'list':
                sources = self._source_path.split(':')
            elif self._source_type == 'file':
                file_data = FileHandler().read_file(self._source_path)
                sources = file_data.strip().split('\n')

            for source in sources:
                if FileHandler().check_path_exists(source):
                    files = FileHandler().get_files(source)
                    self._file_paths.extend(files)
                    rc = 0
                else:
                    Log().logger.info(LogMessage.SOURCE_SKIP.value)
                    rc = 1

        elif self._source_type == 'default':
            if FileHandler().check_path_exists(self._source_path):
                self._file_paths = FileHandler().get_files(self._source_path)
                rc = 0
            else:
                Log().logger.info(LogMessage.SOURCE_SKIP.value)
                rc = 1

        Log().logger.debug(LogMessage.SOURCE_COUNT.value %
                           len(self._file_paths))

        return rc
        