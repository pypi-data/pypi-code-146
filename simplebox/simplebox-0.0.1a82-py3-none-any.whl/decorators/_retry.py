#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from time import time, sleep
from typing import Type, Callable, Dict

from ._hook import _get_chain, _run_hook_func
from .._internal import _T
from .._internal._method_helper import run_call_back
from ..log._factory import LoggerFactory

__logger = LoggerFactory.get_logger("retry")


def retry(timeout: int = 60, interval: int = 1, increasing: int = 0, check: Callable[[_T], bool] = lambda r: r,
          ignore_exception: Type[Exception] = None, post_hook: Callable[[_T, _T], None] = None):
    """
    Provides retry functionality.
    unit second

    callback functions can and only support communication via the chain keyword parameter. example: callback() is ok,
    callback(chain=None) is ok, callback(chain=None, other=None) is ok(other arg will not be assigned), callback(other, chain=None) will happend exception

    :param check: Check whether the result is as expected, return the result if it is met, otherwise try again.
    :param ignore_exception: If it is the exception and its child exceptions, no retry is made
    :param post_hook: If the original function is not executed.Two parameters are required, func_params and func_return
    the callback function is executed and the result of the callback function is returned,
    arguments to the original function are passed to the callback function
    :param timeout: the timeout period after which the timeout exits the retries.
    :param interval: retry interval.
    :param increasing: The incrementing interval
    """

    def _inner(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            chain, func_new_kwargs = _get_chain(func, args, kwargs)
            start = time()
            _interval = interval
            num = 1
            while time() - start < timeout:
                # noinspection PyBroadException
                try:
                    result = func(*args, **kwargs)
                    if check(result):
                        return result
                    else:
                        __logger.warning(f"check result fail!!!")
                    __logger.info(f"run function '{func.__name__}' fail: retrying {num} time(s)")
                    sleep(_interval)
                    num += 1
                    _interval += increasing
                except BaseException as e:
                    if ignore_exception and issubclass(type(e), ignore_exception):
                        break
                    __logger.info(f"run function '{func.__name__}' exception {type(e).__name__}: {str(e)}. retrying {num} time(s)")
                    sleep(_interval)
                    num += 1
                    _interval += increasing
            else:
                if post_hook:
                    _run_hook_func([post_hook], chain, func_new_kwargs)

        return _wrapper

    return _inner


def retrying(func: Callable, func_kwargs: Dict = None, timeout: int = 60, interval: int = 1, increasing: int = 0,
             check: Callable[[_T], bool] = lambda r: r,
             ignore_exception: Type[Exception] = None, post_hook: Callable[[_T, _T], None] = None):
    """

    :param func: The function to be retried.
    :param func_kwargs: The parameters of the function to be retried must be provided as keyword arguments.
    :param check: Check whether the result is as expected, return the result if it is met, otherwise try again.
    :param ignore_exception: If it is the exception and its child exceptions, no retry is made
    :param post_hook: If the original function is not executed.Two parameters are required, func_params and func_return
    the callback function is executed and the result of the callback function is returned,
    arguments to the original function are passed to the callback function
    :param timeout: the timeout period after which the timeout exits the retries.
    :param interval: retry interval.
    :param increasing: The incrementing interval
    :return:
    """
    start = time()
    _interval = interval
    num = 1
    while time() - start < timeout:
        # noinspection PyBroadException
        try:
            if func_kwargs:
                result = func(**func_kwargs)
            else:
                result = func()
            if check(result):
                return result
            else:
                __logger.warning(f"check result fail!!!")
            __logger.info(f"run function '{func.__name__}' fail: retrying {num} time(s)")
            sleep(_interval)
            num += 1
            _interval += increasing
        except BaseException as e:
            if ignore_exception and issubclass(type(e), ignore_exception):
                break
            __logger.info(f"run function '{func.__name__}' exception {type(e).__name__}: {str(e)}. retrying {num} time(s)")
            sleep(_interval)
            num += 1
            _interval += increasing
    else:
        if post_hook:
            if func_kwargs:
                run_call_back(post_hook, func, tuple(), func_kwargs)
            else:
                post_hook({}, {})


__all__ = [retry, retrying]
