#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

from poppy.core.generic.paths import Paths

__all__ = ["paths"]

_ROOT_DIRECTORY = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    )
)

paths = Paths(_ROOT_DIRECTORY)

