#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module collection of functions for reshaping and flattening.

Created on Wed Jan  6 23:53:54 2021

@author: chris
"""

import numpy as np

from . import misc


def reshape(a, newshape, order='C'):
    """Gives a new shape to a TablArray (or array) without changing its data.
    If possible, return a view not a copy

    TablArray reshaping will occur along the current view::

        reshape(a.cell, (2, 2))     # (2, 2) is the new cellular shape
        reshape(a.table, (5, 1))    # (5, 1) is the new tabular shape

    Parameters
    ----------
    a: tablarray_like
        Array to be reshaped.

    newshape: int or tuple of ints
        The new shape. See numpy.reshape

    order: {'C', 'F', 'A'}, optional
        See numpy.reshape
    """
    if not misc.istablarray(a):
        # just fall back on np.reshape if a is not TablArray
        return np.reshape(a, newshape, order=order)

    rclass = a.__class__
    if a.view == 'table' or a.view == 'bcast':
        # reshape only the table
        tl_shape = (*newshape, *a.ts.cshape)
        rarray = np.reshape(a.base, tl_shape, order)
        return rclass(rarray, a.ts.cdim, a.view)
    if a.view == "cell":
        # reshape only the cell
        tl_shape = (*a.ts.tshape, *newshape)
        rarray = np.reshape(a.base, tl_shape, order)
        return rclass(rarray, len(newshape), a.view)
    if a.view == "array":
        # reshape the whole thing
        rarray = np.reshape(a.base, newshape, order)
        cdim = min(a.ts.cdim, len(newshape))
        return rclass(rarray, cdim, a.view)

    raise ValueError('unknown view "%s"' % a.view)


def ravel(a, order='C'):
    """Return a flattened array, returning a view not a copy

    TablArray will ravel along the current view::

        ravel(a.cell)     # ravels all the cells
        ravel(a.table)    # ravels the table
        ravel(a.array)    # ravels it all

    Parameters
    ----------
    a: tablarray_like
        Array to be reshaped.

    order: {'C', 'F', 'A'}, optional
        See numpy.ravel
    """
    if not misc.istablarray(a):
        # just fall back on np.ravel if a is not TablArray
        return np.ravel(a, order=order)

    numel = np.product(a.shape)
    return reshape(a, (numel,), order=order)


def tile(a, reps):
    """
    Cunstruct a larger TablArray by repeating a.

    TablArray will tile along the current view::

        tile(a.cell, (2, 1))    # tile all cells by (2, 1)x
        tile(a.table, (3))      # tile the table by (3)x

    Parameters
    ----------
    a : TablArray or array-like
        the input array
    reps : tuple
        the number of repetitions of a along each axis

    Returns
    -------
    c : TablArray or ndarray
    """
    if not misc.istablarray(a):
        # just fall back on np.tile if a is not TablArray
        return np.tile(a, reps)

    if a.view == 'table' or a.view == 'bcast':
        tl_reps = (*reps, *a.ts.cshape)
    elif a.view == 'cell':
        tl_reps = (*a.ts.tshape, *reps)
    elif a.view == 'array':
        tl_reps = reps
    else:
        raise ValueError('unknown view %s' % a.view)

    rarray = np.tile(a.base, tl_reps)
    rclass = a.__class__
    return rclass(rarray, a.ts.cdim, a.view)
