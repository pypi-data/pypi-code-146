#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of methods useful in any module.

This module gathers a set of methods that are useful in many other modules. When a method is widely 
used in different modules, a general version of it is created and can be found here.

Typical usage example:
    ShellHandler().execute_command(command)
"""

# Generic/Built-in modules
import os
import shutil
import subprocess
import sys

# Third-party modules

# Owned modules
from ..enums.ErrorEnum import ErrorMessage
from ..enums.LogEnum import LogMessage
from ..Log import Log


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


class ShellHandler(metaclass=SingletonMeta):
    """A class used to run shell related tasks across all modules.

    Attributes:
        _env {dictionary} -- Environment variables for the execution of the program.

    Methods:
        _is_command_exist(command) -- Checks if the command exists in the environment using which.
        _run_command(command, env) -- Runs the command, using variables from the environment if any.
        _read_command(process) -- Decode stdout and stderr from the CompletedProcess object.
        _log_command(stdout, stderr, return_code, command_type) -- Log output and errors if any, with different log levels.
        execute_command(command, command_type, env=None) -- Executes shell command.
        
        evaluate_filter(section, filter_name): Evaluates the status of the filter function passed as an argument.

        evaluate_env_variable(self, environment_variable) -- Evaluates if the input variable exists in the current environment.
    """

    def __init__(self):
        """Initializes all attributes of the class.
        """
        self._env = os.environ.copy()

    # Shell command related methods

    @staticmethod
    def _is_command_exist(command):
        """Checks if the command exists in the environment using which.

        Arguments:
            command {string} -- Shell command that needs to be checked.

        Returns:
            boolean -- True if the command does exist, and False otherwise.
        """
        return bool(shutil.which(command))

    @staticmethod
    def _run_command(command, env):
        """Runs the command, using variables from the environment if any.

        Arguments:
            command {string} -- Shell command that needs to be executed.
            env {dictionary} -- Environment variables currently in the shell environment.

        Returns:
            CompletedProcess object -- Object containing multiple information on the command execution.
        """
        process = subprocess.run(command,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 check=False,
                                 env=env)
        return process

    @staticmethod
    def _read_command(process):
        """Decode stdout and stderr from the CompletedProcess object.

        Arguments:
            process {CompletedProcess object} -- Object containing multiple information on the command execution.

        Returns:
            tuple -- stdout, stderr, and return code of the shell command.

        Raises:
            UnicodeDecodeError -- Exception raised if there is an issue decoding a certain character in stdout or stderr.
        """
        try:
            stdout = process.stdout.decode('utf_8')
            stderr = process.stderr.decode('utf_8')
        except UnicodeDecodeError:
            Log().logger.debug(ErrorMessage.UNICODE.value)
            stdout = process.stdout.decode('latin_1')
            stderr = process.stderr.decode('latin_1')

        return_code = process.returncode

        return stdout, stderr, return_code

    @staticmethod
    def _log_command(stdout, stderr, return_code, command_type):
        """Log output and errors if any, with different log levels.

        Arguments:
            stdout {string} -- Standard output of the command.
            stderr {string} -- Standard error of the command.
            return_code {integer} -- Return code of the command.
            command_type {string} -- Type of the command to execute.
        """
        if Log().level == 'DEBUG':
            if return_code != 0 and command_type != 'filter':
                Log().logger.error(stdout)
                Log().logger.error(stderr)
                Log().logger.error(LogMessage.RETURN_CODE.value % return_code)
            else:
                Log().logger.debug(stdout)
                Log().logger.debug(stderr)
                Log().logger.debug(LogMessage.RETURN_CODE.value % return_code)
        elif return_code != 0 and command_type != 'filter':
            Log().logger.error(stdout)
            Log().logger.error(stderr)

    def execute_command(self, command, command_type='', env=None):
        """Executes shell command.
        
        This method is dedicated to execute a shell command and it handles exceptions in case of failure.

        Arguments:
            command {string} -- Shell command that needs to be executed.
            command_type {string} -- Type of the command to execute.
            env {dictionary} -- Environment variables currently in the shell environment.

        Returns:
            tuple -- stdout, stderr, and return code of the shell command.

        Raises:
            KeyboardInterrupt -- Exception raised if the user press Ctrl+C during the command shell execution.
            SystemError -- Exception raised if the command does not exist.
            subprocess.CalledProcessError -- Exception raised if an error didn't already raised one of the previous exceptions.
        """
        if env is None:
            env = self._env

        try:
            command = os.path.expandvars(command)

            if command_type != 'deploy':
                Log().logger.debug(command)

            root_command = command.split()[0]

            if self._is_command_exist(root_command):
                process = self._run_command(command, env)
                stdout, stderr, return_code = self._read_command(process)
            else:
                raise SystemError()
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except SystemError:
            Log().logger.error(ErrorMessage.SYSTEM_SHELL % root_command)
            stdout = None
            stderr = None
            return_code = -1
        except subprocess.CalledProcessError as error:
            Log().logger.error(ErrorMessage.CALLED_PROCESS.value % error)
            stdout = None
            stderr = None
            return_code = -1

        self._log_command(stdout, stderr, return_code, command_type)

        return stdout, stderr, return_code

    # Filter functions

    def evaluate_filter(self, function, name, section, env):
        """Evaluates the status of the filter function passed as an argument.

        Arguments:
            function {string} -- Shell command that needs to be executed.
            name {string} -- Name of the filter function.
            section {string} -- Name of the section.
            env {dictionary} -- Environment variables currently in the shell environment.

        Returns:
            None or boolean -- Result of the filter function evaluation.
        """
        if function != '':
            _, _, rc = self.execute_command(function, 'filter', env)

            # grep command returns 0 if there is any line match
            if rc == 0:
                result = True
                Log().logger.debug(LogMessage.FILTER_TRUE.value %
                                   (section, name))
            else:
                result = False
                Log().logger.debug(LogMessage.FILTER_FALSE.value %
                                   (section, name))
        else:
            Log().logger.debug(LogMessage.FILTER_NONE.value % section)
            result = None

        return result

    # Environment variables

    @staticmethod
    def evaluate_env_variable(environment_variable):
        """Evaluates if the input variable exists in the current environment.

        Arguments:
            environment_variable {string} -- Environment variable that needs to be evaluated.

        Returns:
            string -- Result of the environment variable evaluation.

        Raises:
            KeyError -- Exception raised if the variable does not exist.
        """
        try:
            env_variable = os.environ[environment_variable]
        except KeyError:
            Log().logger.critical(ErrorMessage.KEY.value % environment_variable)
            sys.exit(-1)
        else:
            return env_variable