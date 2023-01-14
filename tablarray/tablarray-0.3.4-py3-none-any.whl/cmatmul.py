#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 17:25:40 2020

@author: chris
"""

import numpy as np

from . import mmul
from .mmul_sig import mmul_ta_signature


def cummatmul(a, axis):
    """Given an ATC object, return the cumulative matmul
    (matrix multiplication) of the cells along the given tabular axis
    Always implies cumulative axis is one of ts.tshape."""
    a = mmul_ta_signature(a, mxdim=2)
    # get a blank ATC for the result
    rarray = np.zeros(a.base.shape, dtype=a.base.dtype)
    rclass = a.__class__
    new_atc = rclass(rarray, a.ts.cdim, a.view)
    # get a table view of the result ATC
    new_table = new_atc.table
    # table view of the atc input
    table = a.table
    # prep for loop
    N_iter = table.shape[axis]
    slice0 = [slice(None)] * table.ndim
    slice1 = [slice(None)] * table.ndim
    # loop over table across this axis
    slice0[axis] = 0
    new_table[slice0] = table[slice0]
    for i in range(1, N_iter):
        slice0[axis] = i - 1
        slice1[axis] = i
        new_table[slice1] = mmul.matmul(table[slice1], new_table[slice0])
    return new_table
