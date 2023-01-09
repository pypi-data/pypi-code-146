#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 19:00:18 2022

@author: aguimera
"""

import scipy as sp
import scipy.interpolate
import numpy as np

def log_interp1d(xx, yy, kind='linear'):
    logx = np.log10(xx)
    # logy = np.log10(yy)
    lin_interp = sp.interpolate.interp1d(logx, yy, kind=kind)
    # log_interp = lambda zz: np.power(10.0, lin_interp(np.log10(zz)))
    log_interp = lambda zz: lin_interp(np.log10(zz))
    return log_interp