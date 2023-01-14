#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 10:50:40 2021

@author: chris
"""

from . import misc


def bcast(a):
    """get view of obj with broadcast-style tabular indexing, if available,
    else return obj"""
    if misc.istablarray(a):
        return a.__view__('bcast')
    return a


def cell(a):
    """get cellular view of obj, if available, else return obj"""
    if misc.istablarray(a):
        return a.__view__('cell')
    return a


def table(a):
    """get tabular view of obj, if available, else return obj"""
    if misc.istablarray(a):
        return a.__view__('table')
    return a


def array(a):
    """get simple array view of obj, if available, else return obj"""
    if misc.istablarray(a):
        return a.__view__('array')
    return a
