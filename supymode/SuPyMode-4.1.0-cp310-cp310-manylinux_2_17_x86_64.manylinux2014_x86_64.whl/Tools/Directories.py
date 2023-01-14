#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

import SuPyMode

RootPath     = Path(SuPyMode.__path__[0])

ZeroPath     = Path(os.path.dirname(RootPath))

ReportPath   = os.path.join(RootPath.parents[0], 'Reports')
