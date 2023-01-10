#!/usr/bin/env python

"""CHIME/FRB Buckets."""

import logging

from chime_frb_api.modules import bucket

log = logging.getLogger(__name__)


class Bucket(bucket.Bucket):
    """CHIME/FRB Bucket Backend."""

    def __init__(self, debug: bool = False, **kwargs):
        # Instantiate Bucket Components
        super().__init__(debug=debug, **kwargs)
