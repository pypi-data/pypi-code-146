#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

import time
from typing import List, TYPE_CHECKING

from fast_tracker import config

from fast_tracker.trace import ID
from fast_tracker.utils.lang import tostring

if TYPE_CHECKING:
    from fast_tracker.trace.carrier import Carrier
    from fast_tracker.trace.span import Span
    from fast_tracker.trace.snapshot import Snapshot


class SegmentRef(object):
    def __init__(self, carrier: "Carrier", ref_type: str = "CrossProcess"):
        self.ref_type = ref_type  # type: str
        self.trace_id = carrier.trace_id  # type: str
        self.segment_id = carrier.segment_id  # type: str
        self.span_id = carrier.span_id if carrier.span_id else ""  # type: str
        self.service = carrier.service  # type: str
        self.service_instance = carrier.service_instance  # type: str
        self.endpoint = carrier.endpoint  # type: str
        self.client_address = carrier.client_address  # type: str

    def __eq__(self, other):
        if not isinstance(other, SegmentRef):
            raise NotImplementedError
        return (
            self.ref_type == other.ref_type
            and self.trace_id == other.trace_id
            and self.segment_id == other.segment_id
            and self.span_id == other.span_id
            and self.service == other.service
            and self.service_instance == other.service_instance
            and self.endpoint == other.endpoint
            and self.client_address == other.client_address
        )

    @classmethod
    def build_ref(cls, snapshot: "Snapshot"):
        from fast_tracker.trace.carrier import Carrier

        carrier = Carrier()
        carrier.trace_id = str(snapshot.trace_id)
        carrier.segment_id = str(snapshot.segment_id)
        carrier.endpoint = snapshot.endpoint
        carrier.span_id = snapshot.span_id
        carrier.service = config.service_name
        carrier.service_instance = config.service_instance
        return SegmentRef(carrier, ref_type="CrossThread")


class _NewID(ID):
    pass


@tostring
class Segment(object):
    def __init__(self):
        self.segment_id = ID()  # type: ID
        self.spans = []  # type: List[Span]
        self.timestamp = int(time.time() * 1000)  # type: int
        self.related_traces = [_NewID()]  # type: List[ID]

    def archive(self, span: "Span"):
        self.spans.append(span)

    def relate(self, trace_id: ID):
        if isinstance(self.related_traces[0], _NewID):
            del self.related_traces[-1]
        self.related_traces.append(trace_id)
