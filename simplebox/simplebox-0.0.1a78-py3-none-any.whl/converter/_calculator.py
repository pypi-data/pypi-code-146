#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import Enum

from ..number import Float, Integer


class _NumericType(Float):
    def __init__(self, num=0):
        super().__init__(num)
        self.__num = num


class _Converter(Integer):
    """
    The calculation is performed with bit as the reference unit
    """

    def __init__(self, num: int or float):
        self.__num: int = num
        self.__decimal = None
        super().__init__(num)

    def to(self, unit: Enum) -> _NumericType:
        return _NumericType(self.__num * self.__decimal / unit.value)


__all__ = [_Converter, _NumericType]
