#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import EnumMeta, Enum
from typing import Dict

from .._internal import _T
from ..classes import StaticClass
from ..collection import ArrayList


class EnumUtils(metaclass=StaticClass):
    """
    enum tools
    """
    @staticmethod
    def get_by_name(enum_: EnumMeta, name: str, default: Enum = None) -> Enum:
        """
        Gets the enumeration object by the enumeration name
        :param enum_: Enumerate classes
        :param name: Enumerates element name
        :param default: If the default value is not found
        :return:
        """
        member = enum_.__members__.get(name)
        return member if member else default

    @staticmethod
    def get_by_value(enum_: EnumMeta, value: _T, default: Enum = None) -> Enum:
        """
        Gets the enumeration object from the enumeration value
        :param enum_: Enumerate classes
        :param value: Enumerates element value
        :param default: If the default value is not found
        :return:
        """
        for element in enum_:
            if element.value == value:
                return element
        return default

    @staticmethod
    def has_name(enum_: EnumMeta, name: str) -> bool:
        """
        Determines whether the enumeration contains members with the specified name
        """
        return name in enum_.__members__.keys()

    @staticmethod
    def has_value(enum_: EnumMeta, value: _T) -> bool:
        """
        Determines whether the enumeration contains members of the specified value
        """
        return value in ArrayList(iterable=enum_.__members__.values()).map(lambda e: e.value)

    @staticmethod
    def to_dict(enum_: EnumMeta) -> Dict[str, _T]:
        """
        Convert the enumeration to a dictionary
        """
        members = enum_.__members__
        keys = members.keys()
        values = ArrayList(iterable=members.values()).map(lambda e: e.value)
        return dict(zip(keys, values))


__all__ = [EnumUtils]
