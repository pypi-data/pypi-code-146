#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import pkg_resources  # type: ignore


def get_version():
    """
    Returns version information of the KFS Python Package
    """

    try:
        sdk_version = pkg_resources.get_distribution("katonic").version
    except pkg_resources.DistributionNotFound:
        sdk_version = "unknown"
    return sdk_version
