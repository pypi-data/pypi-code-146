#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

from ..exceptions import raise_exception

_empty = "\\s|\\u00a0|\\u0020|\\u3000"

_spec_all_re = re.compile(f"({_empty})*", re.U)
_spec_start_end_re = re.compile(f"^({_empty})*|({_empty})*$", re.U)
_spec_start = re.compile(f"^({_empty})*", re.U)
_spec_end = re.compile(f"({_empty})*$", re.U)

__slot__ = (_empty, _spec_all_re, _spec_start_end_re)


class String(str):
    """
    A superset of the str object.
    Some enhanced methods are provided
    """
    def __new__(cls, value):
        return str.__new__(cls, str(value))

    def equals_trip(self, value: str):
        """
        After removing the first and last white space characters, it is judged
        """
        if not issubclass(type(value), str):
            return False
        return self.trip() == _spec_start_end_re.sub("", value)

    def equals(self, value: str):
        """
        Directly judge whether it is equal or not
        """
        if not issubclass(type(value), str):
            return False
        return self == value

    def trip_start(self) -> 'String':
        """
        Clear the space at the end of the string
        """
        return String(_spec_start.sub("", self))

    def trip_end(self) -> 'String':
        """
        Clear spaces at the beginning of the string
        """
        return String(_spec_end.sub("", self))

    def trip_all(self) -> 'String':
        """
        Clear all whitespace characters
        """
        return String(_spec_all_re.sub("", self))

    def trip(self) -> 'String':
        """
        Clears the leading and trailing whitespace characters
        """
        return String(_spec_start_end_re.sub("", self))

    def is_empty(self) -> bool:
        """
        Judge whether the string is empty
        The first and last spaces will be removed before judgment
        """
        return self.trip_all() == ""

    def is_not_empty(self) -> bool:
        """
        Judge whether the string is not empty
        The first and last spaces will be removed before judgment
        """
        return not self.is_empty()

    def is_black(self) -> bool:
        """
        string is black,don't remove start and end spec
        """
        return not self or self == ""

    def is_not_black(self) -> bool:
        """
        string isn't black,don't remove start and end spec
        """
        return not self.is_black()

    def contains(self, target: str) -> bool:
        """
        src contains target
        """
        if isinstance(target, str):
            return target in self
        return False

    def not_contains(self, target: str) -> bool:
        """
        src not contains target
        """
        return not self.contains(target)

    def trip_contains(self, target: str) -> bool:
        """
        after removing the leading and trailing spaces, determine that src contains target
        """
        if isinstance(target, str):
            return _spec_start_end_re.sub("", target) in self.trip()
        return False

    def trip_not_contains(self, target: str) -> bool:
        """
        after removing the leading and trailing spaces, determine that src not contains target
        """
        return not self.trip_contains(target)

    def trip_all_contains(self, target: str) -> bool:
        """
        Remove the "space" from anywhere in the string and make sure that src contain the destination string
        :param target: The included string
        """
        if isinstance(target, str):
            return _spec_all_re.sub("", target) in _spec_all_re.sub("", self)
        return False

    def trip_all_not_contains(self, target: str) -> bool:
        """
        Remove the "space" from anywhere in the string and make sure that src does not contain the destination string
        :param target: The included string
        """
        return not self.trip_all_contains(target)

    def to_bool(self, default: bool = False) -> bool:
        """
        Converts the string bool type to a true bool type.
        :param default: If it is not of type string bool, the value returned by default.
        """
        if isinstance(self, str):
            if self == "True" or self == "true":
                return True
            elif self == "False" or self == "false":
                return False
        return default

    def convert_to_camel(self) -> 'String':
        """snake to camel"""
        return String(re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), self))

    def convert_to_pascal(self) -> 'String':
        """snake to pascal"""
        char = re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), self)
        char_1 = char[:1].upper()
        char_rem = char[1:]
        return String(char_1 + char_rem)

    def convert_to_snake(self) -> 'String':
        """camel to snake"""
        if '_' not in self:
            name = re.sub(r'([a-z])([A-Z])', r'\1_\2', self)
        else:
            raise ValueError(f"'{self}' contain underscores and cannot be converted")
        return String(name.lower())

    def last_index(self, substring: str, from_index: int = 0, to_index: int = 0) -> int:
        """
        Gets the position (start position) of the last occurrence of the specified character in the string.
        If from_index or to_index is specified, the returned position is relative.
        :param substring: Specifies the string retrieved.
        :param from_index: The location where the retrieval begins
        :param to_index: The location where the retrieval ended
        """
        if not issubclass(type(from_index), int):
            raise_exception(TypeError(f"expect is 'int', got a {type(from_index).__name__}"))
        if not issubclass(type(to_index), int):
            raise_exception(TypeError(f"expect is 'int', got a {type(to_index).__name__}"))
        if not issubclass(type(substring), str):
            raise_exception(TypeError(f"expect is 'str', got a {type(substring).__name__}"))
        length = len(self)
        if to_index == 0:
            to_index = length
        substr_len = len(substring)
        if from_index > to_index:
            from_index, to_index = to_index, from_index
        if from_index >= length or substr_len > length:
            return -1
        tmp_str = self[from_index:to_index]
        start = from_index
        last_index = -1
        while True:
            end = substr_len + start
            tmp = tmp_str[start:end]
            if tmp == substring:
                last_index = start
            if end == length:
                break
            start += 1
        return last_index


__all__ = [String]
