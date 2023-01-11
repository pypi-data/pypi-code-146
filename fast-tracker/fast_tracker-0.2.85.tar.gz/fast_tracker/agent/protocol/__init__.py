#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from abc import ABC
from queue import Queue


class Protocol(ABC):
    def connected(self):
        raise NotImplementedError()

    def heartbeat(self):
        raise NotImplementedError()

    def report(self, queue: Queue, block: bool = True):
        raise NotImplementedError()
