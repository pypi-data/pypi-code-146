#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

import uuid

from fast_tracker.utils.counter import AtomicCounter

_id = AtomicCounter()


class ID(object):
    def __init__(self, raw_id: str = None):
        self.value = raw_id or str(uuid.uuid1()).replace('-', '')

    def __str__(self):
        return self.value
