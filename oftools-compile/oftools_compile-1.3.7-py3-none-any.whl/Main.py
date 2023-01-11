#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main module of OpenFrame Tools Compile.
"""
# Generic/Built-in modules
import argparse
import os
import signal
import sys
import traceback
import time
# import logging

# Third-party modules

# Owned modules
from . import __version__
from .Context import Context
from .enums.ErrorEnum import ErrorMessage
from .enums.LogEnum import LogMessage
from .Grouping import Grouping
from .handlers.FileHandler import FileHandler
from .JobFactory import JobFactory
from .Log import Log
from .Profile import Profile
from .Report import Report
from .Source import Source

# Global variables
INTERRUPT = False


def main():
    return Main().run()


class Main(object):
    """Main class containing the methods for parsing the command arguments and running OpenFrame Tools 
    Compile.

    Methods:
        _parse_args() -- Parses command-line options.
        _create_jobs(profile) -- Creates job depending on the section of the profile.
        _end_processing(mode, rc, clear, report, file_path, elapsed_time, profile) -- Common method to end file processing or entire program.
        run() -- Performs all the steps to run compilation for all sources using the appropriate profile.
    """

    @staticmethod
    def _parse_args():
        """Parses command-line options.

        The program defines what arguments it requires, and argparse will figure out how to parse those 
        out of sys.argv. The argparse module also automatically generates help, usage messages and 
        issues errors when users give the program invalid arguments.

        Returns:
            args {ArgumentParser} -- List of all arguments of the tool with their corresponding value.

        Raises:
            argparse.ArgumentError -- Exception raised if there is an issue parsing the command arguments.
            SystemError -- Exception raised if the numbers of profile and source are not 
                matching.           
        """
        parser = argparse.ArgumentParser(
            add_help=False,
            description='OpenFrame Tools Compile',
            formatter_class=argparse.RawTextHelpFormatter)

        parser._action_groups.pop()
        required = parser.add_argument_group('Required arguments')
        optional = parser.add_argument_group('Optional arguments')
        others = parser.add_argument_group('Help & version')

        # Required arguments
        required.add_argument(
            '-p',
            '--profile',
            action='append',
            dest='profile_list',
            help=
            'profile name, contains the description of the compilation target',
            metavar='FILENAME',
            required=True,
            type=str)

        required.add_argument(
            '-s',
            '--source',
            action='append',
            dest='source_list',
            help=
            'source name, currently supported:\n- file or a directory\n- colon-separated list of files of directories\n- text file containing a list of files or directories',
            metavar='SOURCE',
            required=True,
            type=str)

        # Optional arguments
        optional.add_argument(
            '-c',
            '--clear',
            action='store_true',
            dest='clear',
            help='clear all the files generated during compilation',
            required=False)

        optional.add_argument(
            '-g',
            '--grouping',
            action='store_true',
            dest='grouping',
            help=
            'put all the compilation directories in a single one and aggregate all the logs',
            required=False)

        optional.add_argument(
            '-l',
            '--log-level',
            action='store',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            default='INFO',
            dest='log_level',
            help=
            'set log level, potential values:\n- DEBUG\n- INFO (default)\n- WARNING\n- ERROR\n- CRITICAL',
            metavar='LEVEL',
            required=False,
            type=str)

        optional.add_argument('--skip',
                              action='store_true',
                              dest='skip',
                              help='skip source files if not found',
                              required=False)

        optional.add_argument(
            '-t',
            '--tag',
            action='store',
            dest='tag',
            help=
            'add a tag to the name of the report file and the compilation directory',
            metavar='TAG',
            required=False,
            type=str)

        # Other arguments
        others.add_argument('-h',
                            '--help',
                            action='help',
                            help='show this help message and exit')

        others.add_argument(
            '-v',
            '--version',
            action='version',
            help='show this version message and exit',
            version='%(prog)s {version}'.format(version=__version__))

        # Deprecated arguments
        optional.add_argument('-r',
                              '--recursive',
                              action='store',
                              help=argparse.SUPPRESS)

        optional.add_argument('-e',
                              '--export',
                              action='store',
                              help=argparse.SUPPRESS)

        # Do the parsing
        if len(sys.argv) == 1:
            parser.print_help(sys.stdout)
            sys.exit(0)
        try:
            args = parser.parse_args()
        except argparse.ArgumentError as error:
            Log().logger.critical(ErrorMessage.ARGUMENT.value % error)
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

        # Analyze profiles, making sure a file with .prof extension is specified for each profile
        for profile in args.profile_list:
            is_valid_ext = FileHandler().check_extension(profile, 'prof')
            if is_valid_ext is False:
                Log().logger.critical(ErrorMessage.ABORT.value)
                sys.exit(-1)

        # Analyze number of profiles and sources provided
        try:
            if len(args.profile_list) != len(args.source_list):
                raise SystemError()
        except SystemError:
            Log().logger.critical(
                ErrorMessage.SYSTEM_NUMBER.value %
                (len(args.profile_list), len(args.source_list)))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

        return args

    @staticmethod
    def _signal_handler(signum, frame):
        """
        """
        global INTERRUPT
        INTERRUPT = True
        raise KeyboardInterrupt()

    @staticmethod
    def _create_jobs(profile, clear):
        """Creates job depending on the section of the profile.

        Running the method 'sections' on the profile which is a ConfigParser object allow us to create 
        a list of strings, the name of each section of the profile. And then a call to the method 
        create of the JobFactory module generate the corresponding job.

        Args:
            profile {ConfigParser} -- Compilation profile specified for the current source.
            clear {boolean} -- Value of the argument clear from the CLI.

        Returns:
            list[Job] -- list of Job objects.

        Raises:
            #TODO Complete docstrings, maybe change the behavior to print traceback only with DEBUG as log level
        """
        jobs = []
        job_factory = JobFactory(profile)

        try:
            for section_name in profile.sections:
                job = job_factory.create(section_name)
                jobs.append(job)

            if clear is True:
                job = job_factory.create('clear')
                jobs.append(job)
        except:
            traceback.print_exc()
            Log().logger.critical(ErrorMessage.JOB.value)
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)

        return jobs

    @staticmethod
    def _end_processing(
        mode,
        rc,
        clear=None,
        report=None,
        file_path=None,
        elapsed_time=None,
        profile=None,
    ):
        """Common method to end file processing or entire program.

        Modes:
            0: end the file processing normally.
            1: end the file processing when user press Ctrl + C.
            2: end the entire program normally.
            3: end the entire program when the user press Ctrl + \\.

        Arguments:
            mode {integer} -- Ending mode for the program.
            rc {integer} -- Return code of the file processing.
            clear {boolean} -- Value of the argument clear from the CLI.
            report {Report}
            file_path {string} -- Absolute path to the source file.
            elapsed_time {integer} -- Elapsed processing time.
            profile {Profile}
        """
        if mode == 1:
            Log().logger.critical(
                ErrorMessage.KEYBOARD_ABORT_COMPILATION.value % file_path)
        elif mode == 3:
            if INTERRUPT is True:
                Log().logger.debug(LogMessage.SIGQUIT.value)
            else:
                Log().logger.debug(LogMessage.SIGINT.value)
            Log().logger.critical(ErrorMessage.KEYBOARD_INTERRUPT.value)

        if mode in (0, 1):
            if clear is not True:
                Log().logger.info(LogMessage.WORKING_DIRECTORY.value %
                                  Context().current_workdir)
            report.add_entry(file_path, rc, elapsed_time)
            Context().clear(profile)
            Log().close_file()

        if mode in (2, 3):
            Log().logger.debug(LogMessage.RETURN_CODE.value % rc)
            Context().clear_all()
            Log().close_stream()

    def run(self):
        """Performs all the steps to run compilation for all sources using the appropriate profile.

        Returns:
            integer -- Return code of the program.
        """
        # This is normal if there is an error using this with Windows as the OS, SIGQUIT only exist in Unix
        signal.signal(signal.SIGQUIT, self._signal_handler)

        rc = 0
        # For testing purposes. allow to remove logs when executing coverage
        # logging.disable(logging.CRITICAL)
        Log().open_stream()

        # Parse command-line options
        args = self._parse_args()

        # Set log level and log oftools_compile command as DEBUG
        Log().set_level(args.log_level)
        Log().logger.debug(' '.join((arg for arg in sys.argv)))

        # Initialize variables for program execution
        Context().grouping = args.grouping
        Context().skip = args.skip
        Context().tag = args.tag
        report = Report(args.clear)
        profile_dict = {}

        try:
            for i in range(len(args.source_list)):

                # Profile processing
                profile_path = os.path.expandvars(args.profile_list[i])
                Log().logger.debug(LogMessage.PROFILE_PATH.value % profile_path)
                if profile_path not in profile_dict.keys():
                    profile = Profile(profile_path)
                    profile_dict[profile_path] = profile
                else:
                    Log().logger.debug(LogMessage.PROFILE_REUSE.value %
                                       profile_path)
                    profile = profile_dict[profile_path]

                # Source processing
                source_path = os.path.expandvars(args.source_list[i])
                Log().logger.debug(LogMessage.SOURCE_PATH.value % source_path)
                source = Source(args.source_list[i])

                # Create jobs
                jobs = self._create_jobs(profile, args.clear)

                for file_path in source.file_paths:
                    try:
                        # Initialization of variables before running the jobs
                        file_name_in = ''
                        file_name_out = file_path
                        start_time = time.time()
                        
                        # GH#23: need to filter deployment based on the folder name
                        Context().add_env_variable("$OF_COMPILE_SOURCE", file_path)

                        for job in jobs:
                            # For the SetupJob, file_name_in is an absolute path, but for all other jobs this
                            # is just the name of the file
                            file_name_in = file_name_out
                            rc = job.run(file_name_in)
                            if rc not in (0, 1):
                                Log().logger.error(LogMessage.ABORT_FILE.value %
                                                   file_name_in)
                                break
                            file_name_out = job.file_name_out

                        # Report related tasks
                        elapsed_time = time.time() - start_time
                        self._end_processing(0, rc, args.clear, report,
                                             file_path, elapsed_time, profile)

                    except KeyboardInterrupt:
                        rc = -2
                        self._end_processing(1, rc, args.clear, report,
                                             file_path, 0, profile)
                        if INTERRUPT is True:
                            raise KeyboardInterrupt()

            if len(source.file_paths) != 0:
                report.summary()

                if args.grouping is True:
                    grouping = Grouping(args.clear)
                    grouping.run()

            self._end_processing(2, rc)

        except KeyboardInterrupt:
            rc = -3
            self._end_processing(3, rc)

        return rc
