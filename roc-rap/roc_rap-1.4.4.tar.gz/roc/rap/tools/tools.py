#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp

from poppy.core.generic.paths import Paths

__all__ = ["paths"]

# root directory of the module
_ROOT_DIRECTORY = osp.abspath(
    osp.join(
        osp.dirname(__file__),
        osp.pardir,
    )
)

# create a path object that can be used to get some common path in the module
paths = Paths(_ROOT_DIRECTORY)



