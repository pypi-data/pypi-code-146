# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from enum import IntEnum

from contrast.extern import structlog as logging
from contrast.reporting.teamserver_messages import (
    EVENT_TYPE_LOOKUP,
    EVENT_ACTION_LOOKUP,
)

logger = logging.getLogger("contrast")


class TraceEvent(object):
    """
    Wrapper around api.dtm_pb2.TraceEvent
    """

    class EventType(IntEnum):
        TYPE_METHOD = 0
        TYPE_PROPAGATION = 1
        TYPE_TAG = 2

    class Action(IntEnum):
        CREATION = 0
        PROPAGATION = 1
        TRIGGER = 2
        TAG = 3
        A2A = 4
        A2P = 5
        A2O = 6
        A2R = 7
        O2A = 8
        O2P = 9
        O2O = 10
        O2R = 11
        P2A = 12
        P2P = 13
        P2O = 14
        P2R = 15

    def __init__(self):
        self.action = self.Action.CREATION
        self.type = self.EventType.TYPE_METHOD
        self.timestamp_ms = 0
        self.thread = ""
        self.signature = TraceEventSignature()  # contrast.api.dtm.TraceEventSignature
        self.field_name = ""
        self.context = ""
        self.code = ""
        self.object = TraceEventObject()  # contrast.api.dtm.TraceEventObject
        self.ret = TraceEventObject()  # contrast.api.dtm.TraceEventObject
        self.args = []  # contrast.api.dtm.TraceEventObject
        self.stack = []  # contrast.api.dtm.TraceStack
        self.event_sources = []  # contrast.api.dtm.TraceEventSource
        self.tags = []

        self.source = ""
        self.target = ""
        self.taint_ranges = []  # repeated contrast.api.dtm.TraceTaintRange

        self.object_id = 0
        self.parent_object_ids = []  # repeated contrast.api.dtm.ParentObjectId

    def to_json(self):
        return {
            "action": EVENT_ACTION_LOOKUP[self.action],
            "args": [
                {
                    # "hash": 0,  # not required
                    "tracked": arg.tracked,
                    "value": arg.value,
                }
                for arg in self.args
            ],
            # "code": "string",  # currently unused; maybe useful in the future
            "eventSources": [
                {
                    "sourceName": s.name,
                    "sourceType": s.type,
                }
                for s in self.event_sources
            ],
            "fieldName": self.field_name,
            "object": {
                # "hash": 0,  # not required
                "tracked": self.object.tracked,
                "value": self.object.value,
            },
            "objectId": self.object_id,
            "parentObjectIds": [{"id": p.id} for p in self.parent_object_ids],
            # properties not used for dataflow rules
            # "properties": [{"key": "string", "value": "string"}],
            "ret": {
                # "hash": 0,  # not required
                "tracked": self.ret.tracked,
                "value": self.ret.value,
            },
            "signature": {
                "argTypes": list(self.signature.arg_types),
                "className": self.signature.class_name,
                "constructor": self.signature.constructor,
                # not required and we don't save this to the DTM
                # "expressionType": "MEMBER_EXPRESSION",
                # "flags": 0,  # java only
                "methodName": self.signature.method_name,
                # not required and we don't save this to the DTM
                # "operator": "string",
                "returnType": self.signature.return_type,
                # "signature": "string",  # deprecated
                "voidMethod": self.signature.void_method,
            },
            "source": self.source,
            "stack": [
                {
                    "eval": s.eval,
                    "file": s.file_name,
                    "lineNumber": s.line_number,
                    "method": s.method_name,
                    "signature": s.signature,
                    "type": s.type,
                }
                for s in self.stack
            ],
            # "tags": "string",  # we don't save this to the DTM
            "taintRanges": [
                {
                    "tag": t.tag,
                    "range": t.range,
                }
                for t in self.taint_ranges
            ],
            "target": self.target,
            # "thread": "string",  # not required
            "time": self.timestamp_ms,
            "type": EVENT_TYPE_LOOKUP[self.type],
        }


class TraceEventObject(object):
    """
    Wrapper around api.dtm_pb2.TraceEventObject
    """

    def __init__(self):
        self.tracked = False
        self.value = ""
        self.ranges = []  # contrast.api.dtm.TraceTaintRange


class TraceEventSignature(object):
    """
    Wrapper around api.dtm_pb2.TraceEventSignature
    """

    def __init__(self):
        self.return_type = ""
        self.class_name = ""
        self.method_name = ""
        self.arg_types = []
        self.constructor = False
        self.void_method = False
        self.flags = 0


class ParentObjectId(object):
    """
    Wrapper around api.dtm_pb2.ParentObjectId
    """

    def __init__(self):
        self.id = ""


class TraceEventSource(object):
    """
    Wrapper around api.dtm_pb2.TraceEventSource
    """

    def __init__(self):
        self.type = ""
        self.name = ""


class TraceStack(object):
    """
    Wrapper around api.dtm_pb2.TraceStack
    """

    def __init__(self):
        self.signature = ""
        self.declaring_class = ""
        self.method_name = ""
        self.file_name = ""
        self.line_number = 0
        self.type = ""
        self.eval = ""


class TraceTaintRange(object):
    """
    Wrapper around api.dtm_pb2.TraceTaintRange
    """

    def __init__(self):
        self.tag = ""
        self.range = ""
