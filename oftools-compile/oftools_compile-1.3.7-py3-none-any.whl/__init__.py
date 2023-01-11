#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    __version__ = 'test'
    # package is not installed
    pass