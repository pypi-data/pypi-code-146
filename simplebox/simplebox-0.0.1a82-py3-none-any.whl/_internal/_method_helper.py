#!/usr/bin/env python
# -*- coding:utf-8 -*-
from inspect import getfullargspec
from typing import Callable, Tuple, Dict

from . import _T
from ..exceptions import CallException

_self, _cls, _chain = "self", "cls", "chain"


def run_call_back(call_func: Callable, origin_func: Callable, args: Tuple, kwargs: Dict) -> _T:
    try:
        if callable(call_func):
            spec = getfullargspec(call_func)
            new_kwargs = get_func_params(origin_func, args, kwargs)
            if _chain in spec.args or (spec.kwonlydefaults and _chain in spec.kwonlydefaults):
                if _chain in new_kwargs:
                    chain = new_kwargs[_chain]
                else:
                    chain = {}
                return call_func(chain=chain)
            else:
                return call_func()
    except Exception as e:
        raise CallException(f"call back exception: {str(e)}")


def get_func_params(func: Callable, args: Tuple, kwargs: Dict) -> Dict:
    new_params = {}  # 将所有参数以dict形式保存
    spec = getfullargspec(func)

    if len(spec.args) > 0 and len(args) > 0:
        if (spec.args[0] == _self and func.__qualname__.split(".")[0] == args[0].__class__.__name__) or \
                (spec.args[0] == _cls and func.__qualname__.split(".")[0] == args[0].__name__):
            new_params[spec.args[0]] = args[0]
    if _chain in kwargs:
        new_params[_chain] = kwargs.get(_chain)
    return new_params
