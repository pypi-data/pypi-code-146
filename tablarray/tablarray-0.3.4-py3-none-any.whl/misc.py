#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities that tend to get used front and back (IO) of tablarray functions

Created on Sun Jan  3 15:34:31 2021

@author: chris
"""

import numpy as np
from .tashape import taShape
from . import np2ta


def istablarray(a):
    """returns True/False if argument appears to fulfill TablArray class"""
    return (hasattr(a, 'ts') and hasattr(a, 'view') and hasattr(a, 'base')
            and hasattr(a, 'base') and hasattr(a, 'bcast'))


def istablaset(a):
    """returns True/False if argument appears to fulfill TablaSet class"""
    return (hasattr(a, '_tablarrays') and hasattr(a, 'ts') and hasattr(a, 'keys')
            and hasattr(a, 'keys') and hasattr(a, 'bcast'))


def base(a):
    """returns .base if argument is tablarray else pass-through a"""
    return a.base if istablarray(a) else a


def imply_zeros(a, *args):
    """based on TablArray inputs, """
    ts0 = taShape((), 0)
    ts, bc = a.ts.combine(ts0)
    for arg in args:
        ts, bc = ts.combine(arg.ts)
    # now make zeros with ts
    return np2ta.zeros((*ts.tshape, *ts.cshape), ts.cdim)


def _rval_once_a_ta(rclass, rval, cdim, view):
    """"""
    if rval.ndim == cdim:
        return rval
    return rclass(rval, cdim, view)


def _rval_always_ta(rclass, rval, cdim, view):
    return rclass(rval, cdim, view)


def _imply_shape(ll):
    """given a list [of list ...] of something

    recursively imply that ndim is the depth of the lists
    """
    if type(ll) is not list:
        return ()
    return len(ll), *_imply_shape(ll[0])


def _imply_shape_ragged(ll):
    """given a possibly-ragged list [of list ...] of something

    recursively imply the required padded shape

    Note: Ragged recursion means reaching every element so this doesn't scale
    well.
    """
    if type(ll) is list:
        sub_shapes = []
        for row in ll:
            sub_shape = _imply_shape_ragged(row)
            if sub_shape is not None:
                sub_shapes.append(sub_shape)
        n = len(sub_shapes)
        mx_sub_shape = ()
        if n >= 1:
            mx_sub_shape = sub_shapes[0]
        for a in range(n):
            mx_sub_shape = np.maximum(mx_sub_shape, sub_shapes[a])
        return len(ll), *mx_sub_shape
    else:
        return None


def _get_1st_obj(ll):
    """given a list [of list ...] of something

    get the first non-list object
    """
    if type(ll) is not list:
        return ll
    return _get_1st_obj(ll[0])
