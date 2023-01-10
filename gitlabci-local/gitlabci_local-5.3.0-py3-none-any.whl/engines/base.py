#!/usr/bin/env python3

# Standard libraries
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, NamedTuple

# Components
from ..types.volumes import Volumes

# Commands type
Commands = List[str]

# ContainerName type
ContainerName = str

# ExecResult type
class ExecResult(NamedTuple):

    # Properties
    exit_code: int
    output: str
    returncode: int

# LogsResult type
LogsResult = Iterator[bytes]

# Base engine class, pylint: disable=unused-argument
class BaseEngine(ABC): # pragma: no cover

    # Command exec
    @abstractmethod
    def cmd_exec(self) -> str:
        return ''

    # Container
    @property
    @abstractmethod
    def container(self) -> ContainerName:
        return ''

    # Exec
    @abstractmethod
    def exec(self, command: Commands) -> ExecResult:
        return ExecResult(0, '', 0)

    # Get
    @abstractmethod
    def get(self, image: str) -> None:
        pass

    # Logs
    @abstractmethod
    def logs(self) -> LogsResult:
        return iter()

    # Pull
    @abstractmethod
    def pull(self, image: str, force: bool = False) -> None:
        pass

    # Remove
    @abstractmethod
    def remove(self) -> None:
        pass

    # Remove image
    @abstractmethod
    def rmi(self, image: str) -> None:
        pass

    # Run, pylint: disable=too-many-arguments
    @abstractmethod
    def run(self, image: str, commands: Commands, entrypoint: Any,
            variables: Dict[str, str], network: str, option_sockets: bool, services: bool,
            volumes: Volumes, directory: str, temp_folder: str) -> None:
        pass

    # Stop
    @abstractmethod
    def stop(self, timeout: int) -> None:
        pass

    # Supports
    @abstractmethod
    def supports(self, binary: str) -> bool:
        return False

    # Wait
    @abstractmethod
    def wait(self) -> bool:
        return False
