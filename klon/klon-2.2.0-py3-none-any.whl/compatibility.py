#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name, undefined-variable, unused-import, ungrouped-imports

#----------------------------------------------------------------------------------------------------------------------------------
# includes

# 2+3 compat
from __future__ import absolute_import, division, print_function, unicode_literals

# standards
from sys import version_info

#----------------------------------------------------------------------------------------------------------------------------------
# globals

PY2 = (version_info[0] == 2)

if PY2:
    text_type = unicode
else:
    text_type = str

#----------------------------------------------------------------------------------------------------------------------------------
