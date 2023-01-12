#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
from pathlib import Path
from threading import Lock
from time import strftime
from typing import Optional, Union

from simplebox.converter import StorageUnit
from simplebox.enums import EnhanceEnum
from simplebox.utils import StringUtils


class LogLevel(EnhanceEnum):
    """
    log level
    ignore
    """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOSET = 0


L = Union[LogLevel, str, int]
B = Union[bool, str]


class __LogConfig(object):
    """
    Log global configuration
    """
    __lock__ = Lock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        with cls.__lock__:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__dir: Path = Path.cwd().joinpath("logs").absolute()
        self.__level: LogLevel = LogLevel.NOSET
        self.__level_console = LogLevel.CRITICAL
        self.__level_file = LogLevel.CRITICAL
        self.__format: str = f"[%(asctime)s {strftime('%z')}]-[%(process)s]-[%(thread)s]-[%(filename)s %(lineno)s]-[%(name)s]-[%(levelname)s] %(message)s"
        self.__coding: str = "utf-8"
        self.__name: str = f"simplebox-{datetime.now().strftime('%Y-%m-%d')}.log"
        self.__max_bytes: int = StorageUnit.MB.of(100).to(StorageUnit.BYTE).integer()
        self.__backup_count: int = 10
        self.__path: Path = self.__dir.joinpath(self.__name).absolute()
        self.__banner: bool = False
        self.__off_file: bool = True
        self.__off_console: bool = False
        self.__off: bool = False
        self.__cut: bool = False
        if not self.__dir.exists():
            self.dir.mkdir(parents=True)

    @property
    def dir(self) -> Optional[Path]:
        return self.__dir

    @dir.setter
    def dir(self, value: Union[Path, str]):
        self.__set_dir(value)

    def __set_dir(self, value: Union[Path, str]):
        if issubclass(type(value), Path) or issubclass(type(value), str):
            path = Path(value)
            if not path.exists():
                path.mkdir(parents=True)
            self.__dir = value
            self.__path = Path(self.__dir).joinpath("logs", self.__name)

    @property
    def level(self) -> LogLevel:
        return self.__level

    @level.setter
    def level(self, value: L):
        self.__set_level(value)

    def __set_level(self, value: L):
        if issubclass(type(value), LogLevel):
            self.__level = value
        elif issubclass(type(value), str):
            self.__level = LogLevel.get_by_name(value.upper(), LogLevel.NOSET)
        elif issubclass(type(value), int):
            self.__level = LogLevel.get_by_value(value, LogLevel.NOSET)

    @property
    def level_console(self) -> LogLevel:
        return self.__level_console

    @level_console.setter
    def level_console(self, value: L):
        self.__set_level_console(value)

    def __set_level_console(self, value: L):
        if issubclass(type(value), LogLevel):
            self.__level_console = value
        elif issubclass(type(value), str):
            self.__level_console = LogLevel.get_by_value(value.upper(), LogLevel.CRITICAL)
        elif issubclass(type(value), int):
            self.__level_console = LogLevel.get_by_name(value.upper(), LogLevel.CRITICAL)

    @property
    def level_file(self) -> LogLevel:
        return self.__level_file

    @level_file.setter
    def level_file(self, value: L):
        self.__set_level_file(value)

    def __set_level_file(self, value: L):
        if issubclass(type(value), LogLevel):
            self.__level_file = value
        elif issubclass(type(value), str):
            self.__level_file = LogLevel.get_by_name(value.upper(), LogLevel.CRITICAL)
        elif issubclass(type(value), int):
            self.__level_file = LogLevel.get_by_value(value, LogLevel.CRITICAL)

    @property
    def format(self) -> Optional[str]:
        return self.__format

    @format.setter
    def format(self, value: Optional[str]):
        self.__set_format(value)

    def __set_format(self, value: Optional[str]):
        if issubclass(type(value), str):
            self.__format = value

    @property
    def coding(self) -> Optional[str]:
        return self.__coding

    @coding.setter
    def coding(self, value: Optional[str]):
        self.__set_coding(value)

    def __set_coding(self, value: Optional[str]):
        if issubclass(type(value), str):
            self.__coding = value

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, value: Optional[str]):
        self.__set_name(value)

    def __set_name(self, value: Optional[str]):
        if issubclass(type(value), str):
            self.__name = value
            self.__path = Path(self.dir).joinpath(self.__name)

    @property
    def max_bytes(self) -> Optional[int]:
        return self.__max_bytes

    @max_bytes.setter
    def max_bytes(self, value: Optional[int]):
        self.__set_max_bytes(value)

    def __set_max_bytes(self, value: Optional[int]):
        if issubclass(type(value), int):
            self.__max_bytes = value

    @property
    def backup_count(self) -> Optional[int]:
        return self.__backup_count

    @backup_count.setter
    def backup_count(self, value: Optional[int]):
        self.__set_backup_count(value)

    def __set_backup_count(self, value: Optional[int]):
        if issubclass(type(value), int):
            self.__backup_count = value

    @property
    def path(self) -> Optional[Path]:
        return self.__path

    @property
    def banner(self) -> Optional[bool]:
        return self.__banner

    @banner.setter
    def banner(self, value: B):
        self.__set_banner(value)

    def __set_banner(self, value: B):
        if issubclass(type(value), bool):
            self.__banner = value
        elif issubclass(type(value), str):
            self.__banner = StringUtils.to_bool(value, True)

    @property
    def off_file(self) -> Optional[bool]:
        return self.__off_file

    @off_file.setter
    def off_file(self, value: B):
        self.__set_off_file(value)

    def __set_off_file(self, value: B):
        if issubclass(type(value), bool):
            self.__off_file = value
        elif issubclass(type(value), str):
            self.__off_file = StringUtils.to_bool(value, False)

    @property
    def off_console(self) -> Optional[bool]:
        return self.__off_console

    @off_console.setter
    def off_console(self, value: B):
        self.__set_off_console(value)

    def __set_off_console(self, value: B):
        if issubclass(type(value), bool):
            self.__off_console = value
        elif issubclass(type(value), str):
            self.__off_console = StringUtils.to_bool(value, False)

    @property
    def off(self) -> Optional[bool]:
        return self.__off

    @off.setter
    def off(self, value: B):
        self.__set_off(value)

    def __set_off(self, value: B):
        if issubclass(type(value), bool):
            self.__off = value
        elif issubclass(type(value), str):
            self.__off = StringUtils.to_bool(value, False)

    @property
    def cut(self) -> Optional[bool]:
        return self.__cut

    @cut.setter
    def cut(self, value: B):
        self.__set_cut(value)

    def __set_cut(self, value: B):
        if issubclass(type(value), bool):
            self.__cut = value
        elif issubclass(type(value), str):
            self.__off = StringUtils.to_bool(value, False)


LogConfig: __LogConfig = __LogConfig()

__all__ = [LogConfig, LogLevel]
