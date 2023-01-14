#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TablArray or tables of cells
When the best structure of data is any-dimensional cells arranged
in any-dimensional tables - ATC provides fast numpy-like array
operations with broadcasting to handle both cellular-dimensions
and tabular-dimensions at once.

Portions of ATC looks like pass-through to numpy with a tiny overhead to manage
cdim. But the irreplaceable part of ATC is broadcasting for binary operands.

ATC was originally developed to manage large numbers of optical modes.

Created on Fri May 15 17:40:41 2020

@author: chris
"""

from . import linalg
from .np2ta import *

from .version import __version__, __status__

from .cmatmul import *
from .misc import *
from .mmul import *
from .re import *
from .set import *
from .solve import *
from .stack import *
from .ta import *
from .taplot import *
from .taprint import *
from .views import *
