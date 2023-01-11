#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Common module for all Job modules in this program.

Typical usage example:
  job = Job(profile, setup)
  job.run()
  file_name_out = job.file_name_out
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .enums.ErrorEnum import ErrorMessage
from .Log import Log


class Job(object):
    """A class used to store common values and execute common methods to all type of jobs.

    Attributes:
        _section_name {string} -- Name of the section in the profile.
        _profile {dictionary} -- From the Profile module, the data attribute.
        _section_name_no_filter {string} -- Name of the section without the filter if there is one.
        _filter {string} -- Name of the filter extracted from the name of the section if there is one.
        _filter_function {string} -- Corresponding function to the filter, empty if there is no filter for the section.
        _file_path_in {string} -- Absolute path of the input file, which could also be just the file name, depending on the type of job.
        _file_name_in {string} -- Job input file name.
        _file_name_out {string} -- Job output file name.

    Methods:
        __init__(profile section_name) -- Initializes the class with all the attributes.
        _initialize_file_variables(file_path_in) -- Detects if the source provided is a file or a 
            directory, and properly retrieve the name of the file to initialize class attributes.
        _update_context() -- Updates Context with name of files being manipulated in this job execution.
        _process_option(key, value) -- Processes option like environment variable or filter function.
    """

    def __init__(self, profile, section_name):
        """Initializes the class with all the attributes.
        """
        self._profile = profile
        self._section_name = section_name
        self._section_no_filter = profile.sections_no_filter[section_name]
        self._filter = profile.filters[section_name]

        self._file_path_in = ''
        self._file_name_in = ''
        self._file_name_out = ''

    @property
    def file_name_out(self):
        """Getter method for the attribute _file_name_out.
        """
        return self._file_name_out

    def _initialize_file_variables(self, file_path_in):
        """Detects if the source provided is a file or a directory, and properly retrieve the name of the file to update class attributes.

        Arguments:
            file_path_in {string} -- Path of the input file.

        Raises:
            IndexError -- Exception raised if there is no '/' symbol in the file path, which means only 
                the file name has been provided and not the absolute file path.
        """
        # Initialize file_path_in
        self._file_path_in = file_path_in
        # Initializes file_name_in
        try:
            self._file_name_in = self._file_path_in.rsplit('/', 1)[1]
        except IndexError:
            self._file_name_in = self._file_path_in
        # Initialize file_name_out
        if 'setup' in self._section_name or 'deploy' in self._section_name:
            self._file_name_out = self._file_name_in
        else:
            filename = self._file_name_in.rsplit('.', 1)[0]
            extension = self._section_no_filter
            self._file_name_out = filename + '.' + extension

        # Handle cases where the file name starts with a special character
        if self._file_name_in.startswith(('$', '#', '@')):
            self._file_name_in = '\\' + self._file_name_in
            self._file_name_out = '\\' + self._file_name_out

    def _update_context(self):
        """Updates Context with the name of files being manipulated in this job execution.
        """
        base_file_name = self._file_name_out.rsplit('.', 1)[0]

        Context().add_env_variable('$OF_COMPILE_IN', self._file_name_in)
        Context().add_env_variable('$OF_COMPILE_OUT', self._file_name_out)
        Context().add_env_variable('$OF_COMPILE_BASE', base_file_name)

        Context().last_section = self._section_name

    def _process_option(self, key, value):
        """Processes option like an environment variable or a filter function.

        The return code of this method is either 0 or 1, and not negative since it is just a warning 
        and not an error worth stopping the program execution.

        Arguments:
            key {string} -- Option name.
            value {string} -- Option value.

        Returns:
            integer -- Return code of the method.

        Raises:
            Warning -- Exception raised if the input option (key and value pair) is not supported.
        """
        try:
            if key.startswith('$'):
                Context().add_env_variable(key, value)
                if key == '$OF_COMPILE_IN':
                    self._file_name_in = Context().env['OF_COMPILE_IN']
                elif key == '$OF_COMPILE_OUT':
                    self._file_name_out = Context().env['OF_COMPILE_OUT']
                rc = 0
            elif key.startswith('?'):
                Context().add_filter(key, value)
                rc = 0
            else:
                raise Warning()
        except Warning:
            Log().logger.warning(ErrorMessage.OPTION_NOT_SUPPORTED.value %
                                 (self._section_name, key))
            rc = 1

        return rc
