#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:01:14 2020

@author: chris
"""

import functools


def op12_swap(func):
    """wrapper swaps arg12 of func(arg1, arg2, ...)"""
    @functools.wraps(func)
    def wrapper_op12_swap(arg1, arg2, *args, **kwargs):
        return func(arg2, arg1, *args, **kwargs)
    return wrapper_op12_swap
