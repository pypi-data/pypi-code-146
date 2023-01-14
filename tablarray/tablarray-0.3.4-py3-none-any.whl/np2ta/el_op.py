#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:58:22 2020

@author: chris
"""

import functools
import numpy as np

from .. import misc


def _element_op_cast(func):
    """wrap element-wise numpy functions - once an ATC, always an ATC"""
    @functools.wraps(func)
    def wrap_elop_cast(x, *args, **kwargs):
        if misc.istablarray(x):
            rarray = func(x, *args, **kwargs)
            rclass = x.__class__
            # once a TablArray, usually a TablArray
            return misc._rval_once_a_ta(rclass, rarray, x.ts.cdim, x.view)
        else:
            # a is presumably array-like
            return func(x, *args, **kwargs)
    return wrap_elop_cast


abs = _element_op_cast(np.abs)
absolute = _element_op_cast(np.absolute)
angle = _element_op_cast(np.angle)
arccos = _element_op_cast(np.arccos)
arccosh = _element_op_cast(np.arccosh)
arcsin = _element_op_cast(np.arcsin)
arcsinh = _element_op_cast(np.arcsinh)
arctan = _element_op_cast(np.arctan)
arctanh = _element_op_cast(np.arctanh)
bitwise_not = _element_op_cast(np.bitwise_not)
cbrt = _element_op_cast(np.cbrt)
ceil = _element_op_cast(np.ceil)
conj = _element_op_cast(np.conjugate)
conjugate = _element_op_cast(np.conjugate)
cos = _element_op_cast(np.cos)
cosh = _element_op_cast(np.cosh)
deg2rad = _element_op_cast(np.deg2rad)
degrees = _element_op_cast(np.degrees)
exp = _element_op_cast(np.exp)
exp2 = _element_op_cast(np.exp2)
expm1 = _element_op_cast(np.expm1)
fabs = _element_op_cast(np.fabs)
floor = _element_op_cast(np.floor)
imag = _element_op_cast(np.imag)
invert = _element_op_cast(np.invert)
iscomplex = _element_op_cast(np.iscomplex)
isfinite = _element_op_cast(np.isfinite)
isinf = _element_op_cast(np.isinf)
isnan = _element_op_cast(np.isnan)
isnat = _element_op_cast(np.isnat)
isreal = _element_op_cast(np.isreal)
log = _element_op_cast(np.log)
log10 = _element_op_cast(np.log10)
log1p = _element_op_cast(np.log1p)
log2 = _element_op_cast(np.log2)
logical_not = _element_op_cast(np.logical_not)
negative = _element_op_cast(np.negative)
positive = _element_op_cast(np.positive)
rad2deg = _element_op_cast(np.rad2deg)
radians = _element_op_cast(np.radians)
real = _element_op_cast(np.real)
real_if_close = _element_op_cast(np.real_if_close)
reciprocal = _element_op_cast(np.reciprocal)
rint = _element_op_cast(np.rint)
sign = _element_op_cast(np.sign)
signbit = _element_op_cast(np.signbit)
sin = _element_op_cast(np.sin)
sinc = _element_op_cast(np.sinc)
sinh = _element_op_cast(np.sinh)
spacing = _element_op_cast(np.spacing)
square = _element_op_cast(np.square)
sqrt = _element_op_cast(np.sqrt)
tan = _element_op_cast(np.tan)
tanh = _element_op_cast(np.tanh)
trunc = _element_op_cast(np.trunc)

