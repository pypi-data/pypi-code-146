#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import Enum
from typing import Dict

from .._internal import _T
from ..utils import EnumUtils


class EnhanceEnum(Enum):
    """
    Enumerates enhanced classes that provide some tool methods.
    """
    @classmethod
    def has_value(cls, value: _T) -> bool:
        """
        Determines whether the enumeration contains members of the specified value
        """
        return EnumUtils.has_value(cls, value)

    @classmethod
    def has_name(cls, name: str) -> bool:
        """
        Determines whether the enumeration contains members with the specified name
        """
        return EnumUtils.has_name(cls, name)

    @classmethod
    def get_by_name(cls, name: str, default: Enum = None) -> Enum:
        """
        Gets the enumeration object by the enumeration name
        :param name: Enumerates element name
        :param default: If the default value is not found
        """
        return EnumUtils.get_by_name(cls, name, default)

    @classmethod
    def get_by_value(cls, value: _T, default: Enum = None):
        """
        Gets the enumeration object from the enumeration value
        :param value: Enumerates element value
        :param default: If the default value is not found
        """
        return EnumUtils.get_by_value(cls, value, default)

    @classmethod
    def to_dict(cls) -> Dict:
        """
        Convert the enumeration to a dictionary
        """
        return EnumUtils.to_dict(cls)


__all__ = [EnhanceEnum]
