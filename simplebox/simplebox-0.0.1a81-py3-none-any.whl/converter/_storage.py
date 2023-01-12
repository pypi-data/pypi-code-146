#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ._calculator import _Converter, Enum
from ..number import Integer


class StorageUnit(Enum):
    """
    Storage unit conversion tool
    """
    BIT = Integer(1)
    BYTE = Integer(1 << 3)
    KB = Integer(1 << 13)
    MB = Integer(1 << 23)
    GB = Integer(1 << 33)
    TB = Integer(1 << 43)
    PB = Integer(1 << 53)
    EB = Integer(1 << 63)
    ZB = Integer(1 << 73)
    YB = Integer(1 << 83)
    BB = Integer(1 << 93)
    NB = Integer(1 << 103)
    DB = Integer(1 << 113)

    def of(self, num: int or float) -> '_Converter':
        converter = _Converter(num)
        setattr(converter, "_Converter__decimal", self.value)
        return converter


__all__ = [StorageUnit]
