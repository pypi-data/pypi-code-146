#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:22:26 2020

@author: chris
"""

import functools
import numpy as np

from .. import ta


def _atc_new(func):
    """decorator for ATC compatibility for new numpy generators,
    but I'm not so sure I should use a decorator or even have the same names
    the thing is that this decorator changes the input args..."""
    @functools.wraps(func)
    def wrapper_atc_new(shape, cdim, view='cell', **kwargs):
        rarray = func(shape, **kwargs)
        return ta.TablArray(rarray, cdim, view=view)
    return wrapper_atc_new


empty = _atc_new(np.empty)
ones = _atc_new(np.ones)
zeros = _atc_new(np.zeros)
# full wouldn't have exaclty the same wrapper
