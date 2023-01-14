#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module collection of functions for stacking and splitting TablArrays

Created on Thu Feb 24 20:15:45 2021

@author: chris
"""

import functools
import numpy as np

from . import misc
from .np2ta import cbroadcast
import tablarray as ta


def _cast_other_types(arrays, view=None):
    """
    mixing of types
    ---------------
    Always return:

    1. all TablArray (alignment depends on view)
    2. or all ndarray
    """
    first_ta = None
    for a in arrays:
        if misc.istablarray(a):
            first_ta = a
            break
    if type(arrays) is not list:
        arrays = list(arrays)
    if first_ta is None:
        # if no arrays are TablArray type
        for i in range(len(arrays)):
            if type(arrays[i]) is not np.ndarray:
                # cast all to ndarray type
                arrays[i] = np.array(arrays[i])
    else:
        # at least one array is TablArray type
        if view is None:
            view = first_ta.view
        for i in range(len(arrays)):
            a = arrays[i]
            if not misc.istablarray(a):
                # cast all to TablArray type
                a = np.array(a)
                if view == 'cell':
                    cdim = max(first_ta.ts.cdim, a.ndim)
                else:
                    # if the first array is tabular, lists broadcast to tabular
                    cdim = 0
                arrays[i] = ta.TablArray(a, cdim, view=view)
    return arrays


def _wrap_stackers(func, newdim=True):
    """wrapper for considering TablArray's in numpy's stacking and
    concatenating functions"""
    @functools.wraps(func)
    def fstacker_wrapped(arrays, axis=0, out=None, *args, **kwargs):
        arrays = _cast_other_types(arrays)
        if misc.istablarray(arrays[0]):
            view = arrays[0].view
            cdim = arrays[0].ts.cdim
            tdim = arrays[0].ts.tdim
            # determine cdim and axis, considering view
            if view == 'cell':
                if newdim:
                    cdim += 1
                if axis >= 0:
                    axis += tdim
            elif view == 'table' or view == 'bcast':
                if axis < 0:
                    axis -= cdim
            # use numpy.stack to execute on .base of the arrays
            basarrays = []
            for a in arrays:
                basarrays.append(a.base)
            rarray = func(basarrays, axis, out, *args, **kwargs)
            rclass = arrays[0].__class__
            return rclass(rarray, cdim)
        else:
            # fall back on numpy for non-TablArray type
            return func(arrays, axis, out, *args, **kwargs)
    fstacker_wrapped.__doc__ = (
        "**TablArray compatible** %s\n\n" % func.__name__
        + fstacker_wrapped.__doc__)
    return fstacker_wrapped


# stacking functions from numpy wrapped for TablArray compatibility
stack = _wrap_stackers(np.stack, newdim=True)
concatenate = _wrap_stackers(np.concatenate, newdim=False)
vstack = _wrap_stackers(np.vstack, newdim=False)
hstack = _wrap_stackers(np.hstack, newdim=False)


class _tup_bcast(object):
    def __init__(self):
        self.dtype = 'bool'
        self.shape = ()

    def bcast(self, dtype_i, shape_i):
        # determine the new shape
        newshape, _, _ = cbroadcast.broadcast_shape(
            self.shape, shape_i)
        self.shape = tuple(newshape)
        # determine the new type
        self.dtype = cbroadcast._prioritize_dtype(None, self.dtype, dtype_i)


class _tarrays_bcast(object):
    def __init__(self):
        self.dtype = 'bool'
        self.tshape = ()
        self.cshape = ()

    def bcast(self, dtype, ts):
        # determine the new shape
        newtshape, _, success = cbroadcast.broadcast_shape(
            self.tshape, ts.tshape)
        if not success:
            raise ValueError('incompatible broadcast shapes')
        newcshape, _, success = cbroadcast.broadcast_shape(
            self.cshape, ts.cshape)
        if not success:
            raise ValueError('incompatible broadcast shapes')
        self.tshape = tuple(newtshape)
        self.cshape = tuple(newcshape)
        # determine the new type
        self.dtype = cbroadcast._prioritize_dtype(None, self.dtype, dtype)


def stack_bcast(arrays, axis=0, out=None, view=None):
    """
    Join a sequence of arrays along a new axis, follow broadcasting rules if
    possible to mesh conflicting shapes (all arrays must be broadcast-able).

    TablArray will interpret axis per the current view of the first array::

        >>> a = ta.TablArray([1, 0], 0)
        >>> b = ta.TablArray([[2, 1], [3, 2]], 1)
        >>> # axis=0 will be along cellular cdim
        >>> stack_bcast((a.cell, b), axis=0)
        [|[[1. 0.] |
         | [2. 1.]]|

         |[[1. 0.] |
         | [3. 2.]]|]t(2,)|c(2, 2)
        >>> # axis=-1 will be along tabular tdim
        >>> stack_bcast((a.table, b), axis=-1)
        [[|[1. 0.]|
          |[2. 1.]|]

         [|[1. 0.]|
          |[3. 2.]|]]t(2, 2)|c(2,)
        >>> # broadcasted stacking also works with ndarray types
        >>> stack_bcast((a.base, b.base), axis=1)
        array([[[1, 0],
                [2, 1]],

               [[1, 0],
                [3, 2]]])

    Parameters
    ----------
    arrays : tuple, sequence of TablArrays or array-like
        Arrays to be stacked.
    axis : int, optional
        The axis in the result array along which the input arrays are stacked.
        Default is 0.
    out : TablArray or ndarray, optional
        If provided, the destination to place the result.
    view : 'cell', 'table'
        If provided, use this view instead of inferring from the first array.

    Returns
    -------
    stacked : TablArray or array
        The array formed by stacking.
    """
    arrays = _cast_other_types(arrays, view)
    n = len(arrays)
    if misc.istablarray(arrays[0]):
        # method for TablArray objects
        if view is None:
            view = arrays[0].view
        bc = _tarrays_bcast()
        # find the broadcasted shape and dtype
        for a in arrays:
            bc.bcast(a.dtype, a.ts)
        # determine cdim and axis, considering view
        if view == 'cell':
            cdim = len(bc.cshape) + 1
            if axis >= 0:
                axis += len(bc.tshape)
            # there are some boundary checks to consider
            # if axis >= cdim:
            #    raise ValueError('axis %d is out of cdim %d' % (axis, cdim))
        elif view == 'table' or view == 'bcast':
            cdim = len(bc.cshape)
            if axis < 0:
                axis -= cdim
        ndim = len(bc.tshape) + len(bc.cshape) + 1
        if axis < 0:
            # convert negative axis values
            axis += ndim
        newshape = list(bc.tshape) + list(bc.cshape)
        newshape.insert(axis, n)
        # print(bc.tshape, bc.cshape)
        # print(newshape)
        # create out array, if it wasn't given to us
        if out is None:
            out = ta.TablArray(np.zeros(newshape), cdim, view=view)
        elif out.base.shape != tuple(newshape):
            raise ValueError('out.base shape %s mismatches required shape %s'
                             % (out.base.shape, newshape))
        outarray = out.base
    else:
        # method for TablArray objects
        bc = _tup_bcast()
        for a in arrays:
            bc.bcast(a.dtype, a.shape)
        ndim = len(bc.shape) + 1
        if axis < 0:
            # convert negative axis values
            axis += ndim
        newshape = list(bc.shape)
        newshape.insert(axis, n)
        if out is None:
            out = np.zeros(newshape, bc.dtype)
        elif out.shape != tuple(newshape):
            raise ValueError('out shape %s mismatches required shape %s'
                             % (out.shape, newshape))
        outarray = out
    # slot arrays into place in the out array
    slice0 = [slice(None)] * axis
    slice1 = [slice(None)] * (ndim - axis - 1)
    for i in range(n):
        a = arrays[i]
        # print(tuple(slice0 + [i] + slice1))
        outarray.__setitem__(tuple(slice0 + [i] + slice1), a)
    return out
