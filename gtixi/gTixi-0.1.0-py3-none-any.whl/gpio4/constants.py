#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 18:14:02 2018

@author: hank
@page:   https://github.com/hankso
"""

import re


class _sunxi():
    def __getitem__(self, pin):
        rst = re.findall(r"P([A-Z])(\d+)", str(pin))
        if not rst:
            raise KeyError('pin name {} not supported!'.format(pin))
        return 32*(ord(rst[0][0])-65) + int(rst[0][1])


RISING       = 'rising'                                         # noqa: E221
FALLING      = 'falling'                                        # noqa: E221
CHANGE       = 'change'                                         # noqa: E221
HIGH         = 1                                                # noqa: E221
LOW          = 0                                                # noqa: E221
INPUT        = 'in'                                             # noqa: E221
OUTPUT       = 'out'                                            # noqa: E221
INPUT_PULLUP = 'pullup'                                         # noqa: E221
INPUT_PULLDN = 'pulldn'                                         # noqa: E221
MSBFIRST     = 1                                                # noqa: E221
LSBFIRST     = 2                                                # noqa: E221
true         = True                                             # noqa: E221
false        = False                                            # noqa: E221
FOREVER      = 1e5                                              # noqa: E221
FOREVER_ms   = 1e5 * 1000                                       # noqa: E221

BOARD_SUNXI = _sunxi()
BOARD_NANO_PI = {}                                              # TODO
BOARD_ORANGE_PI_PC = {}                                         # TODO
BCM = {}                                                        # TODO

__all__ = ['RISING', 'FALLING', 'CHANGE', 'HIGH', 'LOW',
           'OUTPUT', 'INPUT', 'INPUT_PULLUP', 'INPUT_PULLDN',
           'MSBFIRST', 'LSBFIRST', 'true', 'false', 'FOREVER', 'FOREVER_ms',
           'BOARD_SUNXI', 'BOARD_NANO_PI', 'BOARD_ORANGE_PI_PC', 'BCM']
