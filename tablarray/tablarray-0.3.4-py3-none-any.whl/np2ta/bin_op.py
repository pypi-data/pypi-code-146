#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
My idea is to have a comparable lib to numpy.add, .sum, etc.
But it will work regardless of whether the x1, x2, ... are numpy or TablArray.

Created on Sun May 17 18:17:59 2020

@author: chris
"""

import functools
import numpy as np

from .. import misc


def _cast_other_type(other, TablArray):
    """when a TablArray and other type are cast in a binary operator, make sure
    other is np.ndarray compatible, also maybe reorient for broadcasting
    if the TablArray is in a tabular view"""
    o_type = type(other)
    other = np.array(other) if (o_type is list or o_type is tuple) else other
    if TablArray._tabular and not np.isscalar(other):
        # if my view is tabular I need to promote to tabular shape
        o_shape2 = tuple(list(other.shape) + [1] * TablArray.ts.cdim)
        other = other.reshape(o_shape2)
    return other


def _binary_broadcast(func, dtype=None):
    """broadcasting for binary operands - TablArray, np.ndarray, or scalar"""
    @functools.wraps(func)
    def wrap_bin_bcast(a, b, *args, **kwargs):
        """depending on the types of a and b, find a suitable broadcasting"""
        if misc.istablarray(a) and misc.istablarray(b):
            # if both are TablArray, then use tablarray broadcasting
            cdim, bc = a.ts.combine(b.ts)
            rarray = bc.calc_function(func, a.base, b.base, *args,
                                      dtype=dtype, **kwargs)
            rclass = a.__class__
            view = a.view
        elif misc.istablarray(a):
            b = _cast_other_type(b, a)
            # if only one is TablArray, then use numpy array broadcast
            rarray = func(a.base, b, *args, **kwargs)
            rclass = a.__class__
            # assume the result has the same cdim as a.ts.cdim
            cdim = a.ts.cdim
            view = a.view
        elif misc.istablarray(b):
            a = _cast_other_type(a, b)
            rarray = func(a, b.base, *args, **kwargs)
            rclass = b.__class__
            cdim = b.ts.cdim
            view = b.view
        else:
            # if neither operand is TablArray, just fall back on numpy
            return func(a, b, *args, **kwargs)
        # once a TablArray, always a TablArray
        return misc._rval_once_a_ta(rclass, rarray, cdim, view)
    wrap_bin_bcast.__doc__ = (
        "**TablArray compatible** %s\n\n" % func.__name__
        + wrap_bin_bcast.__doc__)
    return wrap_bin_bcast


# binary functions from numpy wrapped for TablArray compatibility

# these are also available as methods
add = _binary_broadcast(np.add)
subtract = _binary_broadcast(np.subtract)
multiply = _binary_broadcast(np.multiply)
power = _binary_broadcast(np.power)
true_divide = _binary_broadcast(np.true_divide)
divmod = _binary_broadcast(np.divmod)
equal = _binary_broadcast(np.equal, dtype=bool)
greater_equal = _binary_broadcast(np.greater_equal, dtype=bool)
greater = _binary_broadcast(np.greater, dtype=bool)
less_equal = _binary_broadcast(np.less_equal, dtype=bool)
less = _binary_broadcast(np.less, dtype=bool)
logical_and = _binary_broadcast(np.logical_and)
logical_or = _binary_broadcast(np.logical_or)
logical_xor = _binary_broadcast(np.logical_xor)

# these are only available here - not as methods
# allclose = _binary_broadcast(np.allclose, dtype=bool)
arctan2 = _binary_broadcast(np.arctan2)
bitwise_and = _binary_broadcast(np.bitwise_and)
bitwise_or = _binary_broadcast(np.bitwise_or)
bitwise_xor = _binary_broadcast(np.bitwise_xor)
copysign = _binary_broadcast(np.copysign)
divide = _binary_broadcast(np.true_divide)
float_power = _binary_broadcast(np.float_power)
floor_divide = _binary_broadcast(np.floor_divide)
fmax = _binary_broadcast(np.fmax)
fmin = _binary_broadcast(np.fmin)
fmod = _binary_broadcast(np.fmod)
gcd = _binary_broadcast(np.gcd)
heaviside = _binary_broadcast(np.heaviside)
hypot = _binary_broadcast(np.hypot)
isclose = _binary_broadcast(np.isclose, dtype=bool)
lcm = _binary_broadcast(np.lcm)
ldexp = _binary_broadcast(np.ldexp)
left_shift = _binary_broadcast(np.left_shift)
logaddexp = _binary_broadcast(np.logaddexp)
logaddexp2 = _binary_broadcast(np.logaddexp2)
maximum = _binary_broadcast(np.maximum)
minimum = _binary_broadcast(np.minimum)
mod = _binary_broadcast(np.remainder)
nextafter = _binary_broadcast(np.nextafter)
not_equal = _binary_broadcast(np.not_equal, dtype=bool)
remainder = _binary_broadcast(np.remainder)
right_shift = _binary_broadcast(np.right_shift)
