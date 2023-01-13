#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fast_tracker.trace.context import SpanContext

from fast_tracker.trace import ID


class Snapshot:
    def __init__(
        self,
        segment_id: str = None,
        span_id: str = None,
        trace_id: ID = None,
        endpoint: str = None,
        correlation: dict = None,
    ):
        self.trace_id = trace_id  # type: ID
        self.segment_id = segment_id  # type: str
        self.span_id = span_id  # type: str
        self.endpoint = endpoint  # type: str
        self.correlation = correlation.copy()  # type: dict

    def is_from_current(self, context: "SpanContext"):
        return self.segment_id is not None and self.segment_id == context.capture().segment_id

    def is_valid(self):
        return self.trace_id is not None
