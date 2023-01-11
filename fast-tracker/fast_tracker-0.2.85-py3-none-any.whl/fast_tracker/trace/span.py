#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

import time
import traceback
from abc import ABC
from copy import deepcopy
from typing import List
from typing import TYPE_CHECKING

from fast_tracker import Kind, Layer, Log, Component, LogItem, config
from fast_tracker.trace import ID
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.segment import SegmentRef, Segment
from fast_tracker.trace.tags import Tag
from fast_tracker.utils.lang import tostring

if TYPE_CHECKING:
    from fast_tracker.trace.context import SpanContext


@tostring
class Span(ABC):
    def __init__(
        self,
        context: "SpanContext",
        sid: str = "",
        pid: str = "",
        op: str = None,
        peer: str = None,
        kind: Kind = None,
        component: Component = None,
        layer: Layer = None,
    ):
        self.context = context  # type: SpanContext
        self.sid = sid  # type: str
        self.pid = pid  # type: str
        self.op = op  # type: str
        self.peer = peer  # type: str
        self.kind = kind  # type: Kind
        self.component = component or Component.Unknown  # type: Component
        self.layer = layer or Layer.Local  # type: Layer

        self.tags = []  # type: List[Tag]
        self.logs = []  # type: List[Log]
        self.refs = []  # type: List[SegmentRef]
        self.start_time = 0  # type: int
        self.end_time = 0  # type: int
        self.error_occurred = False  # type: bool

    def start(self):
        self.start_time = int(time.time() * 1000)
        self.context.start(self)

    def stop(self):
        return self.context.stop(self)

    def finish(self, segment: "Segment") -> bool:
        self.end_time = int(time.time() * 1000)
        segment.archive(self)
        return True

    def raised(self) -> "Span":
        self.error_occurred = True
        self.logs = [
            Log(
                items=[
                    LogItem(key="Error", val=self.format_exc()),
                ]
            )
        ]
        return self

    def format_exception(self, etype, value, tb, limit=None, chain=True):
        """Format a stack trace and the exception information.

        The arguments have the same meaning as the corresponding arguments
        to print_exception().  The return value is a list of strings, each
        ending in a newline and some containing internal newlines.  When
        these lines are concatenated and printed, exactly the same text is
        printed as does print_exception().
        """
        # format_exception has ignored etype for some time, and code such as cgitb
        # passes in bogus values as a result. For compatibility with such code we
        # ignore it here (rather than in the new TracebackException API).
        # 重写了python的traceback.py中的两个方法：format_exception、format_exc，但并未覆盖这两个方法
        data = traceback.TracebackException(type(value), value, tb, limit=limit)
        err = data._str
        err_log = data.stack[-1]
        trace = "filename:{fn}, line:{ln}, lineno:{lo}, func_name:{fu}".format(
            fn=err_log.filename, ln=err_log.line, lo=err_log.lineno, fu=err_log.name
        )
        err_type = str(data.exc_type)
        return {"err_msg": err, "err_type": err_type, "err_trace": trace}

    def format_exc(self, limit=None, chain=True):
        import sys

        # self.format_exception(*sys.exc_info(), limit=limit, chain=chain)
        """Like print_exc() but return a string."""
        # return "".join(self.format_exception(*sys.exc_info(), limit=limit, chain=chain))
        return self.format_exception(*sys.exc_info(), limit=limit, chain=chain)

    def log(self, ex: Exception) -> "Span":
        self.error_occurred = True
        self.logs.append(Log(items=[LogItem(key="Error", val=str(ex))]))
        return self

    def tag(self, tag: Tag) -> "Span":
        if tag.overridable:
            for i, t in enumerate(self.tags):
                if t.key == tag.key:
                    self.tags[i] = deepcopy(tag)
                    return self

        self.tags.append(deepcopy(tag))

        return self

    def inject(self) -> "Carrier":
        raise RuntimeWarning("只能将上下文载体注入ExitSpan，这可能是代理中的潜在错误，如果遇到这种情况，请在联系fast_tracker团队。 ")

    def extract(self, carrier: "Carrier") -> "Span":
        if carrier is None:
            return self

        self.context.segment.relate(ID(carrier.trace_id))
        self.context._correlation = carrier.correlation_carrier.correlation
        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.raised()
        self.stop()
        if exc_tb is not None:
            return False
        return True


@tostring
class StackedSpan(Span):
    def __init__(self, *args, **kwargs):
        Span.__init__(self, *args, **kwargs)
        self._depth = 0

    def start(self):
        self._depth += 1
        if self._depth == 1:
            Span.start(self)

    def stop(self):
        self._depth -= 1
        if self._depth == 0:
            Span.stop(self)


@tostring
class EntrySpan(StackedSpan):
    def __init__(
        self,
        context: "SpanContext",
        sid: str = "",
        pid: str = "",
        op: str = None,
        peer: str = None,
        component: "Component" = None,
        layer: "Layer" = None,
    ):
        StackedSpan.__init__(
            self,
            context,
            sid,
            pid,
            op,
            peer,
            Kind.Entry,
            component,
            layer,
        )
        self._max_depth = 0

    def start(self):
        StackedSpan.start(self)
        self._max_depth = self._depth
        self.component = 0
        self.layer = Layer.Local
        self.logs = []
        self.tags = []

    def extract(self, carrier: "Carrier") -> "Span":
        Span.extract(self, carrier)

        if carrier is None or not carrier.is_valid:
            return self

        ref = SegmentRef(carrier=carrier)

        if ref not in self.refs:
            self.refs.append(ref)

        return self


@tostring
class ExitSpan(StackedSpan):
    def __init__(
        self,
        context: "SpanContext",
        sid: str = "",
        pid: str = "",
        op: str = None,
        peer: str = None,  # 节点信息 节点的地址和端口
        component: "Component" = None,
        layer: "Layer" = None,
    ):
        StackedSpan.__init__(
            self,
            context,
            sid,
            pid,
            op,
            peer,
            Kind.Exit,
            component,
            layer,
        )

    def inject(self) -> "Carrier":
        return Carrier(
            trace_id=str(self.context.segment.related_traces[0]),
            segment_id=str(self.context.segment.segment_id),
            span_id=str(self.sid),
            service=config.service_name,
            service_instance=config.service_instance,
            endpoint=self.op,
            client_address=self.peer,
            correlation=self.context._correlation,
        )


@tostring
class NoopSpan(Span):
    def __init__(self, context: "SpanContext" = None, kind: "Kind" = None):
        Span.__init__(self, context=context, kind=kind)

    def extract(self, carrier: "Carrier"):
        if carrier is not None:
            self.context._correlation = carrier.correlation_carrier.correlation

    def inject(self) -> "Carrier":
        return Carrier(correlation=self.context._correlation)
