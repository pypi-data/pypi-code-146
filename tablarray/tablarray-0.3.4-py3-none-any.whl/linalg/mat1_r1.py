#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 14:07:30 2020

@author: chris
"""

import functools
import numpy as np

from .. import misc


def _mat1_r1_atc(func, min_cdim, rval_cdim):
    """ATC-wrap for numpy.linalg of the form func(array)->array-like"""
    @functools.wraps(func)
    def wrapped_mat1_r1_atc(a, *args, **kwargs):
        if misc.istablarray(a):
            if (a.ts.cdim < min_cdim):
                raise np.linalg.LinAlgError(
                        '%d-dimensional array given.' % a.ts.cdim
                        + 'Array must be at least %d-dimensional' % min_cdim)
            rarray = func(a.cell, *args, **kwargs)
            rclass = a.__class__
            return misc._rval_once_a_ta(rclass, rarray, rval_cdim, a.view)
            # return rclass(rarray, rval_cdim, view=a.view)
        else:
            return func(a, *args, **kwargs)
    return wrapped_mat1_r1_atc


# func(matrix)->scalar; i.e. cdim=0
det = _mat1_r1_atc(np.linalg.det, min_cdim=2, rval_cdim=0)
cond = _mat1_r1_atc(np.linalg.cond, min_cdim=2, rval_cdim=0)

# func(matrix)->vector; i.e. cdim=1
eigvals = _mat1_r1_atc(np.linalg.eigvals, min_cdim=2, rval_cdim=1)
eigvalsh = _mat1_r1_atc(np.linalg.eigvalsh, min_cdim=2, rval_cdim=1)

# func(matrix)->matrix; i.e. cdim=2
cholesky = _mat1_r1_atc(np.linalg.cholesky, min_cdim=2, rval_cdim=2)
inv = _mat1_r1_atc(np.linalg.inv, min_cdim=2, rval_cdim=2)
matrix_power = _mat1_r1_atc(np.linalg.matrix_power, min_cdim=2, rval_cdim=2)

# func(array)->scalar
matrix_rank = _mat1_r1_atc(np.linalg.matrix_rank, min_cdim=1, rval_cdim=0)
