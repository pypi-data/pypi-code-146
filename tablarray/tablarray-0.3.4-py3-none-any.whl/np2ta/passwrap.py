#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 16:13:17 2022

@author: chris
"""

import functools

from .. import misc


def _wrap_array_passthrough(func):
    """
    passthrough wrapper, to extract .base from any TablArray found
    in any *args, **kwargs
    """
    @functools.wraps(func)
    def wrap_a_pthrough(*args, **kwargs):
        args2 = []
        kwargs2 = {}
        for arg in args:
            args2.append(arg.base if misc.istablarray(arg) else arg)
        for key, val in kwargs.items():
            kwargs2[key] = val.base if misc.istablarray(val) else val
        func(*tuple(args2), **kwargs2)
    wrap_a_pthrough.__doc__ = (
        "**TablArray compatible (passthrough)** %s\n\n" % func.__name__
        + wrap_a_pthrough.__doc__)
    return wrap_a_pthrough
