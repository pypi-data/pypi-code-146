#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import os
import re
from datetime import datetime

from pytz import utc  # type: ignore


def make_tzaware(t: datetime) -> datetime:
    """We assume tz-naive datetimes are UTC"""
    return t.replace(tzinfo=utc) if t.tzinfo is None else t


def is_valid_name(name: str) -> bool:
    """A name should be alphanumeric values and underscores but not start with an underscore"""
    return not name.startswith("_") and re.compile(r"\W+").search(name) is None


# set environment variable
os.environ["DB_NAME"] = "bWxmbG93X2Ri"

os.environ[
    "HOST"
] = "bWxmbG93LXBvc3RncmVzLXBvc3RncmVzcWwtaGEtcG9zdGdyZXNxbC1oZWFkbGVzcy5hcHBsaWNhdGlvbi5zdmMuY2x1c3Rlci5sb2NhbA=="

os.environ["USER"] = "bWxmbG93X3VzZXI="

os.environ["POSTGRES_PASSWORD"] = "V0Qza3k1UUYwTVBCNGNVNFdicWE="

os.environ["DB_SCHEMA"] = "cHVibGlj"

os.environ["REDIS_HOST"] = "cmVkaXMtbWFzdGVyLmFwcGxpY2F0aW9u"

os.environ["REDIS_PASSWORD"] = "cmVkaXMxMjM="
