#!/usr/bin/env python
# -*- coding:utf-8 -*-
from decimal import Decimal, ROUND_HALF_UP

from ._compare import _Compare, _T
from ..exceptions import raise_exception
from ..number import Integer


class Float(float, _Compare):
    """
    A subclass of float.
    Some tool methods are provided
    """
    def __new__(cls, num: _T = 0):
        if issubclass(type(num), str) and not num.isdigit():
            raise_exception(ValueError(f"The string '{num}' is not a valid number"))
        return float.__new__(cls, num)

    def __init__(self, num: _T = 0):
        self.__num = num

    def round(self, accuracy: int = None) -> 'Float':
        """
        Rounds floating-point types
        """
        if isinstance(accuracy, int) and accuracy >= 0:
            return Float(Decimal(self.__num).quantize(Decimal(f'0.{"0" * accuracy}'), rounding=ROUND_HALF_UP).__float__())
        return self

    def integer(self) -> Integer:
        """
        Output as int type
        """
        return Integer(self.__num)
