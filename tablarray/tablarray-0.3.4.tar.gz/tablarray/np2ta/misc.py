#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:31:44 2020

@author: chris
"""

import functools
import numpy as np

from .ax_op import all
from .bin_op import isclose

# numpy has shape and size that already work properly for TablArray
shape = np.shape
size = np.size


@functools.wraps(np.allclose)
def allclose(a, b, *args, **kwargs):
    close = isclose(a, b, *args, **kwargs)
    return all(close.array)
