#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Callable


def raise_exception(cause: BaseException, call: Callable = None):
    """
    Actively throws exceptions.
    :param cause: With the exception object thrown
    :param call: The callback function that executes before the exception is thrown
    """
    if callable(call):
        call()
    if issubclass(type(cause), BaseException):
        raise cause
    raise BasicException(str(cause))


class BasicException(Exception):
    """
    Simplebox exception base class.
    """

    def __init__(self, *args):
        super().__init__(*args)


class CallException(BasicException):
    """
    Call function exception.
    """

    def __init__(self, *args):
        super().__init__(*args)


class TimeoutExpiredException(BasicException):
    """
    Timeout exception.
    """

    def __init__(self, *args):
        super().__init__(*args)


class HttpException(BasicException):
    """
    Http exception.
    """

    def __init__(self, *args):
        super().__init__(*args)


class ArgumentException(BasicException):
    """
    argument exception.
    """

    def __init__(self, *args):
        super().__init__(*args)


class TypeException(BasicException):
    """
    Type exception.
    """

    def __init__(self, *args):
        super().__init__(*args)


class NonePointerException(BasicException):
    """
    None exception.
    if obj is None can raise NonePointerException.
    """

    def __init__(self, *args):
        super().__init__(*args)


class EmptyException(BasicException):
    """
    Empty exception.
    If the object is None, False, empty string "", 0, empty list[], empty dictionary{}, empty tuple(),
    will raise NonePointerException.
    """

    def __init__(self, *args):
        super().__init__(*args)


class InstanceException(BasicException):
    """
    Instance exception.
    """

    def __init__(self, *args):
        super().__init__(*args)


__all__ = [BasicException, CallException, TimeoutExpiredException, HttpException, ArgumentException,
           TypeException, NonePointerException, InstanceException, raise_exception]
