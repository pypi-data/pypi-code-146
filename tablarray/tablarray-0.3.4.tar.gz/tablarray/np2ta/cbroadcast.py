#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:09:36 2020

@author: chris
"""
# std lib
import attr
import numpy as np

# broadcast loop controls
DIMEQ = 0       # EQ dimensions
DIMLP1 = 1      # loop over side 1
DIMLP2 = 2      # loop over side 2
DIMPAD1 = -1    # pad on side 1
DIMPAD2 = -2    # pad on side 2
DIMERR = -3     # error, incompatible dimension

_DTYPE_PRIORITY = {'bool': 0,
                   'bool8': 1,
                   'int8': 2,
                   'int16': 3,
                   'int32': 4,
                   'int64': 5,
                   'float16': 6,
                   'float32': 7,
                   'float64': 8,
                   'float128': 9,
                   'complex64': 10,
                   'complex128': 11,
                   'complex256': 12}


def _prioritize_dtype(override, atype, btype):
    """when arrays a and b are broadcast,
    determine dtype of the return array"""
    if override is not None:
        return override
    a_priority = _DTYPE_PRIORITY[atype.__str__()]
    b_priority = _DTYPE_PRIORITY[btype.__str__()]
    dtype = atype if (a_priority >= b_priority) else btype
    return dtype


def broadcast_shape(shape1, shape2):
    """given 2 shapes, return the broadcast result shape and controls

    >>> broadcast_shape((1, 1, 3), (2, 1))
    (array([1, 2, 3]), array([-2,  1,  2]), True)
    >>> broadcast_shape((1, 4, 3), (2, 1))
    (array([1, 4, 3]), array([-2, -3,  2]), False)
    """
    if shape1 == shape2:
        # shorten the process if the answer is trivial
        control = np.zeros(len(shape1), dtype=int)
        return shape1, control, True
    # get padding ready for any difference in length
    delta_len = len(shape1) - len(shape2)
    pad = [0] * abs(delta_len)
    if delta_len >= 0:
        shape1 = np.array(shape1)
        shape2 = np.array(pad + list(shape2))
    else:
        shape2 = np.array(shape2)
        shape1 = np.array(pad + list(shape1))
    new_shape = np.zeros(len(shape1), dtype=int)
    mask1 = shape1 >= shape2
    new_shape[mask1] = shape1[mask1]
    mask2 = shape2 > shape1
    new_shape[mask2] = shape2[mask2]
    controls = DIMERR * np.ones(len(shape1), dtype=int)
    # control indicates broadcasting method per dim
    controls[shape1 == shape2] = DIMEQ
    controls[np.logical_and(shape1 > shape2, shape2 <= 1)] = DIMLP2
    controls[np.logical_and(shape2 > shape1, shape1 <= 1)] = DIMLP1
    controls[shape1 == 0] = DIMPAD1
    controls[shape2 == 0] = DIMPAD2
    valid = not np.any(controls == DIMERR)
    return new_shape, controls, valid


@attr.s
class CellBroadcast(object):
    """Given a and b arrays, being segmented between tabular and cellular
    shapes, provide an iterator that yields 3 slices to be used for
    broadcasting.

    Example::

        cb = CellBroadcast((2,), (1,), (1,), (2, 2))
        cb.demo()
    """
    _tshape_a = attr.ib(type=tuple)
    _tshape_b = attr.ib(type=tuple)
    _cshape_a = attr.ib(type=tuple)
    _cshape_b = attr.ib(type=tuple)

    def __attrs_post_init__(self):
        # tabularshape controls
        tshape_ctrl = broadcast_shape(
                self._tshape_a, self._tshape_b)
        # cellularshape controls
        cshape_ctrl = broadcast_shape(
                self._cshape_a, self._cshape_b)
        # new_cdim = len(new_cshape)
        self.new_cdim = len(cshape_ctrl[0])
        # master shape controls
        shape_ctrl = self._broadcast_ctrl_combiner(
                tshape_ctrl, cshape_ctrl)
        self.new_shape, self._controls, self.valid = shape_ctrl
        self._ndim = len(self.new_shape)
        self.rslice = [slice(None)] * self._ndim
        is_in_a = np.logical_not(self._controls == DIMPAD1)
        ndim_a = np.sum(is_in_a)
        self.aslice = [slice(None)] * ndim_a
        self._a_ndim_map = np.zeros(self._ndim, dtype=int)
        self._a_ndim_map[is_in_a] = np.arange(ndim_a)
        is_in_b = np.logical_not(self._controls == DIMPAD2)
        ndim_b = np.sum(is_in_b)
        self.bslice = [slice(None)] * ndim_b
        self._b_ndim_map = np.zeros(self._ndim, dtype=int)
        self._b_ndim_map[is_in_b] = np.arange(ndim_b)

    @classmethod
    def from_tshapes(cls, a_ts, b_ts):
        return cls(a_ts.tshape, b_ts.tshape, a_ts.cshape, b_ts.cshape)

    @staticmethod
    def _broadcast_ctrl_combiner(a_ctrl, b_ctrl):
        """given a_ctr,b_ctrl: (new_shape, controls, valid), combine into 1"""
        a_shape, a_controls, a_valid = a_ctrl
        b_shape, b_controls, b_valid = b_ctrl
        new_shape = (np.concatenate((a_shape, b_shape))).astype(int)
        controls = (np.concatenate((a_controls, b_controls))).astype(int)
        valid = a_valid and b_valid
        return new_shape, controls, valid

    def _set_slice(self, dim, this_ctrl, this_slice):
        self.rslice[dim] = (this_slice)
        adim = self._a_ndim_map[dim]
        bdim = self._b_ndim_map[dim]
        # place this slice into aslice and/or bslice
        if this_ctrl == DIMLP2 or this_ctrl == DIMPAD2:
            self.aslice[adim] = (this_slice)
        if this_ctrl == DIMLP1 or this_ctrl == DIMPAD1:
            self.bslice[bdim] = (this_slice)
        # DIMLP requires slice(0) to dereference
        if this_ctrl == DIMLP1:
            self.aslice[adim] = (0)
        elif this_ctrl == DIMLP2:
            self.bslice[bdim] = (0)

    def __iter__(self, dim=0):
        if dim == self._ndim:
            # end recursion using yield as an iterator
            yield tuple(self.rslice), tuple(self.aslice), tuple(self.bslice)
            return
        this_ctrl = self._controls[dim]
        if this_ctrl == DIMEQ:
            # recursion
            yield from self.__iter__(dim + 1)
        else:
            this_n = self.new_shape[dim]
            for i in range(this_n):
                self._set_slice(dim, this_ctrl, i)
                # recursion
                yield from self.__iter__(dim + 1)

    def demo(self):
        print('new_shape: %s' % self.new_shape)
        for rslice, aslice, bslice in self:
            print('\nr ', rslice)
            print('a ', aslice)
            print('b ', bslice)

    def calc_function(self, func, a, b, dtype=None):
        """calculate rval=func(a, b) using my iterator"""
        assert self.valid, (
                "couldn't broadcast compound shapes %s and %s" %
                (a.ts, b.ts))
        dtype = _prioritize_dtype(dtype, a.dtype, b.dtype)
        rval = np.zeros(self.new_shape, dtype=dtype)
        for rslice, aslice, bslice in self:
            rval[rslice] = func(a[aslice], b[bslice])
        return rval


if __name__ == '__main__':
    import doctest
    doctest.testmod()
