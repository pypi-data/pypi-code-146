#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains some useful methods for GUEST plugin.
"""


import argparse
from datetime import datetime
import logging
import os

from roc.guest.constants import INPUT_DATETIME_STRFTIME
from roc.guest.exceptions import GuestException

__all__ = ['valid_time', 'raise_error', 'valid_single_file', 'valid_data_version']

logger = logging.getLogger(__name__)

def raise_error(message, exception=GuestException):
    """Add an error entry to the logger and raise an exception."""
    logger.error(message)
    raise exception(message)

def valid_data_version(data_version):
    """
    Make sure to have a valid data version.

    :param data_version: integer or string containing the data version
    :return: string containing valid data version (i.e., 2 digits string)
    """
    try:
        if isinstance(data_version, list):
            data_version = data_version[0]
        data_version = int(data_version)
        return f"{data_version:02d}"
    except ValueError:
        raise_error(f"Input value for --data-version is not valid! ({data_version})")

def valid_single_file(file):
    """
    Make sure to have a valid single file.

    :param file: 1-element list or string containing the path to the file
    :return:
    """
    try:
        if isinstance(file, list):
            file = file[0]
        if os.path.isfile(file):
            return file
        else:
            raise FileNotFoundError
    except FileNotFoundError:
           raise_error(f"Input file not found! ({file})",
                       exception=FileNotFoundError)
    except ValueError:
        raise_error(f"Input file is not valid! ({file})",
                    exception=ValueError)
    except Exception as e:
        raise_error(f"Problem with input file! ({file})",
                    exception=e)

def valid_time(t, format=INPUT_DATETIME_STRFTIME):
    """
    Validate input datetime string format.

    :param t: input datetime string
    :param format: expected datetime string format
    :return: datetime object with input datetime info
    """
    if t:
        try:
            return datetime.strptime(t, format)
        except ValueError:
            raise_error(f"Not a valid datetime: '{t}'.",
                    exception=argparse.ArgumentTypeError)
