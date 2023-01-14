#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import Lock
from typing import Union, Optional

B = Union[bool, str]


class __RestConfig(object):
    """
    Rest  global configuration
    """
    __lock__ = Lock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        with cls.__lock__:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__allow_redirection = True
        self.__check_status = False
        self.__only_body = True
        self.__encoding = "utf-8"

    @property
    def allow_redirection(self) -> bool:
        return self.__allow_redirection

    @allow_redirection.setter
    def allow_redirection(self, value: B):
        self.__set_allow_redirection(value)

    def __set_allow_redirection(self, value: B):
        if issubclass(type(value), bool):
            self.__allow_redirection = value
        elif issubclass(type(value), str):
            self.__allow_redirection = _to_bool(value, True)

    @property
    def check_status(self) -> bool:
        return self.__check_status

    @check_status.setter
    def check_status(self, value: B):
        self.__set_check_status(value)

    def __set_check_status(self, value: B):
        if issubclass(type(value), bool):
            self.__check_status = value
        elif issubclass(type(value), str):
            self.__check_status = _to_bool(value, False)

    @property
    def only_body(self) -> bool:
        return self.__only_body

    @only_body.setter
    def only_body(self, value: B):
        self.__set_only_body(value)

    def __set_only_body(self, value: B):
        if issubclass(type(value), bool):
            self.__only_body = value
        elif issubclass(type(value), str):
            self.__only_body = _to_bool(value, True)

    @property
    def encoding(self) -> str:
        return self.__encoding

    @encoding.setter
    def encoding(self, value: Optional[str]):
        self.__set_encoding(value)

    def __set_encoding(self, value: Optional[str]):
        if issubclass(type(value), str):
            self.__encoding = value


def _to_bool(value: str, default: bool = False) -> bool:
    """
    Converts the string bool type to a true bool type.
    :param value: string bool type.
    :param default: If it is not of type string bool, the value returned by default.
    """
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value == "True" or value == "true":
            return True
        elif value == "False" or value == "false":
            return False
    return default


RestConfig: __RestConfig = __RestConfig()

__all__ = [RestConfig]
