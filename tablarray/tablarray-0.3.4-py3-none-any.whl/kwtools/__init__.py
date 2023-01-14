#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kwargs_tools
by Chris Cannon
====

Provides
    1. kwargs_scan - convert header and values from csv into a dictionary
    2. kwargs_db - instance = myclass(search='name')
                    is converted to
                   instance = myclass(param1, param2, ...)
                   using a database lookup
    3. kwargs_gui


@author: Chris Cannon
"""

__author__ = "Chris Cannon"
__version__ = "0.0.0"
__license__ = "GPLv3"
__status__ = "Prototype"

from .kwargs_scan import *
from .kwargs_db import *