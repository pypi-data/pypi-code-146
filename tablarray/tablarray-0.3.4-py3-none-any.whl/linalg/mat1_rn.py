#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 16:37:02 2020

@author: chris
"""

import functools
import numpy as np

from .. import misc


def _mat1_rN_atc(func, min_cdim, *rv_cdims):
    """ATC-wrap for numpy.linalg of the form func(array)->array-like"""
    N_rval = len(rv_cdims)

    @functools.wraps(func)
    def wrapped_mat1_rN_atc(a, *args, **kwargs):
        if misc.istablarray(a):
            if (a.ts.cdim < min_cdim):
                raise np.linalg.LinAlgError(
                        '%d-dimensional array given.' % a.ts.cdim
                        + 'Array must be at least %d-dimensional' % min_cdim)
            rvals = func(a.cell, *args, **kwargs)
            assert len(rvals) == N_rval, '%d rvals, expected %d' % (
                    len(rvals), N_rval)
            rclass = a.__class__
            rval2 = [None] * N_rval
            for i in range(N_rval):
                # print(rv_cdims[i])
                # rval2[i] = rclass(rvals[i], rv_cdims[i], view=a.view)
                rval2[i] = misc._rval_once_a_ta(
                    rclass, rvals[i], rv_cdims[i], a.view)
            return tuple(rval2)
        else:
            return func(a, *args, **kwargs)
    return wrapped_mat1_rN_atc


eig = _mat1_rN_atc(np.linalg.eig, 2, 1, 2)
eigh = _mat1_rN_atc(np.linalg.eigh, 2, 1, 2)
slogdet = _mat1_rN_atc(np.linalg.slogdet, 2, 0, 1)
