#!/usr/bin/env python
# -*- coding:utf-8 -*-
from inspect import getfullargspec
from typing import Callable, Dict, List

from simplebox._internal._method_helper import get_func_params
from simplebox.exceptions import NonePointerException


def _get_chain(func, args, kwargs) -> (Dict, Dict):
    func_new_kwargs = get_func_params(func, args, kwargs)
    if "chain" in func_new_kwargs:
        chain = func_new_kwargs.get("chain")
        if chain is None:
            raise NonePointerException(f"'{func.__name__}''s params 'chain' is None")
    else:
        chain = {}
    return chain, func_new_kwargs


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


def _build_new_params(kwargs: Dict) -> (List, Dict):
    t_args = []
    if "args" in kwargs:
        t_args = kwargs.pop("args")
    t_kwargs = {}
    if "kwargs" in kwargs:
        t_kwargs.update(kwargs.pop("kwargs"))
    t_kwargs.update(kwargs)
    return t_args, t_kwargs
