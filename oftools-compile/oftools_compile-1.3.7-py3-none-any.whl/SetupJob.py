#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to run the job for the profile setup section.

Typical usage example:
  job = SetupJob()
  job.run(file_path_in)
"""

# Generic/Built-in modules
import datetime
import os

# Third-party modules

# Owned modules
from .Context import Context
from .enums.ErrorEnum import ErrorMessage
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .handlers.ShellHandler import ShellHandler
from .Job import Job
from .Log import Log


class SetupJob(Job):
    """A class used to perform all the setup section steps.

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze() -- Analyzes prerequisites before running the job for the section.
        _process_section() -- Reads the section line by line to execute the corresponding methods.
        _init_current_workdir() -- Initializes the working directory for the file being currently 
            processed.
        _init_file() -- Copies the file to the working directory.
        _init_log_file() -- Initializes the log file for the file being currently processed.
        _process_backup(value) -- Cleans the root working directory from old compilation directories based on the number of backups to be kept.
        _process_housekeeping(value) -- Cleans the root working directory from compilation directories older than the input number of days.
        run(file_path_in) -- Performs all the steps for the setup section of the profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates the following statements:
            - is the section already complete, based on the name without the filter function
            - is the section mandatory, list of sections in the setup section
            - is the filter of the section True or False, if there is one

        Returns:
            integer - Return code of the analysis.
        """
        filter_function = Context().get_filter_function(self._filter)

        if self._profile.is_section_complete(self._section_name):
            rc = 1
        elif self._profile.is_section_mandatory(self._section_name):
            rc = 0
        elif ShellHandler().evaluate_filter(filter_function, self._filter,
                                            self._section_name,
                                            Context().env) in (True, None):
            rc = 0
        else:
            rc = 1

        return rc

    def _process_section(self):
        """Reads the section line by line to execute the corresponding methods.

        For the setup section, it mainly analyzes the workdir options, but also processes options such as mandatory, backup and housekeeping. And as any other 
        section, it looks for environment and filter variables.

        Returns:
            integer -- Return code of the method.
        """
        rc = 0
        Log().logger.debug(LogMessage.START_SECTION.value %
                           (self._section_name, self._file_path_in))

        for key, value in self._profile.data[self._section_name].items():
            if key == 'workdir':
                self._init_current_workdir()
                rc = self._init_file()
                self._init_log_file()
            elif key == 'mandatory':
                continue
            elif key == 'housekeeping':
                rc = self._process_housekeeping(value)
            elif key == 'backup':
                if self._profile.data.has_option('setup',
                                                 'housekeeping') is False:
                    rc = self._process_backup(value)
                else:
                    continue
            else:
                rc = self._process_option(key, value)

            if rc < 0:
                Log().logger.error(LogMessage.ABORT_SECTION.value %
                                   (self._section_name, key))
                break

        if rc in (0,1):
            Log().logger.debug(LogMessage.END_SECTION.value %
                               (self._section_name, self._file_name_out))
            self._profile.section_completed(self._section_no_filter)

        return rc

    def _init_current_workdir(self):
        """Initializes the working directory for the file being currently processed.
        """
        Log().logger.debug(LogMessage.START_WORKING_DIRECTORY.value %
                           self._section_name)

        while True:
            current_workdir = os.path.join(
                Context().exec_working_dir,
                self._file_name_in + Context().tag + Context().time_stamp)

            rc = FileHandler().create_directory(current_workdir)
            if rc == 1:
                Log().logger.debug(LogMessage.ADD_TIME_TO_TIME_STAMP.value %
                                   (self._section_name, current_workdir))
                Context().time_stamp = 1
            else:
                # Update Context and change directory to current working directory
                Context().current_workdir = current_workdir
                os.chdir(current_workdir)
                break

        Log().logger.debug(LogMessage.END_WORKING_DIRECTORY.value %
                           self._section_name)

    def _init_file(self):
        """Copies the file to the current working directory.

        Returns:
            integer -- Return code of the method.
        """
        Log().logger.debug(LogMessage.START_SETUP_FILE.value %
                           self._section_name)

        current_workdir = Context().current_workdir
        rc = FileHandler().copy_file(self._file_path_in, current_workdir)

        Log().logger.debug(LogMessage.END_SETUP_FILE.value % self._section_name)

        return rc

    def _init_log_file(self):
        """Initializes the log file for the file being currently processed.

        It first opens the file, then write the header and the setup section steps to the file.
        """
        Log().logger.debug(LogMessage.START_LOG_FILE.value % self._section_name)

        current_workdir = Context().current_workdir
        Log().open_file(os.path.join(current_workdir, 'oftools_compile.log'))
        header = '================================================================================'
        header = header[0:8] + ' ' + self._file_name_in + ' ' + header[
            len(self._file_name_in) + 8:]

        Log().logger.info(header)
        Log().logger.info(LogMessage.MKDIR_COMMAND.value %
                          (self._section_name, current_workdir))
        Log().logger.info(LogMessage.CD_COMMAND.value %
                          (self._section_name, current_workdir))
        Log().logger.info(
            LogMessage.CP_COMMAND.value %
            (self._section_name, self._file_path_in, current_workdir))

        Log().logger.debug(LogMessage.END_LOG_FILE.value % self._section_name)

    def _process_backup(self, value):
        """Cleans the root working directory from old compilation directories based on the number of backups to be kept.

        Arguments:
            value {string} -- Value of the backup option, this is an integer.

        Returns:
            integer -- Return code of the method.

        Raises:
            ValueError -- Exception raised if the input value cannot be converted from string to integer.
        """
        Log().logger.debug(LogMessage.START_CLEANING.value %
                           (self._section_name, 'backup'))

        try:
            if value != '':
                value = int(value)
                backup_paths = FileHandler().get_duplicates(
                    Context().root_workdir, self._file_name_in)

                if len(backup_paths) > value:
                    creation_times = FileHandler().get_modified_times(
                        backup_paths)
                    # Sorting the backup_paths list based on a sorting of the creation_times list
                    backup_paths = [
                        path
                        for _, path in sorted(zip(creation_times, backup_paths))
                    ]

                    while len(backup_paths) > value:
                        backup = backup_paths[0]
                        backup_paths.pop(0)
                        FileHandler().delete_directory(backup)
                else:
                    Log().logger.debug(LogMessage.VALUE_BELOW_THRESHOLD.value %
                                       (self._section_name,
                                        len(backup_paths) - 1, value, 'backup'))

                Log().logger.debug(LogMessage.END_CLEANING.value %
                                   (self._section_name, 'backup'))
                rc = 0
            else:
                Log().logger.warning(LogMessage.VALUE_EMPTY.value %
                                     ('setup', 'backup'))
                rc = 1
        except ValueError:
            Log().logger.error(ErrorMessage.VALUE_BACKUP.value % value)
            rc = -1

        return rc

    def _process_housekeeping(self, value):
        """Cleans the root working directory from compilation directories older than the input number of days.

        Arguments:
            value {string} -- Value of the housekeeping option, this must be a number of days.

        Returns:
            integer -- Return code of the method.

        Raises:
            ValueError -- Exception raised if part of the input value cannot be converted from string to integer.
        """
        Log().logger.debug(LogMessage.START_CLEANING.value %
                           (self._section_name, 'housekeeping'))

        try:
            if value != '':
                if self._profile.data.has_option('setup', 'backup'):
                    if value[-1] == 'd':

                        days = int(value[:-1])
                        threshold = datetime.datetime.today(
                        ) - datetime.timedelta(days=int(days))
                        backup_paths = FileHandler().get_duplicates(
                            Context().root_workdir, self._file_name_in)
                        backup_value = int(
                            self._profile.data.get('setup', 'backup'))

                        if len(backup_paths) > backup_value:
                            creation_times = FileHandler().get_modified_times(
                                backup_paths)
                            creation_times.sort()
                            # Sorting the backup_paths list based on a sorting on the creation_times list
                            backup_paths = [
                                path for _, path in sorted(
                                    zip(creation_times, backup_paths))
                            ]

                            number_of_backups = len(backup_paths)
                            for i, backup in enumerate(backup_paths):
                                backup_modified_date = datetime.datetime.fromtimestamp(
                                    creation_times[i])

                                if backup_modified_date < threshold:
                                    number_of_backups -= 1
                                    FileHandler().delete_directory(backup)

                                if number_of_backups == backup_value:
                                    break

                            if number_of_backups == len(backup_paths):
                                Log().logger.info(
                                    LogMessage.NOT_OLD_ENOUGH.value %
                                    (self._section_name, 'housekeeping'))
                            else:
                                Log().logger.debug(
                                    LogMessage.END_CLEANING.value %
                                    (self._section_name, 'housekeeping'))
                        else:
                            Log().logger.debug(
                                LogMessage.VALUE_BELOW_THRESHOLD.value %
                                (self._section_name, len(backup_paths) - 1,
                                 backup_value, 'housekeeping'))
                        rc = 0
                    else:
                        raise ValueError()
                else:
                    raise SystemError()
            else:
                Log().logger.warning(LogMessage.VALUE_EMPTY.value %
                                     ('setup', 'housekeeping'))
                rc = 1
        except SystemError:
            Log().logger.error(ErrorMessage.MISSING_BACKUP.value)
            rc = -1
        except ValueError:
            Log().logger.error(ErrorMessage.VALUE_HOUSEKEEPING.value % value)
            rc = -1

        return rc

    def run(self, file_path_in):
        """Performs all the steps for the setup section of the profile.

        Returns:
            integer -- Return code of the setup section.
        """
        self._initialize_file_variables(file_path_in)
        self._update_context()

        rc = self._analyze()
        if rc != 0:
            self._file_name_out = file_path_in
            return rc

        rc = self._process_section()
        if rc not in (0,1):
            self._file_name_out = file_path_in

        return rc
