#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from typing import List

_options_hook_func = ["__sb_log", "__sb_rest"]


def __config_parser(args: List, instance):
    args.pop(0)
    if not args or len(args) != 1:
        return
    prefix = f"_{instance.__class__.__name__.replace('_', '')}__set_"
    for arg in re.split(";", args[0]):
        kv = arg.split(":")
        if len(kv) < 2:
            continue
        key, value = kv
        getattr(instance, f"{prefix}{key.replace('-', '_')}")(value)


'''
The hook function name for each configuration item of the framework begins with "__sb"
'''


def __sb_log(args: List):
    from simplebox.config._log_config import LogConfig
    __config_parser(args, LogConfig)


def __sb_rest(args: List):
    from simplebox.config._rest_config import RestConfig
    __config_parser(args, RestConfig)
