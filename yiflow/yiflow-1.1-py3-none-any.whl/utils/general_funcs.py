#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        : utils.py
@Description : 一些工具函数
@Date        : 2020/10/29 11:39:17
@Author      : merlinbao
@Version     : 1.0
"""

import os
from colorama import Fore, Style


def wrap_title(text):
    return Fore.GREEN + str(text) + Style.RESET_ALL


def wrap_link(text):
    return Fore.RED + str(text) + Style.RESET_ALL


def make_list_flat(string, keys):
    def _flat(string, key):
        new_string = ''
        left, right = 0, 0
        try:
            pos = string.index(key)
            left = pos + string[pos:].index('[')
            right = pos + string[pos:].index(']')
            new_string = string[:left] + string[left:right].replace('\n', '').replace(' ', '').replace(',', ', ')
            new_string += _flat(string[right:], key)
        except ValueError:
            new_string += string[right:]
        return new_string

    for key in keys:
        string = _flat(string, key)

    return string


def get_proj_dir():
    return os.getenv('YF_PROJ_PATH').replace('\\', '/')