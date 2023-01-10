#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from os import environ
from pathlib import Path
from typing import Dict, List

# Modules libraries
from dotenv import dotenv_values

# Variables class
class Variables:

    # Members
    __cache: Dict[str, str]
    __env_files: Dict[str, str]
    __globals: Dict[str, str]
    __locals: Dict[str, str]
    __options: Namespace
    __parameters: Dict[str, str]

    # Constructor
    def __init__(self, options: Namespace) -> None:

        # Prepare options
        self.__options = options

        # Prepare members
        self.__env_files = {}
        self.__globals = {}
        self.__locals = {}
        self.__parameters = {}

        # Cache environment
        self.environment_cache()

        # Parse env options
        self.options_parse_env()

    # Cache environment
    def environment_cache(self) -> None:
        self.__cache = environ.copy()

    # Restore environment
    def environment_restore(self) -> None:
        environ.clear()
        environ.update(self.__cache)

    # Update environment
    @staticmethod
    def environment_update(values: Dict[str, str]) -> None:

        # Apply environment values
        environ.update(values)

    # Apply variables
    def apply(self, types: List[str]) -> None:

        # Prepare parameters variables
        if 'parameters' in types:
            for variable, value in self.__parameters.items():
                environ[variable] = value

        # Prepare locals variables
        if 'locals' in types:
            for variable, value in self.__locals.items():
                if variable not in environ:
                    environ[variable] = value

        # Prepare globals variables
        if 'globals' in types:
            for variable, value in self.__globals.items():
                if variable not in environ:
                    environ[variable] = value

        # Prepare env_files variables
        if 'env_files' in types:
            for variable, value in self.__env_files.items():
                if variable not in environ:
                    environ[variable] = value

    # Evaluate job variables
    def evaluate_job(self, job_variables: Dict[str, str]) -> Dict[str, str]:

        # Variables
        variables: Dict[str, str] = {}

        # Register parameters variables
        for variable, value in self.__parameters.items():
            variables[variable] = value

        # Register locals variables
        for variable, value in self.__locals.items():
            if variable not in variables:
                variables[variable] = value

        # Register job variables
        for variable, value in job_variables.items():
            if variable not in variables:
                variables[variable] = value

        # Register globals variables
        for variable, value in self.__globals.items():
            if variable not in variables:
                variables[variable] = value

        # Register env_files variables
        for variable, value in self.__env_files.items():
            if variable not in variables:
                variables[variable] = value

        # Result
        return variables

    # Parse options
    def options_parse_env(self) -> None:

        # Variables
        files: List[Path] = []

        # Register .env file
        files += [
            Path(self.__options.path) / '.env',
        ]

        # Parse env options
        if self.__options.env:
            for env in self.__options.env:
                env_parsed = env.split('=', 1)

                # Parse VARIABLE=value
                if len(env_parsed) == 2:
                    variable = env_parsed[0]
                    value = env_parsed[1]
                    self.__parameters[variable] = value

                # Parse ENVIRONMENT_FILE
                elif (Path(self.__options.path) / env).is_file():
                    files += [Path(self.__options.path) / env]

                # Parse VARIABLE
                else:
                    variable = env
                    if variable in environ:
                        self.__parameters[variable] = environ[variable]

        # Iterate through environment files
        for env_file in files:
            if not env_file.is_file():
                continue

            # Parse environment files
            env_values = dotenv_values(dotenv_path=env_file)
            for variable in env_values:

                # Define default environment variable
                if isinstance(env_values[variable], str):
                    self.__env_files[variable] = str(env_values[variable])

    # Parse local_env
    def local_parse_env(self, data_node: List[str]) -> None:

        # Parse data node
        for env in data_node:
            env_parsed = env.split('=', 1)

            # Parse VARIABLE=value
            if len(env_parsed) == 2:
                variable = env_parsed[0]
                value = env_parsed[1]
                if variable not in self.__locals:
                    self.__locals[variable] = value

            # Parse ENVIRONMENT_FILE
            elif (Path(self.__options.path) / env).is_file():
                env_file = Path(self.__options.path) / env
                env_values = dotenv_values(dotenv_path=env_file)
                for variable in env_values:

                    # Define default environment variable
                    if variable not in self.__locals and isinstance(
                            env_values[variable], str):
                        self.__locals[variable] = str(env_values[variable])

            # Parse VARIABLE
            else:
                variable = env
                if variable not in self.__locals:
                    if variable in environ:
                        self.__locals[variable] = environ[variable]

    # Parse local_variables
    def local_parse_variables(self, data_node: Dict[str, str]) -> None:

        # Parse data node
        for variable in data_node:
            value = data_node[variable]
            if variable not in self.__locals:
                self.__locals[variable] = value

    # Globals
    @property
    def globals(self) -> Dict[str, str]:
        return self.__globals

    # Parameters
    @property
    def parameters(self) -> Dict[str, str]:
        return self.__parameters
