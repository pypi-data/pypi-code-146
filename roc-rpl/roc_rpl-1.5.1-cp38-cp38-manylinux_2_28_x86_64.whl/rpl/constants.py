#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime

from poppy.core.conf import settings
from poppy.core.logger import logger

__all__ = ['TYPE_TO_NUMPY_DTYPE',
           'VALID_PACKET',
           'INVALID_PACKET_HEADER',
           'INVALID_PACKET_DATA',
           'OUTSIDE_RANGE_PACKET',
           'INVALID_PACKET_CDATA',
           'INVALID_PACKET_TIME',
           'UNKNOWN_STATUS',
           'TC_PACKET_TYPE', 'TM_PACKET_TYPE',
           'UNKNOWN_PACKET', 'TIME_ISO_STRFORMAT',
           'TIME_DAILY_STRFORMAT', 'TIME_RANGE_STRFORMAT',
           'TCREPORT_STRTFORMAT', 'INVALID_UTC_DATETIME',
           'INVALID_UTC_TIME', 'UNKNOWN_ACK_STATE',
           'UNKNOWN_UNIQUE_ID', 'TM_RAW_DATA_DEF',
           'RAW_DATA_DEF', 'TC_RAW_DATA_DEF', 'UNKNOWN_IDB',
           'SPICE_KERNEL_PATTERN', 'TC_ACK_STATE_PASSED',
           'SOLAR_ORBITER_NAIF_ID', 'KERNEL_CATEGORY',
           'TC_ACK_STATE_PASSED', 'EXCLUDED_PACKETS',
           'RECOVERED_PACKETS', 'SCOS_HEADER_BYTES',
           'PIPELINE_DATABASE', 'TEST_DATABASE',
           ]

TYPE_TO_NUMPY_DTYPE = {
    'uint16': 'uint16',
    'uint8': 'uint8',
    'uint32': 'uint32',
    'int16': 'int16',
    'int8': 'int8',
    'int32': 'int32',
    'float32': 'float32',
    'time': ('uint32', 3)
}

# Packet status possible flags
VALID_PACKET = 0
INVALID_PACKET_HEADER = 1
INVALID_PACKET_DATA = 2
OUTSIDE_RANGE_PACKET = 3
# same than INVALID_PACKET_DATA but for invalid compressed data
INVALID_PACKET_CDATA = 4
INVALID_PACKET_TIME = 5
UNKNOWN_STATUS = -1

# TM/TC packet_type CCSDS ID
TM_PACKET_TYPE = 0
TC_PACKET_TYPE = 1

# Unknown Packet flag
UNKNOWN_PACKET= 'UNKNOWN'

# TC ack. state flag
TC_ACK_STATE_PASSED = 'PASSED'

# Datetime string formats
INPUT_DATETIME_STRFTIME = '%Y-%m-%dT%H:%M:%S'
TIME_ISO_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TCREPORT_STRTFORMAT = TIME_ISO_STRFORMAT
TIME_DAILY_STRFORMAT = '%Y%m%d'
TIME_RANGE_STRFORMAT = '%Y%m%dT%H%M%S'

INVALID_UTC_TIME = '2000-01-01T00:00:00.000000Z'

UNKNOWN_UNIQUE_ID = 'UNKNOWN'
UNKNOWN_ACK_STATE = 'UNKNOWN'
UNKNOWN_IDB = 'UNKNOWN'

# Convert invalid UTC time string into datetime
INVALID_UTC_DATETIME = datetime.strptime(INVALID_UTC_TIME,
                                        TCREPORT_STRTFORMAT)

# Default values for RawData packet list dictionary
RAW_DATA_DEF = {
    'srdb_id': None,
    'palisade_id': None,
    'status': VALID_PACKET,
    'utc_time': INVALID_UTC_DATETIME,
    'binary': None,
    'type': None,
}

# Default values for RawData TM packet list dictionary
TM_RAW_DATA_DEF = {
    'sync_flag': None,
}

# Default values for RawData TC packet list dictionary
TC_RAW_DATA_DEF = {
    'ack_acc_state': None,
    'ack_exe_state': None,
}

# Special packets
EXCLUDED_PACKETS = [
                    'RACK_SUCCESS_EXE_COMMAND',  # MEB GSE packet
                    'RACK_HK', # MEB GSE packet
                    ]

# Packets, known to be inconsistent but must be parsed anyway
RECOVERED_PACKETS = [
                    'TM_DPU_RWF_HK', # 102 bytes packet size found, but 101 bytes expected
                    ]



# Give for each kernel type the glob file pattern,
# The field(s) to extract as regex and the number of field(s) to extract
SPICE_KERNEL_PATTERN = {'ck': ['solo_ANC_soc-*_????????-????????_V??.bc',
                               '\_([0-9]{8})\-([0-9]{8})\_V([0-9]{2}).bc', 3],
                        'fk':['solo_ANC_soc-*_V??.tf',
                              '\_V([0-9]{2}).tf', 1],
                        'ik':['solo_ANC_soc-*_V??.ti',
                              '\_V([0-9]{2}).ti', 1],
                        'mk':['solo_ANC_soc-*.tm',
                              '\_V([0-9]{3})\_([0-9]{8})\_([0-9]{3}).tm', 3],
                        'sclk': ['solo_ANC_soc-*_????????_????????_V??.tsc',
                                 '\_([0-9]{8})\_([0-9]{8})\_V([0-9]{2}).tsc', 3],
                        'spk':['solo_ANC_soc-*_????????-????????_V??.bsp',
                                '\_([0-9]{8})\-([0-9]{8})\_V([0-9]{2}).bsp', 3],
                        'lsk':['*.tls',
                               '([0-9]{4}).tls', 3],
                        'pck':['*.*', None, 0],
                        }



# NAIF SPICE ID of Solar Orbiter
SOLAR_ORBITER_NAIF_ID = -144

# Predictive and as-flown kernel category
# predictive should be loaded first
KERNEL_CATEGORY = ['pred', 'flown']

# DDS TmRaw SCOS header length in bytes
SCOS_HEADER_BYTES = 76

# Load pipeline database identifier
try:
    PIPELINE_DATABASE = settings.PIPELINE_DATABASE
except:
    PIPELINE_DATABASE = 'PIPELINE_DATABASE'
    logger.warning(f'settings.PIPELINE_DATABASE not defined for {__file__}, \
                     use "{PIPELINE_DATABASE}" by default!')

try:
    TEST_DATABASE = settings.TEST_DATABASE
except:
    TEST_DATABASE = 'TEST_DATABASE'
    logger.warning(f'settings.TEST_DATABASE not defined for {__file__}, \
                     use "{TEST_DATABASE}" by default!')
