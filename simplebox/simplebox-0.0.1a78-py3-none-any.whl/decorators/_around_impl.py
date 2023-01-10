#!/usr/bin/env python
# -*- coding:utf-8 -*-
from inspect import getfullargspec
from typing import TypeVar, Dict, List, Callable, Tuple

from .._internal._method_helper import get_func_params
from ..exceptions import NonePointerException

_TDict = TypeVar("_TDict", bound=Dict)


def around_impl(func: Callable, befores: List[Callable] or Callable = None, afters: List[Callable] or Callable = None,
                catch: bool = False, *args, **kwargs):

    func_new_kwargs = get_func_params(func, args, kwargs)
    if "chain" in func_new_kwargs:
        chain = func_new_kwargs.get("chain")
        if chain is None:
            raise NonePointerException(f"'{func.__name__}''s params 'chain' is None")
    else:
        chain = {}
    _run_hook_func(befores, chain, func_new_kwargs)
    # noinspection PyBroadException
    try:
        t_args = []
        if "args" in func_new_kwargs:
            t_args = func_new_kwargs.pop("args")
        t_kwargs = {}
        if "kwargs" in func_new_kwargs:
            t_kwargs.update(func_new_kwargs.pop("kwargs"))
        t_kwargs.update(func_new_kwargs)
        result = func(*t_args, **t_kwargs)
        return result
    except BaseException as e:
        if not catch:
            raise e
    finally:
        _run_hook_func(afters, chain, func_new_kwargs)


def _run_hook_func(call_obj: List[Callable] or Callable, chain: Dict, func_kwargs: Dict) -> Dict:
    if not call_obj:
        return {}
    call_list = []
    if issubclass(type(call_obj), List):
        call_list.extend(call_obj)
    else:
        call_list.append(call_obj)
    for call in call_list:
        func_type_name = type(call).__name__
        hook_params = {}
        if func_type_name == "method" or func_type_name == "function":
            assert callable(call), f"'{func_type_name}' not a callable"
            __hook_params(call, hook_params, func_kwargs, chain)
            call(**hook_params)
        else:
            assert hasattr(call, "__func__"), f"'{func_type_name}' not a callable"
            __hook_params(call.__func__, hook_params, func_kwargs, chain)
            call.__func__(**hook_params)
    if "chain" in func_kwargs:
        func_kwargs["chain"] = chain


def __hook_params(call: Callable, params_map: Dict, func_new_kwargs: Dict, chain: Dict):
    spec = getfullargspec(call)
    if "chain" in spec.args or (spec.kwonlydefaults and "chain" in spec.kwonlydefaults):
        params_map["chain"] = chain
    if len(spec.args) > 0:
        if spec.args[0] == "self":
            if "self" in func_new_kwargs:
                if call.__qualname__.split(".")[0] == func_new_kwargs.get("self").__class__.__name__:
                    params_map["self"] = func_new_kwargs.get("self")
        elif spec.args[0] == "cls":
            if "self" in func_new_kwargs:
                if call.__qualname__.split(".")[0] == func_new_kwargs.get("self").__class__.__name__:
                    params_map["cls"] = func_new_kwargs.get("self").__class__
            elif "cls" in func_new_kwargs:
                if call.__qualname__.split(".")[0] == func_new_kwargs.get("cls").__name__:
                    params_map["cls"] = func_new_kwargs.get("cls")
