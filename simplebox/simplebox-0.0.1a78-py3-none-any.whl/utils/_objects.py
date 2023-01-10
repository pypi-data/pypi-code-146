#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from inspect import stack, getframeinfo, currentframe
from random import sample
from re import findall

from .._internal import _T, _V
from ..char import StringBuilder
from ..classes import StaticClass
from ..exceptions import raise_exception, NonePointerException

_base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
loc = locals()


class ObjectsUtils(metaclass=StaticClass):
    """
    object tools
    """

    @staticmethod
    def check_contains(iterable_obj: _T, content: _V, throw: BaseException = None):
        """
        Check whether obj contains content, and throw an exception if it does not
        """
        if not issubclass(type(throw), BaseException):
            frame = getframeinfo(currentframe().f_back)
            parameters = findall(re.compile(r".*check_contains[(](.*?)[)]", re.S), frame.code_context[0])[0].split(',')
            msg = f"object [{parameters[0]}] not contain content[{parameters[1].strip()}]."
            cause = NonePointerException(msg)
        else:
            cause = throw

        flag = False
        # noinspection PyBroadException
        try:
            if not iterable_obj or content not in iterable_obj:
                flag = True
                raise_exception(cause)
        except BaseException:
            if flag:
                raise
            else:
                raise_exception(cause)

    @staticmethod
    def check_non_none(obj: _T, throw: BaseException = None):
        """
        if object only is None,will raise exception
        """
        if not issubclass(type(throw), BaseException):
            frame = getframeinfo(currentframe().f_back)
            parameters = findall(re.compile(r".*check_non_none[(](.*?)[)]", re.S), frame.code_context[0])
            msg = f"object [{parameters[0]}] is None."
            cause = NonePointerException(msg)
        else:
            cause = throw
        if obj is None:
            raise_exception(cause)

    @staticmethod
    def check_non_empty(obj: _T, throw: BaseException = None):
        """
        If the object is None, False, empty string "", 0, empty list[], empty dictionary{}, empty tuple(),
        will raise exception
        """
        if not issubclass(type(throw), BaseException):
            frame = getframeinfo(currentframe().f_back)
            parameters = findall(re.compile(r".*check_non_empty[(](.*?)[)]", re.S), frame.code_context[0])
            msg = f"object [{parameters[0]}] is empty."
            cause = NonePointerException(msg)
        else:
            cause = throw
        if not obj:
            raise_exception(cause)

    @staticmethod
    def none_of_default(src: _T, default: _T) -> _T:
        """
        Judge whether SRC is empty, and return the value of default if it is empty
        :param src: Object to be judged
        :param default: Default value
        """
        if src:
            return src
        return default

    @staticmethod
    def generate_random_str(length: int = 16, base_str: str = None) -> str:
        """
        Generates a random string of a specified length
        :params length: Length of generated string
        """
        if not issubclass(type(base_str), str):
            base_str = _base_str
        if len(base_str) == 0 or length == 0:
            return ""
        base_str_len = len(base_str)
        sb = StringBuilder()
        if length <= base_str_len:
            sb.append("".join(sample(base_str, length)))
        else:
            step = length // base_str_len
            remainder = length % base_str_len
            for _ in range(step):
                sb.append("".join(sample(base_str, base_str_len)))
            sb.append("".join(sample(base_str, remainder)))
        return sb.string()

    @staticmethod
    def get_current_function_name() -> str:
        """
        Gets the name of the current function inside the function
        """
        return stack()[1][3]

    @staticmethod
    def get_private_attribute(obj, name: str):
        """
        Gets the private property value of the object, and if it is a private method, returns the function object.
        """
        obj_name = obj.__class__.__name__
        for attribute in obj.__dir__():
            attr_name = f"_{obj_name}{name}"
            if obj_name in attribute and attr_name == attribute:
                return getattr(obj, attr_name)
        return None


__all__ = [ObjectsUtils]
