#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to handle all profile related tasks.

Typical usage example:
  profile = Profile(profile_path)
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules

# Owned modules
from .Context import Context
from .enums.ErrorEnum import ErrorMessage
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Profile(object):
    """A class used to initialize the Profile object and analyze it.

    Attributes:
        _data {ConfigParser} -- Data extracted from the profile.
        _sections {dictionary} -- List of the section names in the profile.
        _filters {dictionary} -- List of the filter functions.
        _sections_complete {dictionary} -- List of the section names and their completion status.
        _sections_mandatory_ {list} -- Sections that are listed as mandatory.
        _sections_no_filter {dictionary} -- List of the section names without filters if any.

    Methods:
        __init__(profile_path) -- Initializes the class with all the attributes.
        _split_section_and_filter(section) -- Separates the section name from the filter function if any.
        _analyze() -- Analyzes the sections of the profile.
        _analyze_setup(section) -- Analyzes the setup section of the profile.
        _analyze_mandatory(section) -- Analyzes the mandatory option in the setup section.
        _analyze_compile(section) -- Analyzes any compile section of the profile.
        _analyze_deploy(section) -- Analyzes the deploy section of the profile.
        
        is_section_mandatory(section_name_no_filter) -- Checks if given section is mandatory or not.
        is_section_complete(section_name_no_filter, skip=True) -- Checks if given section is already 
            complete.
        section_completed(section_name_no_filter) -- Changes the status of the given section to complete.
    """

    def __init__(self, profile_path):
        """Initializes the class with all the attributes.
        """
        self._data = FileHandler().read_file(profile_path)
        self._sections = self._data.sections()
        Log().logger.debug(LogMessage.PROFILE_SECTIONS.value % self._sections)

        self._filters = {}

        self._sections_complete = {}
        self._sections_mandatory = []
        self._sections_no_filter = {}

        self._analyze()

    @property
    def data(self):
        """Getter method for the attribute _data.
        """
        return self._data

    @property
    def sections(self):
        """Getter method for the attribute _sections.
        """
        return self._sections

    @property
    def sections_no_filter(self):
        """Getter method for the attribute _sections_no_filter.
        """
        return self._sections_no_filter

    @property
    def filters(self):
        """Getter method for the attribute _filters.
        """
        return self._filters

    @property
    def sections_complete(self):
        """Getter method for the attribute _complete_sections.
        """
        return self._sections_complete

    def _split_section_and_filter(self, section):
        """Separates the section name from the filter function if any.

        It also initializes the complete_sections dictionary.

        Arguments:
            section {string} -- Full name of the setup section.
        """
        # Spliting section name and filter function
        if '?' in section:
            section_no_filter = section.split('?')[0]
            filter_name = section.split('?')[1]
        else:
            section_no_filter = section
            filter_name = ''

        # Adding new entry in both dictionaries
        self._filters[section] = filter_name
        self._sections_no_filter[section] = section_no_filter

        # Initializing complete sections dictionary
        self._sections_complete[section_no_filter] = False

    def _analyze(self):
        """Analyzes the sections of the profile.

        Makes sure that there is a setup section, and analyzes individually each section depending on its type.

        Raises:
            SystemError -- Exception raised if the setup section is missing in the profile.
        """
        try:
            if 'setup' not in self._sections:
                raise SystemError()

            for section in self._sections:
                self._split_section_and_filter(section)

                # Detailed analysis of the sections
                if section.startswith('setup'):
                    self._analyze_setup(section)
                elif section.startswith('deploy'):
                    self._analyze_deploy(section)
                else:
                    self._analyze_compile(section)

            self._analyze_mandatory()

        except SystemError:
            Log().logger.critical(ErrorMessage.SYSTEM_MISSING_SETUP.value)
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

    def _analyze_setup(self, section):
        """Analyzes the setup section of the profile.

        Arguments:
            section {string} -- Full name of the setup section.

        Raises:
            SystemError -- Exception raised if the workdir option is missing from the setup section.
            ValueError -- Exception raised if the workdir option is empty.
            OSError -- Exception raised if there is an issue with the workdir option in the setup section.
        """
        try:
            # Analyze working directory option
            if self._data.has_option(section, 'workdir'):
                working_directory = self._data.get(section, 'workdir')

                if working_directory != '':
                    if FileHandler().is_a_directory(
                            working_directory) and FileHandler(
                            ).check_write_access(working_directory):

                        # Set group directory as working directory for the execution if grouping option used
                        if Context().grouping:
                            group_directory = os.path.join(
                                working_directory,
                                'group' + Context().tag + Context().time_stamp)
                            FileHandler().create_directory(
                                group_directory, 'group')
                            Context().exec_working_dir = group_directory
                        else:
                            Context().exec_working_dir = working_directory

                        # Save root working directory path to Context
                        Context().root_workdir = working_directory

                        # Create report directory if it does not already exist
                        report_directory = os.path.join(working_directory,
                                                        'report')
                        FileHandler().create_directory(report_directory)
                    else:
                        raise OSError()
                else:
                    raise ValueError()
            else:
                raise SystemError()
        except SystemError:
            Log().logger.critical(ErrorMessage.SYSTEM_MISSING_OPTION.value %
                                  (section, 'workdir'))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)
        except ValueError:
            Log().logger.critical(ErrorMessage.VALUE_EMPTY.value %
                                  (section, 'workdir'))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)
        except OSError:
            Log().logger.critical(ErrorMessage.OS_ISSUE_WORKDIR.value % section)
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

    def _analyze_mandatory(self):
        """Analyzes the mandatory option in the setup section.

        Arguments:
            section {string} -- Full name of the setup section.

        Raises:
            ValueError -- Exception raised if the mandatory option is empty.
            Warning -- Exception raised if the mandatory option value contains a section that does not exist in the profile.
        """
        # Analyze mandatory option
        if self._data.has_option('setup', 'mandatory'):
            value = self._data.get('setup', 'mandatory')

            if value != '':
                # Split the mandatory sections in a list
                value = value.split(':')
                # Check that the mandatory section actually exist in the profile
                for mandatory_section in value:
                    try:
                        if mandatory_section in self._sections_no_filter.values(
                        ):
                            Log().logger.info(LogMessage.MANDATORY_ADD.value %
                                              mandatory_section)
                            self._sections_mandatory.append(mandatory_section)
                        else:
                            if mandatory_section in self._sections and '?' in mandatory_section:
                                Log().logger.info(
                                    LogMessage.MANDATORY_FILTER.value %
                                    mandatory_section)
                            else:
                                Log().logger.info(
                                    LogMessage.MANDATORY_NOT_FOUND.value %
                                    mandatory_section)
                            raise Warning()
                    except Warning:
                        Log().logger.warning(
                            ErrorMessage.WARNING_MANDATORY.value %
                            mandatory_section)
                Log().logger.debug(LogMessage.MANDATORY_SECTIONS.value %
                                   self._sections_mandatory)
            else:
                Log().logger.warning(LogMessage.VALUE_EMPTY.value %
                                     ('setup', 'mandatory'))

    def _analyze_compile(self, section):
        """Analyzes any compile section of the profile.

        Makes sure that the option 'args' or 'option' is in the section.

        Arguments:
            section {string} -- Full name of the compile section.

        Raises:
            SystemError -- An error occurs if the given compile section does not contain an 'args' or 
                'option' option.
            ValueError -- Exception raised if the 'args' or 'option' option is empty.
        """
        try:
            if self._data.has_option(section, 'args'):
                args = self._data.get(section, 'args')
                if args == '':
                    raise ValueError()
            elif self._data.has_option(section, 'option'):
                option = self._data.get(section, 'option')
                if option == '':
                    raise ValueError()
            else:
                raise SystemError()
        except SystemError:
            Log().logger.critical(ErrorMessage.SYSTEM_MISSING_OPTION.value %
                                  (section, 'args'))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)
        except ValueError:
            Log().logger.critical(ErrorMessage.VALUE_EMPTY.value %
                                  (section, 'args or option'))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

    def _analyze_deploy(self, section):
        """Analyzes the deploy section of the profile.

        Makes sure that the option 'file' is in the section.

        Arguments:
            section {string} -- Full name of the deploy section.

        Raises:
            SystemError -- An error occurs if the deploy section does not contain a 'file' option.
            ValueError -- Exception raised if the file option is empty.
        """
        try:
            if self._data.has_option(section, 'file'):
                file_option = self._data.get(section, 'file')
                if file_option == '':
                    raise ValueError()
            else:
                raise SystemError()
        except SystemError:
            Log().logger.critical(ErrorMessage.SYSTEM_MISSING_OPTION.value %
                                  (section, 'file'))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)
        except ValueError:
            Log().logger.critical(ErrorMessage.VALUE_EMPTY.value %
                                  (section, 'file'))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

    def is_section_mandatory(self, section):
        """Checks if given section is mandatory or not.

        Arguments:
            section {string} -- Name of the section.

        Returns:
            boolean -- Status of the section, if it is mandatory or not.
        """
        section_no_filter = self._sections_no_filter[section]

        if section_no_filter in self._sections_mandatory:
            Log().logger.debug(LogMessage.SECTION_MANDATORY.value % section)
            status = True
        else:
            status = False

        return status

    def is_section_complete(self, section, skip=True):
        """Checks if given section is already complete.

        Arguments:
            section {string} -- Name of the section.
            skip {boolean} -- Value of the skip flag.

        Returns:
            boolean -- Status of the section, if it is complete or not.
        """
        section_no_filter = self.sections_no_filter[section]
        status = self.sections_complete[section_no_filter]

        if status and skip is True:
            Log().logger.debug(LogMessage.SECTION_COMPLETE.value % section)

        return status

    def section_completed(self, section_no_filter):
        """Changes the status of the given section to complete.

        Arguments:
            section_no_filter {string} -- Name of the section without filter.
        """
        self.sections_complete[section_no_filter] = True
