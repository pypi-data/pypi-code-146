#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import json
import os.path as osp

from jinja2 import Environment, FileSystemLoader

from poppy.core.tools.exceptions import DescriptorLoadError
from poppy.core.logger import logger
from poppy.core.conf import settings

__all__ = ['PLUGIN',
           'DESCRIPTOR',
           'NAIF_SOLO_ID',
           'TM_PACKET_TYPE',
           'TC_PACKET_TYPE',
           'PACKET_TYPE',
           'PACKET_DATA_GROUP',
           'PACKET_INVALID',
           'PACKET_VALID',
           'IDB_SOURCE',
           'TEST_DATABASE',
           'PIPELINE_DATABASE',
           'PIPELINE_TABLES',
           'SQL_LIMIT',
           'TRYOUTS',
           'TIME_SQL_STRFORMAT',
           'TIME_INPUT_STRFORMAT',
           'TIME_OUTPUT_STRFORMAT',
           'TIME_DAILY_STRFORMAT',
           'TIME_ISO_STRFORMAT',
           'TIME_EFECS_STRFORMAT',
           'TIME_WAIT_SEC',
           'DATA_VERSION',
           'START_TIME',
           'END_TIME',
           'PACKET_CHUNK',
           'DELTA_HOURS',
           'TC_ACK_ALLOWED_STATUS',
           'ROC_DATA_ROOT',
           'ROC_PUBLIC_DATA_ROOT',
           'FILE_STATE_LIST',
           'FILE_STATUS_LIST',
           'FILE_LEVEL_LIST',
           'ROC_SPICE_KERNEL_ROOT',
           'DATA_ALLOWED_EXTENSIONS',
           'SPICE_KERNEL_ALLOWED_EXTENSIONS',
           'LEVEL_2_INST',
           'LEVEL_3_INST',
           'LEVEL_BY_MISSION',
           'LEVEL_BY_MONTH',
           'LEVEL_BY_DAY',
           'SPICE_KERNEL_TYPES',
           'ROC_DATA_HTTPS_ROOT',
           'ROC_DATA_HTTPS_PUBLIC_ROOT',
           'L0_DIRPATH_PATTERN',
           'ROC_SPICE_KERNEL_HTTPS_ROOT',
           'BIA_SWEEP_TABLE_PACKETS',
           'HFR_FREQ_LIST_PACKETS',
           'SBM_LOG_PACKETS',
           'HFR_SCIENCE_PACKETS',
           'BIA_SWEEP_LOG_PACKETS',
           'SBM_ALGO_PARAM_LIST',
           'BIA_SWEEP_TABLE_NR',
           'LFR_KCOEFF_PARAM_NR',
           'JENV',
           'SOLO_HK_TEMPLATE',
           'BIA_CURRENT_LOG_PACKETS',
           'LFR_KCOEFF_DUMP_PACKETS',
           'TF_CP_BIA_P011_SRDB_ID',
           'WORKERS',
           'CIWT0130TM',
           'TF_PA_DPU_0038',
           'TF_PA_DPU_0039',
           'SOAR_TAP_URL',
           'EFECS_EVENT_LOG',
           'EVENT_TM_APID',
           'TC_ACK_APID',
           'SCIENCE_TM_APID',
           'LL_TM_APID',
           'SBM_TM_APID',
           'HK_TM_APID',
           'TM_APID_EVENT_LOG',
           'TC_PACKET_EVENT_LOG',
           'LFR_CALIB_EVENT_LOG',
           ]

# Name of the plugin
from roc.dingo.models.file import FileLog
from roc.dingo.models.file import \
    FILE_STATE_LIST, FILE_STATUS_LIST, FILE_LEVEL_LIST
from roc.dingo.models.packet import TmLog, TcLog

PLUGIN = 'roc.dingo'

# root directory of the module
_ROOT_DIRECTORY = osp.abspath(
    osp.join(
        osp.dirname(__file__),
    )
)


# NAIF SPICE ID for SOLO
NAIF_SOLO_ID = -144

# Default data version for product file
DATA_VERSION = '01'

# Number of database connexion tryouts
TRYOUTS = 3

# Time to wait in seconds between two database connection tryouts
TIME_WAIT_SEC = 3

# Default IDB source
IDB_SOURCE = 'MIB'

# TM/TC packet_type CCSDS ID
TM_PACKET_TYPE = 0
TC_PACKET_TYPE = 1
PACKET_VALID = 'VALID'
PACKET_INVALID = 'INVALID'

# Packet type list
PACKET_TYPE = ['TM', 'TC']

# Group for TM and TC
PACKET_DATA_GROUP = {'TM': 'source_data',
                     'TC': 'application_data'}

# Time string format
TIME_SQL_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TIME_ISO_STRFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TIME_INPUT_STRFORMAT = '%Y-%m-%dT%H:%M:%S'
TIME_EFECS_STRFORMAT = '%Y-%jT%H:%M:%SZ'
TIME_OUTPUT_STRFORMAT = '%Y%m%dT%H%M%S'
TIME_DAILY_STRFORMAT = '%Y%m%d'


# Limit of rows to be returned by the database
SQL_LIMIT = 1000000000

# Number of workers to run in parallel
WORKERS = 1

# Pipeline tables
PIPELINE_TABLES = {'tm_log': TmLog,
                   'file_log': FileLog,
                   'tc_log': TcLog,
                   }

# Default end time of the packets time range to query
# Default is beginning of the current day
END_TIME = datetime.now().date()

# Default start time of the packets time range to query
# Default is end_time - 180 days
START_TIME = END_TIME - timedelta(days=180)

# Load pipeline database identifier
try:
    PIPELINE_DATABASE = settings.PIPELINE_DATABASE
except Exception:
    PIPELINE_DATABASE = 'PIPELINE_DATABASE'
    logger.warning(f'settings.PIPELINE_DATABASE not defined for {__file__}, \
                     use "{PIPELINE_DATABASE}" by default!')

try:
    TEST_DATABASE = settings.TEST_DATABASE
except Exception:
    TEST_DATABASE = 'TEST_DATABASE'
    logger.warning(f'settings.TEST_DATABASE not defined for {__file__}, \
                     use "{TEST_DATABASE}" by default!')

# Load descriptor file
descriptor_path = osp.join(_ROOT_DIRECTORY, 'descriptor.json')
try:
    with open(descriptor_path, 'r') as file_buffer:
        DESCRIPTOR = json.load(file_buffer)
except Exception:
    raise DescriptorLoadError(f'Loading {descriptor_path} has failed!')

# Number of packets to process/insert in one chunk
PACKET_CHUNK = 100

# Time interval in hours to query
DELTA_HOURS = 1

# TC Packet ack possible status
TC_ACK_ALLOWED_STATUS = ['PASSED', 'FAILED']

# ROC data file tree rootname
ROC_DATA_ROOT = \
    '/volumes/plasma/rpw/roc/data/https/private/solo/rpw/data/'

# ROC publica data file tree rootname
ROC_PUBLIC_DATA_ROOT = \
    '/volumes/plasma/rpw/roc/data/https/pub/solo/rpw/data/'

# L0 FILE directory PATH PATTERN (default path in pipeline Docker container)
L0_DIRPATH_PATTERN = '/pipeline/data/private/solo/rpw/data/L0/????/??/??'

# ROC data http access URL
ROC_DATA_HTTPS_ROOT = \
    'https://rpw.lesia.obspm.fr/roc/data/private/solo/rpw/data/'

# ROC spice kernel file tree rootname
ROC_SPICE_KERNEL_ROOT = \
    '/volumes/plasma/rpw/roc/data/https/private/solo/soc/spice/kernels/'

# ROC data http access URL
ROC_SPICE_KERNEL_HTTPS_ROOT = \
    'https://rpw.lesia.obspm.fr/roc/data/private/solo/soc/spice/kernels/'

# ROC public data http access URL
ROC_DATA_HTTPS_PUBLIC_ROOT = \
    'https://rpw.lesia.obspm.fr/roc/data/pub/solo/rpw/data/'

# ROC Delivered directory
ROC_DELIVERED_ROOT = '/volumes/plasma/rpw/roc/data/sftp/soc/gfts/delivered'

# DATA ALLOWED EXTENSIONS
DATA_ALLOWED_EXTENSIONS = \
    ['xml', 'json', 'cdf', 'h5']

# SPICE KERNEL ALLOWED EXTENSIONS
SPICE_KERNEL_ALLOWED_EXTENSIONS = \
    ['bc', 'bpc', 'bsp', 'tf', 'ti', 'tls', 'tm', 'tpc', 'tsc']

# Defined in models/file.py
# FILE_LEVEL_LIST = [
#     'CAL', 'TC', 'TM', 'SK', 'L0', 'HK', 'L1',
#     'BIA', 'L1R', 'L2', 'L3', 'LL01']

# LEVEL 2 DATA INSTRUMENTS
LEVEL_2_INST = \
    ['lfr_asm', 'lfr_bp', 'lfr_wf_b', 'lfr_wf_e', 'tds_hist1d', 'tds_hist2d',
     'tds_lfm', 'tds_mamp', 'tds_stat', 'tds_wf_b', 'tds_wf_e', 'thr']

# LEVEL 3 DATA INSTRUMENTS
LEVEL_3_INST = ['lfr_density', 'lfr_efield', 'lfr_scpot', 'tnr_fp']

# SPICE KERNEL TYPES
# Skipping mk/ because they are only meta-kernels
SPICE_KERNEL_TYPES = ['ck', 'fk', 'ik', 'lsk', 'pck', 'sclk', 'spk']

# GROUPING PERIOD PER LEVEL
LEVEL_BY_MISSION = ['CAL', 'SK']
LEVEL_BY_MONTH = ['L2', 'L3', 'BIA']
LEVEL_BY_DAY = ['TC', 'TM', 'L0', 'HK', 'L1', 'L1R', 'LL01']


# TM packet APID
TC_ACK_APID = [1201, 1207, 1233, 1249]  # DPU, LFR, TDS, THR
EVENT_TM_APID = [1207]
LL_TM_APID = [1212]
SCIENCE_TM_APID = [1228, 1244, 1260]
SBM_TM_APID = [1276, 1292]
HK_TM_APID = [1204, 1220, 1236, 1252, 1269, 1300]

# List of TM/TC packets to insert in specific tables

SBM_LOG_PACKETS = ['TM_DPU_EVENT_PR_DPU_SBM1',
                   'TM_DPU_EVENT_PR_DPU_SBM2']
BIA_SWEEP_TABLE_PACKETS = ['TC_DPU_LOAD_BIAS_SWEEP',
                           'TC_DPU_CLEAR_BIAS_SWEEP']
BIA_CURRENT_LOG_PACKETS = ['TC_DPU_SET_BIAS1',
                           'TC_DPU_SET_BIAS2',
                           'TC_DPU_SET_BIAS3']
BIA_SWEEP_LOG_PACKETS = ['TM_DPU_EVENT_PR_BIA_SWEEP']
HFR_FREQ_LIST_PACKETS = ['TC_THR_LOAD_NORMAL_PAR_2',
                         'TC_THR_LOAD_NORMAL_PAR_3',
                         'TC_THR_LOAD_BURST_PAR_2',
                         'TC_THR_LOAD_BURST_PAR_3']
LFR_KCOEFF_DUMP_PACKETS = ['TM_LFR_KCOEFFICIENTS_DUMP']
HFR_SCIENCE_PACKETS = ['TM_THR_SCIENCE_NORMAL_HFR',
                       'TM_THR_SCIENCE_BURST_HFR',
                       'TM_THR_SCIENCE_CALIBRATION_HFR']

# SBM1/SBM2 TM algo parameters
SBM_ALGO_PARAM_LIST = {
    1: ['SY_DPU_SBM1_DT1_SBM1_D',
        'SY_DPU_SBM1_DT2_SBM1_D',
        'SY_DPU_SBM1_DT3_SBM1_D'],
    2: ['HK_DPU_SBM2_DT_SBM2',
        'HK_DPU_SBM2_DT_LW',
        'HK_DPU_EPD_S20_ESW_FLAG_D',
        'HK_DPU_EPD_S20_EASW_FLAG_D',
        'HK_DPU_EPD_S20_EN_FLAG_D',
        'HK_DPU_EPD_S20_ES_FLAG_D',
        'HK_DPU_EPD_S20_PSW_FLAG_D',
        'HK_DPU_EPD_S20_PASW_FLAG_D',
        'HK_DPU_EPD_S20_PN_FLAG_D',
        'HK_DPU_EPD_S20_PS_FLAG_D']
}

# List of EFECS events to copy in event_log table
# See EFECS_ICD_SOL-SGS-ICD-0006 for list of EFECS
EFECS_EVENT_LOG = ['WOL', 'TCM', 'PASS', 'EMC_MAND_QUIET',
                   'EMC_PREF_NOISY', 'MAINT', 'NAV']

# List of TM APID to copy in event_log table
TM_APID_EVENT_LOG = [1207]

# List of TC to copy in event_log table
TC_PACKET_EVENT_LOG = ['TC_DPU_SWITCH_ON_EQUIPMENT',
                       'TC_DPU_SWITCH_OFF_EQUIPMENT',
                       'TC_DPU_BOOT_DAS',
                       'TC_DPU_ENTER_STANDBY',
                       'TC_DPU_ENTER_SERVICE',
                       'TC_DPU_ENTER_SURVEY_NORMAL',
                       'TC_DPU_ENTER_SURVEY_BURST',
                       'TC_DPU_ENTER_SURVEY_BACKUP',
                       'TC_DPU_ENTER_SBM_DETECTION',
                       'TC_DPU_ENTER_SBM1_DUMP',
                       'TC_DPU_ENTER_SBM2_ACQ',
                       'TC_TDS_DUMP_SBM2_TSWF',
                       'TC_TDS_DUMP_NORMAL_TSWF',
                       'TC_THR_ENABLE_CALIBRATION',
                       ]
TC_PACKET_EVENT_LOG.extend(HFR_FREQ_LIST_PACKETS)
TC_PACKET_EVENT_LOG.extend(BIA_CURRENT_LOG_PACKETS)

# LFR Calibration event packets
LFR_CALIB_EVENT_LOG = ['TC_LFR_ENABLE_CALIBRATION',
                       'TC_LFR_DISABLE_CALIBRATION']

# Number of max. values that can be stored in the bias sweep table
BIA_SWEEP_TABLE_NR = 256

# Number of kCoeff parameters by TM
LFR_KCOEFF_PARAM_NR = 32

# Setup jinja2 environment
JINJA_TEMPLATE_DIR = os.path.join(_ROOT_DIRECTORY, 'templates')
JENV = Environment(loader=FileSystemLoader(JINJA_TEMPLATE_DIR))
# Jinja2 template for SOLO HK XML files
SOLO_HK_TEMPLATE = 'solo_hk_xml.tpl'

# SRDB ID of the transfer function TF_CP_BIA_P011 (or TF_CP_BIA_0011 in ICD)
# NOTES: SRDB_ID is CIWP0075TC and not CIWP0040TC as indicated in the ICD)
TF_CP_BIA_P011_SRDB_ID = 'CIWP0075TC'

# SBM1 QF TF ID
TF_PA_DPU_0038 = 'CIWP0028TM'
# SBM2 QF TF ID
TF_PA_DPU_0039 = 'CIWP0029TM'

# Enumeration for PA_DPU_BIA_SWEEP_PR_CODE {NIW01757}
CIWT0130TM = {
    1: 'START_ANT1',
    2: 'END_ANT1',
    3: 'START_ANT2',
    4: 'END_ANT2',
    5: 'START_ANT3',
    6: 'END_ANT3',
    7: 'STEP_ANT1',
    8: 'STEP_ANT2',
    9: 'STEP_ANT3',
}

# URL of the SOAR TAP service
SOAR_TAP_URL = 'http://soar.esac.esa.int/soar-sl-tap/tap'
