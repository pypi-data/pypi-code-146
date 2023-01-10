#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from sys import exc_info
from typing import Any, Dict, Optional

# Modules libraries
from oyaml import safe_load as yaml_safe_load, YAMLError

# Components
from ..package.bundle import Bundle
from ..prints.colors import Colors
from ..types.parsers import ParsersData
from .gitlab import GitLab
from .variables import Variables

# Parsers class, pylint: disable=too-few-public-methods
class Parsers:

    # Members
    __options: Namespace

    # Constructor
    def __init__(self, options: Namespace) -> None:

        # Prepare options
        self.__options = options

        # Prepare variables
        self.__variables = Variables(self.__options)

    # Read
    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:

        # Read GitLab CI YAML
        try:
            with open(self.__options.configuration, encoding='utf8',
                      mode='r') as configuration_data:
                data: ParsersData = yaml_safe_load(configuration_data)
                return GitLab(self.__options, self.__variables).parse(data)
        except YAMLError as exc:
            print(' ')
            print(
                f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR:' \
                    f' {Colors.BOLD}{exc}{Colors.RESET}'
            )
            print(' ')
        except (FileNotFoundError, PermissionError):
            print(' ')
            print(
                f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR:' \
                    f' {Colors.BOLD}{str(exc_info()[1])}{Colors.RESET}'
            )
            print(' ')

        # Failure
        return None
