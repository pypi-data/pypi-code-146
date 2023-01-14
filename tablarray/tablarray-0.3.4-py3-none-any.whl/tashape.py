#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:58:10 2020

@author: chris
"""

import copy
import numpy as np

from .np2ta import cbroadcast


class taShape(object):
    """given an array and cellular ndim, return derived attributes object"""
    def __init__(self, shape, cdim):
        self.cdim = cdim
        self.tdim = len(shape) - cdim
        self.cshape = shape[self.tdim:]     # cellular shape
        self.csize = np.prod(self.cshape)   # cellular number of elements
        self.tshape = shape[:self.tdim]     # tabular shape
        self.tsize = np.prod(self.tshape)   # tabular number of elements

    def __str__(self):
        return 't%s|c%s' % (self.tshape, self.cshape)

    def combine(self, other):
        """combine - the new shape after broadcast of 2,
        None if incompatible"""
        bc = cbroadcast.CellBroadcast.from_tshapes(self, other)
        new_shape = taShape(tuple(bc.new_shape), bc.new_cdim) if bc.valid else None
        return new_shape, bc

    def cslice(self, indices):
        """align slice indices only to the cellular structure,
        spanning :,... across all tabular dimensions"""
        cslice = indices
        # calculate cdim for cellular aligned slice
        cdim = self.cdim
        for idx in cslice:
            if idx != slice(None):
                cdim -= 1
        assert len(cslice) <= self.cdim, (
                'got len(*cslice)==%d instead of required <=%d'
                % (len(cslice), self.cdim))
        tspan = [slice(None)] * self.tdim
        spanning_slice = tspan + cslice
        return spanning_slice, cdim

    def tslice(self, indices):
        """align slice indices only to the cellular structure,
        spanning :,... across all tabular dimensions"""
        # cdim is unchanged
        cdim = self.cdim
        tslice = indices
        assert len(tslice) <= self.tdim, (
                'got len(*tslice)==%d instead of required <=%d'
                % (len(tslice), self.tdim))
        cspan = [slice(None)] * self.cdim
        spanning_slice = tslice + cspan
        return spanning_slice, cdim

    def bcast(self, indx):
        """"""
        # broadcast rule: inf indx is too long, truncate on the left
        indx = indx[-self.tdim:]
        indx2 = copy.copy(indx)
        for i, indx_i in enumerate(indx):
            i2 = -len(indx) + i
            # print(-i2, idx_i)
            if self.tshape[i2] == 1:
                if np.isscalar(indx_i) and indx_i > 0:
                    # broadcast rule: if indx_i > 0 at dim == 1, snap to 0
                    indx2[i2] = 0
        # print(indx2)
        return indx2

    def aslice(self, indices):
        cdim = self.cdim
        for i in range(self.tdim, len(indices)):
            idx = indices(i)
            if idx != slice(None):
                cdim -= 1
        return indices, cdim
