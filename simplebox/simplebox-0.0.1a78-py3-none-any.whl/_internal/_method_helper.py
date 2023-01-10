#!/usr/bin/env python
# -*- coding:utf-8 -*-
from inspect import getfullargspec
from typing import Callable, Tuple, Dict, List

from . import _T
from ..exceptions import CallException


def run_call_back(call_func: Callable, origin_func: Callable, args: Tuple, kwargs: Dict) -> _T:
    try:
        if callable(call_func):
            spec = getfullargspec(call_func)
            new_kwargs = get_func_params(origin_func, args, kwargs)
            if "chain" in spec.args or (spec.kwonlydefaults and "chain" in spec.kwonlydefaults):
                if "chain" in new_kwargs:
                    chain = new_kwargs["chain"]
                else:
                    chain = {}
                return call_func(chain=chain)
            else:
                return call_func()
    except Exception as e:
        raise CallException(f"call back exception: {str(e)}")


def get_func_params(func: Callable, args: Tuple, kwargs: Dict) -> Dict:
    new_params = {}  # 将所有参数以dict形式保存
    arg_spec = getfullargspec(func)

    tmp_arg_names = arg_spec.args
    tmp_arg_values = __copy_args(args)
    tmp_kwarg_kvs = __copy_kwargs(kwargs)
    if len(tmp_arg_names) > 0 and len(tmp_arg_values) > 0:
        first_value = tmp_arg_values[0]
        if func.__qualname__.split(".")[0] == first_value.__class__.__name__:  # 即为类方法或实例方法,添加到字典中
            new_params[tmp_arg_names.pop(0)] = tmp_arg_values.pop(0)
    choice_args_values = tmp_arg_values[:len(tmp_arg_names)]
    no_choice_values = tmp_arg_values[len(tmp_arg_names):]

    tmp_arg_names_len = len(tmp_arg_names)
    choice_args_values_len = len(choice_args_values)
    if tmp_arg_names_len > choice_args_values_len:
        diff_num = tmp_arg_names_len - choice_args_values_len
        for i in range(diff_num, tmp_arg_names_len):
            value = tmp_kwarg_kvs[tmp_arg_names[i]]
            choice_args_values.insert(i, value)
            del tmp_kwarg_kvs[tmp_arg_names[i]]
    new_params.update(dict(zip(tmp_arg_names, choice_args_values)))  # 添加位置参数kv

    kw_defaults = arg_spec.kwonlydefaults
    if not kw_defaults:
        kw_defaults = {}
    kw_defaults_keys = kw_defaults.keys()
    must_need_value_keys = [i for i in arg_spec.kwonlyargs if i not in kw_defaults_keys]
    for key in kw_defaults_keys:  # 添加kwargs，如果用户传了，使用用户的参数，否则用默认值
        if key in kwargs:
            new_params[key] = kwargs[key]
            del tmp_kwarg_kvs[key]
        else:
            new_params[key] = kw_defaults[key]
    for key in must_need_value_keys:  # 这类关键字参数没有默认值，从剩余的参数中依次赋值
        if key not in new_params and key in kwargs:
            new_params[key] = kwargs[key]
        else:
            new_params[key] = None
    if arg_spec.varargs:
        new_params[arg_spec.varargs] = no_choice_values  # 将剩余的args参数复制给函数形参的args
    if arg_spec.varkw:
        new_params[arg_spec.varkw] = tmp_kwarg_kvs  # 将剩余的kwargs参数赋值给函数的形参kwargs
    return new_params


def __copy_args(args: Tuple or List) -> List:
    tmp_args = []
    tmp_args_append = tmp_args.append
    for arg in args:
        tmp_args_append(arg)
    return tmp_args


def __copy_kwargs(kwargs: Dict) -> Dict:
    tmp_kwargs = {}
    for k, v in kwargs.items():
        tmp_kwargs[k] = v
    return tmp_kwargs
