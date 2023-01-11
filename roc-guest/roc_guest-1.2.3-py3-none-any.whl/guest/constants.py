#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin constant variables."""
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

__all__ = [
    'ADS_GSE_STRFTIME',
    'INVALID_PACKET_TIME',
    'TESTLOG_STRFTIME',
    'CURDIR',
    'JINJA_TEMPLATE_DIR',
    'JENV',
    'TESTLOG_TEMPLATE',
    'TIME_RANGE_STRFORMAT',
    'TIME_ISO_STRFORMAT',
    'INPUT_TIME_STRFORMAT',
    'TESTLOG_EVENTDATE_STRFORMAT',
    'TESTLOG_EVENTTIME_STRFORMAT',
    'INPUT_DATETIME_STRFTIME',
    'INVALID_ADS_TIME',
    'TCREPORT_STRTFORMAT',
    'INVALID_UTC_DATETIME',
    'INVALID_UTC_TIME',
    'SCOS_HEADER_BYTES',
    'DATA_VERSION',
]

# output format for string time in ADS GSE text file (e.g., 2018-08-06T14:15:47.375Z)
ADS_GSE_STRFTIME = "%Y-%m-%dT%H:%M:%S.%fZ"

# Time value for invalid packet
INVALID_PACKET_TIME = "0000-00-00T00:00:00.000Z"

# Time iso format
TIME_ISO_STRFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# TC report time format
TCREPORT_STRTFORMAT = TIME_ISO_STRFORMAT

# value for invalid UTC Time
INVALID_UTC_TIME = '2000-01-01T00:00:00.000000Z'
INVALID_UTC_DATETIME = datetime.strptime(INVALID_UTC_TIME,
                                        TCREPORT_STRTFORMAT)

INPUT_DATETIME_STRFTIME = "%Y-%m-%dT%H:%M:%S"
TESTLOG_STRFTIME = "%Y-%m-%dT%H:%M:%S"

# Setup jinja2 environment
CURDIR = os.path.abspath(os.path.dirname(__file__))
JINJA_TEMPLATE_DIR = os.path.join(CURDIR, "templates")
JENV = Environment(loader=FileSystemLoader(JINJA_TEMPLATE_DIR))
# Jinja2 template for GSE test log XML
TESTLOG_TEMPLATE = "gse_test_log.tpl"

TIME_RANGE_STRFORMAT = "%Y%m%dT%H%M%S"
INPUT_TIME_STRFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
TESTLOG_EVENTDATE_STRFORMAT = "%Y-%m-%d"
TESTLOG_EVENTTIME_STRFORMAT = "%H:%M:%S.%f"

# Invalid line in the ADS GSE text file
INVALID_ADS_TIME = '0000-00-00T00:00:00.000Z'

# Length in bytes of the TM SCOS HEADER
SCOS_HEADER_BYTES = 76

# DEfault data version
DATA_VERSION = '01'
