#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module collects TablArray conversions for np.linalg functions which are
unary operands, where one or more axes transform to a scalar (axis -> scalar)

Created on Sat Jan  9 12:34:32 2021

@author: chris
"""

import numpy as np

from ..np2ta.ax_op import _axial_broadcast

norm = _axial_broadcast(np.linalg.norm)
