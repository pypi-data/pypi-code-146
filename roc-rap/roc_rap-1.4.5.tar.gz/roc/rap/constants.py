#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constants for RAP plugin.
"""

__all__ = ['PLUGIN',
           'PIPELINE_DATABASE',
           'TIME_SQL_STRFORMAT',
           'TC_HFR_LIST_PAR',
           'UINT32_MAX_ENCODING',
           'THR_TICK_NSEC']

PLUGIN = 'roc.rap'

# Load pipeline database identifier
try:
    from poppy.core.logger import logger
    from poppy.core.conf import settings
    PIPELINE_DATABASE = settings.PIPELINE_DATABASE
except Exception:
    PIPELINE_DATABASE = 'PIPELINE_DATABASE'
    logger.warning(f'settings.PIPELINE_DATABASE not defined for {__file__}, \
                     use "{PIPELINE_DATABASE}" by default!')

# SQL string time format
TIME_SQL_STRFORMAT = '%Y-%m-%d %H:%M:%S.%f'

# List of TC for HFR LIST mode configuration
TC_HFR_LIST_PAR = [
                    'TC_THR_LOAD_NORMAL_PAR_2',
                    'TC_THR_LOAD_NORMAL_PAR_3',
                    'TC_THR_LOAD_BURST_PAR_2',
                    'TC_THR_LOAD_BURST_PAR_3',
                   ]

# Max encoding value for uint32
UINT32_MAX_ENCODING = 2**32

# THR Tick value in nanosec
THR_TICK_NSEC = 15258
