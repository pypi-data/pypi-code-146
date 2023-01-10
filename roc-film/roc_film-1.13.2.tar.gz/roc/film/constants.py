#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
from os import path as osp
from datetime import datetime

from poppy.core.conf import settings
from poppy.core.logger import logger

__all__ = ['PLUGIN',
           'PIPELINE_DATABASE',
           'INPUT_DATETIME_STRFTIME',
           'TIME_ISO_STRFORMAT',
           'TIME_DAILY_STRFORMAT',
           'CDF_TRANGE_STRFORMAT',
           'TIME_GEN_STRFORMAT',
           'TIME_JSON_STRFORMAT',
           'TIME_L0_STRFORMAT',
           'TIME_DOY1_STRFORMAT',
           'TIME_DOY2_STRFORMAT',
           'SCOS_HEADER_BYTES',
           'DATA_VERSION',
           'UNKNOWN_IDB',
           'CHUNK_SIZE',
           'TC_ACK_ALLOWED_STATUS',
           'TEMP_DIR',
           'ARCHIVE_DAILY_DIR',
           'TMRAW_PREFIX_BASENAME',
           'TCREPORT_PREFIX_BASENAME',
           'TC_ACK_ALLOWED_STATUS',
           'ANT_1_FLAG',
           'ANT_2_FLAG',
           'ANT_3_FLAG',
           'TM_PACKET_CATEG',
           'MIN_DATETIME',
           'MAX_DATETIME',
           'PACKET_TYPE',
           'CDFEXPORT_PATH',
           'TIMEOUT',
           'CDF_POST_PRO_OPTS_ARGS',
           'BIA_SWEEP_TABLE_NR',
           ]

# root directory of the module
_ROOT_DIRECTORY = osp.abspath(
    osp.join(
        osp.dirname(__file__),
    )
)

# Name of the plugin
PLUGIN = 'roc.film'

# Load pipeline database identifier
try:
    PIPELINE_DATABASE = settings.PIPELINE_DATABASE
except:
    PIPELINE_DATABASE = 'PIPELINE_DATABASE'
    logger.warning(f'settings.PIPELINE_DATABASE not defined for {__file__}, use "{PIPELINE_DATABASE}" by default!')


# STRING format for time
INPUT_DATETIME_STRFTIME = '%Y-%m-%dT%H:%M:%S'
TIME_ISO_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TIME_DAILY_STRFORMAT = '%Y%m%d'
CDF_TRANGE_STRFORMAT = '%Y%m%dT%H%M%S'
TIME_GEN_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TIME_JSON_STRFORMAT = '%Y-%m-%dT%H:%M:%SZ'
TIME_L0_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%f000Z'
TIME_DOY1_STRFORMAT = '%Y-%jT%H:%M:%S.%fZ'
TIME_DOY2_STRFORMAT = '%Y-%jT%H:%M:%SZ'

# Datetime values min/max range
MIN_DATETIME = datetime(1999, 1, 1)
MAX_DATETIME = datetime(2100, 12, 31)

# Relative output directory path of the RPW file local archive
ARCHIVE_DAILY_DIR = '%Y/%m/%d'

# TmRaw prefix basename
TMRAW_PREFIX_BASENAME = 'solo_TM_rpw'

# TcReport prefix basename
TCREPORT_PREFIX_BASENAME = 'solo_TC_rpw'

# SOLO HK prefix basename
SOLOHK_PREFIX_BASENAME = 'solo_HK_platform'

# DDS TmRaw SCOS header length in bytes
SCOS_HEADER_BYTES = 76


# Default value for data_version
DATA_VERSION = '01'

# Default IDB source/version values
UNKNOWN_IDB = 'UNKNOWN'

# Temporary dir
TEMP_DIR = tempfile.gettempdir()

# Number of packets/events to be processed at the same time
CHUNK_SIZE = 10000

# TC Packet ack possible status in L0 files
TC_ACK_ALLOWED_STATUS = ['PASSED', 'FAILED']

# Antenna flags
ANT_1_FLAG = 1
ANT_2_FLAG = 2
ANT_3_FLAG = 3

# Packet category list
TM_PACKET_CATEG = ['ev', 'hk', 'oth', 'll', 'sci', 'sbm']

# Packet type list
PACKET_TYPE = ['TM', 'TC']

# Path to the cdfexport executable (default)
CDFEXPORT_PATH = '/pipeline/lib/cdf/current/bin/cdfexport'

# Max process timeout
TIMEOUT = 14400

# Allowed values for keyword --options in l1_post_pro command
CDF_POST_PRO_OPTS_ARGS = ['soop_type',
                         'obs_id',
                         'resize_wf',
                         'cdf_export',
                         'update_cdf',
                          'quality_bitmask']

# Number of max. values that can be stored in the bias sweep table
BIA_SWEEP_TABLE_NR = 256
