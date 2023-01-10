#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from roc.idb.constants import MIB_VERSION_STRFORMAT

__all__ = ['valid_mib_version']

def valid_mib_version(mib_version,
                      valid_format=MIB_VERSION_STRFORMAT):
    """
    Check if input MIB version is valid.

    :param mib_version: String containing the MIB version to check
    :param valid_format: string containing the valid MIB version format
    (use datetime.strptime convention)
    :return: mib version string if valid, otherwise raise an ValueError exception
    """

    try:
        # Use datetime to check if MIB version is valid
        _ = datetime.strptime(mib_version, valid_format)
    except:
        ValueError(f'Input MIB version {mib_version} is not valid!')

    return mib_version
