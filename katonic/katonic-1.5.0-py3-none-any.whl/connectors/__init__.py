#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from katonic.version import get_version


def version() -> str:
    """Returns the version of the current Katonic SDK."""
    return get_version()  # type: ignore
