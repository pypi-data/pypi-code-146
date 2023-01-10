#!/usr/bin/env python3

# Standard libraries
from typing import List

# Options class, pylint: disable=too-many-instance-attributes
class Options:

    # Members
    __disabled: str
    __env_job_name: str
    __env_job_path: str
    __extends_available: List[str]
    __extends_unknown: List[str]
    __git_clone_path: str
    __host: bool
    __quiet: bool
    __silent: bool
    __sockets: bool
    __ssh: bool

    # Constructor
    def __init__(self) -> None:

        # Initialize members
        self.__disabled = ''
        self.__env_job_name = ''
        self.__env_job_path = ''
        self.__extends_available = []
        self.__extends_unknown = []
        self.__git_clone_path = ''
        self.__host = False
        self.__quiet = False
        self.__silent = False
        self.__sockets = False
        self.__ssh = False

    # Disabled
    @property
    def disabled(self) -> str:
        return self.__disabled

    # Disabled
    @disabled.setter
    def disabled(self, value: str) -> None:
        self.__disabled = value

    # Env job name
    @property
    def env_job_name(self) -> str:
        return self.__env_job_name

    # Env job name
    @env_job_name.setter
    def env_job_name(self, value: str) -> None:
        self.__env_job_name = value

    # Env job path
    @property
    def env_job_path(self) -> str:
        return self.__env_job_path

    # Env job path
    @env_job_path.setter
    def env_job_path(self, value: str) -> None:
        self.__env_job_path = value

    # Extends available
    @property
    def extends_available(self) -> List[str]:
        return self.__extends_available

    # Extends available
    @extends_available.setter
    def extends_available(self, value: List[str]) -> None:
        self.__extends_available = value

    # Extends unknown
    @property
    def extends_unknown(self) -> List[str]:
        return self.__extends_unknown

    # Extends unknown
    @extends_unknown.setter
    def extends_unknown(self, value: List[str]) -> None:
        self.__extends_unknown = value

    # Git clone path
    @property
    def git_clone_path(self) -> str:
        return self.__git_clone_path

    # Git clone path
    @git_clone_path.setter
    def git_clone_path(self, value: str) -> None:
        self.__git_clone_path = value

    # Host
    @property
    def host(self) -> bool:
        return self.__host

    # Host
    @host.setter
    def host(self, value: bool) -> None:
        self.__host = value

    # Quiet
    @property
    def quiet(self) -> bool:
        return self.__quiet

    # Quiet
    @quiet.setter
    def quiet(self, value: bool) -> None:
        self.__quiet = value

    # Silent
    @property
    def silent(self) -> bool:
        return self.__silent

    # Silent
    @silent.setter
    def silent(self, value: bool) -> None:
        self.__silent = value

    # Sockets
    @property
    def sockets(self) -> bool:
        return self.__sockets

    # Sockets
    @sockets.setter
    def sockets(self, value: bool) -> None:
        self.__sockets = value

    # SSH
    @property
    def ssh(self) -> bool:
        return self.__ssh

    # SSH
    @ssh.setter
    def ssh(self, value: bool) -> None:
        self.__ssh = value
