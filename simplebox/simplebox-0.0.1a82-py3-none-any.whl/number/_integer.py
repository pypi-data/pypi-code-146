#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ._compare import _Compare, _T
from ..exceptions import raise_exception


class Integer(int, _Compare):
    """
    A subclass of int.
    Some tool methods are provided
    """
    def __new__(cls, num: _T = 0, base=10):
        if base not in [2, 8, 10, 16]:
            raise_exception(ValueError(f"base error: {base}"))
        if base != 10:
            return int.__new__(cls, num, base=base)
        if issubclass(type(num), str) and not num.isdigit():
            raise_exception(ValueError(f"The string '{num}' is not a valid number"))
        return int.__new__(cls, num)

    def __init__(self, num: _T = 0, base=10):
        self.__num = num
        self.__base = base

    def is_odd(self) -> bool:
        """
        The check is an odd number
        """
        return not self.is_even()

    def is_even(self) -> bool:
        """
        The check is an even number
        """
        return self & 1 == 0

    def to_bin(self) -> str:
        """
        Convert to binary (string)
        """
        return bin(self)

    def to_oct(self) -> str:
        """
        Convert to octal (string)
        """
        return oct(self)

    def to_hex(self) -> str:
        """
        Convert to hexadecimal (string)
        """
        return hex(self)
