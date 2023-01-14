#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import TypeVar, Dict, List, Callable

from ._hook import _run_hook_func, _get_chain

_TDict = TypeVar("_TDict", bound=Dict)


def around_impl(func: Callable, befores: List[Callable] or Callable = None, afters: List[Callable] or Callable = None,
                catch: bool = False, *args, **kwargs):
    chain, func_new_kwargs = _get_chain(func, args, kwargs)
    _run_hook_func(befores, chain, func_new_kwargs)
    # noinspection PyBroadException
    try:
        result = func(*args, **kwargs)
        return result
    except BaseException as e:
        if not catch:
            raise e
    finally:
        _run_hook_func(afters, chain, func_new_kwargs)
