#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 17:10:44 2020

@author: chris
"""

import functools
import numpy as np

from .. import misc


def _axial_broadcast(func):
    """ACT compatibility for unary operands where one or more axes transform
    to a scalar (axis -> scalar)"""
    @functools.wraps(func)
    def wrap_ax_bcast(a, axis=None, **kwargs):
        if misc.istablarray(a):
            if axis is None:
                axis = a._viewdims
                cdim = a._viewcdim
            else:
                if type(axis) is tuple:
                    axis = tuple(np.array(a._viewdims)[list(axis)])
                else:
                    axis = a._viewdims[axis]
                if a._cellular:
                    # if one of the cellular dims collapses to a scalar,
                    # then cdims will decrease
                    if np.isscalar(axis):
                        cdim = a.ts.cdim - 1
                    else:
                        cdim = a.ts.cdim - len(axis)
                else:
                    # if one of the tabular dims collapses to a scalar,
                    # the number of cdims is unchanged
                    cdim = a.ts.cdim
            rarray = func(a.base, axis=axis, **kwargs)
            rclass = a.__class__  # probably TablArray
            # once a TablArray, usually a TablArray
            return misc._rval_once_a_ta(rclass, rarray, cdim, a.view)
        else:
            # just passthrough
            return func(a, axis=axis, **kwargs)
    return wrap_ax_bcast


# these are also available as methods
all = _axial_broadcast(np.all)
any = _axial_broadcast(np.any)
argmax = _axial_broadcast(np.argmax)
argmin = _axial_broadcast(np.argmin)
max = _axial_broadcast(np.max)
mean = _axial_broadcast(np.mean)
min = _axial_broadcast(np.min)
prod = _axial_broadcast(np.prod)
std = _axial_broadcast(np.std)
sum = _axial_broadcast(np.sum)

# these are only available here - not as methods
amax = _axial_broadcast(np.amax)
amin = _axial_broadcast(np.amin)
median = _axial_broadcast(np.median)
nanargmax = _axial_broadcast(np.nanargmax)
nanargmin = _axial_broadcast(np.nanargmin)
nanmax = _axial_broadcast(np.nanmax)
nanmean = _axial_broadcast(np.nanmean)
nanmedian = _axial_broadcast(np.nanmedian)
nanmin = _axial_broadcast(np.nanmin)
nanprod = _axial_broadcast(np.nanprod)
nansum = _axial_broadcast(np.nansum)
nanstd = _axial_broadcast(np.nanstd)
nanvar = _axial_broadcast(np.nanvar)
var = _axial_broadcast(np.var)
