#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of variables and parameters for program execution.

Typical usage example:
  Context().tag = args.tag
  Context().clear()
"""

# Generic/Built-in modules
import datetime
import os
import sys

# Third-party modules

# Owned modules
from .enums.ErrorEnum import ErrorMessage
from .Log import Log
from .handlers.ShellHandler import ShellHandler


class SingletonMeta(type):
    """This pattern restricts the instantiation of a class to one object. 
    
    It is a type of creational pattern and involves only one class to create methods and specified objects. It provides a global point of access to the instance created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(object, metaclass=SingletonMeta):
    """A class used to store a set of variables and parameters across all modules.

    Attributes:
        _init_env {dictionary} -- Output of the os.environ.copy method.
        _env {dictionary} -- All the environment variables for the current execution of the program.

        _root_workdir {string} -- Absolute path of the root working directory.
        _exec_working_dir {string} -- Absolute path of the working directory where new working directories are created and files processed.
        _current_workdir {string} -- Absolute path of the current working directory.

        _last_section {string} -- Name of the last section being executed, whether it succeeds or 
            fails.

        _filters {dictionary} -- Filter names and their respective values.

        _report_file_path {string} -- Absolute path of the report file of the compilation.

        _grouping {boolean} -- Flag used to group all working directories into one group directory.
        _skip {boolean} -- Flag used to skip source files if not found or not.

        _tag {string} -- Keyword to tag working directories and report file.
        
        _time_stamp {string} -- Datetime respecting _%Y%m%d_%H%M%S format for working directories and 
            report identification purposes.

        _init_pwd {string} -- Absolute path of the initial directory where the command has been executed. 

    Methods:
        __init__() -- Initializes all attributes of the class.
        add_env_variable(key, value) -- Adds a variable to the environment.
        add_filter(key, value) -- Adds a filter function to the list of filters.
        get_filter_function(key) -- Retrieves the expression of the filter function from the Context.

        clear() -- Clears context after each file processing.
        clear_all() -- Clears context completely at the end of the program execution.
    """

    def __init__(self):
        """Initializes all attributes of the class.
        """
        # Environment
        self._init_env = os.environ.copy()
        self._env = self._init_env

        # Directories
        self._root_workdir = ''
        self._exec_working_dir = ''
        self._current_workdir = ''

        # Profile sections
        self._last_section = ''

        # Filter variables
        self._filters = {}

        # Report
        self._report_file_path = ''

        # Argument flags
        self._grouping = False
        self._skip = False

        # Tag
        self._tag = ''

        # Timestamp
        self._time_stamp = datetime.datetime.now()

        # Other
        self._init_pwd = os.getcwd()

    @property
    def env(self):
        """Getter method for the attribute _env.
        """
        return self._env

    @property
    def root_workdir(self):
        """Getter method for the attribute _root_workdir.
        """
        return self._root_workdir

    @root_workdir.setter
    def root_workdir(self, working_dir):
        """Setter method for the attribute _root_workdir.
        """
        self._root_workdir = os.path.expandvars(working_dir)

    @property
    def exec_working_dir(self):
        """Getter method for the attribute _exec_working_dir.
        """
        return self._exec_working_dir

    @exec_working_dir.setter
    def exec_working_dir(self, working_dir):
        """Setter method for the attribute _exec_working_dir.
        """
        self._exec_working_dir = os.path.expandvars(working_dir)

    @property
    def current_workdir(self):
        """Getter method for the attribute _current_workdir.
        """
        return self._current_workdir

    @current_workdir.setter
    def current_workdir(self, working_dir):
        """Setter method for the attribute _current_workdir.
        """
        self._current_workdir = working_dir

    @property
    def last_section(self):
        """Getter method for the attribute _last_section.
        """
        return self._last_section

    @last_section.setter
    def last_section(self, section):
        """Setter method for the attribute _last_section.
        """
        self._last_section = section

    @property
    def filters(self):
        """Getter method for the attribute _filters.
        """
        return self._filters

    @property
    def report_file_path(self):
        """Getter method for the attribute _report_file_path.
        """
        return self._report_file_path

    @report_file_path.setter
    def report_file_path(self, file_path):
        """Setter method for the attribute _report_file_path.
        """
        self._report_file_path = file_path

    @property
    def grouping(self):
        """Getter method for the attribute _grouping.
        """
        return self._grouping

    @grouping.setter
    def grouping(self, grouping):
        """Setter method for the attribute _grouping.
        """
        if grouping is not None:
            self._grouping = grouping

    @property
    def skip(self):
        """Getter method for the attribute _skip.
        """
        return self._skip

    @skip.setter
    def skip(self, skip):
        """Setter method for the attribute _skip.
        """
        if skip is not None:
            self._skip = skip

    @property
    def tag(self):
        """Getter method for the attribute _tag.
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Setter method for the attribute _tag.
        """
        if tag is None:
            self._tag, _, _ = ShellHandler().execute_command(
                'logname', 'tag', self._env)
            self._tag = '_' + self._tag.replace('\n', '')
        else:
            self._tag = '_' + tag

    @property
    def time_stamp(self):
        """Getter method for the attribute _time_stamp.
        """
        return self._time_stamp.strftime('_%Y%m%d_%H%M%S')

    @time_stamp.setter
    def time_stamp(self, update):
        """Setter method for the attribute _time_stamp.

        Arguments:
            update {integer} -- Number of seconds needed to update the time stamp.
        """
        time_update = datetime.timedelta(seconds=update)
        self._time_stamp += time_update

    def add_env_variable(self, key, value):
        """Adds a variable to the environment.

        Arguments:
            key {string} -- Name of the environment variable.
            value {string} -- Value of the environment variable.
        """
        if not value.startswith('$(') and not value.startswith('`'):
            self._env[key[1:]] = os.path.expandvars(value)
        else:
            if value.startswith('$(') and value.endswith(')'):
                value = value[2:-1]
            elif value.startswith('`') and value.endswith('`'):
                value = value[1:-1]
            out, _, _ = ShellHandler().execute_command(value, 'env_variable',
                                                       self._env)
            value = out.rstrip()
            # Write to env dictionary without dollar sign
            self._env[key[1:]] = value

        os.environ.update(self._env)

    def add_filter(self, key, value):
        """Adds a filter function to the list of filters.

        Arguments:
            key {string} -- Name of the filter function.
            value {string} -- Expression of the filter function.
        """
        # Remove question mark from filter function name
        self._filters[key[1:]] = value

    def get_filter_function(self, key):
        """Retrieves the expression of the filter function from the Context.

        Arguments:
            key {string} -- Name of the filter function.

        Returns:
            string -- Expression of the filter function.

        Raises:
            KeyError -- Exception raised if a filter function is used in the profile before being defined.
        """
        try:
            if key == '':
                filter_function = ''
            else:
                filter_function = self.filters[key]
        except KeyError:
            Log().logger.error(ErrorMessage.KEY_FILTER.value % key)
            self.clear_all()
            sys.exit(-1)

        return filter_function

    def clear(self, profile):
        """Clears context after each file processing.

        Arguments:
            profile {Profile object} -- From the Profile module.
        """
        self._env = self._init_env
        os.environ.update(self._init_env)

        self._current_workdir = ''

        self._filters.clear()
        for key in profile.sections_complete.keys():
            profile.sections_complete[key] = False

        os.chdir(self._init_pwd)

    def clear_all(self):
        """Clears context completely at the end of the program execution.
        """
        self._root_workdir = ''
        self._exec_working_dir = ''

        self._filters = {}
        self._last_section = ''
        self._report_file_path = ''
        self._tag = ''
        self._time_stamp = datetime.datetime.now()

        os.chdir(self._init_pwd)
