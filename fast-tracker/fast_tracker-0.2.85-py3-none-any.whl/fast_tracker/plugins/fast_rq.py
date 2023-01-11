#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2023/1/9
"""

from fast_tracker import config
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.utils import functions


def install():
    from rq.worker import Worker

    def _fast_execute_job(this: Worker, job, queue):
        context = get_context()
        carrier = Carrier()
        trace_id_name = config.get_trace_id_name()
        trace_id = job.meta.get(trace_id_name, "")
        functions.log("RQ span is: %r", trace_id)
        for item in carrier:
            if type(item) is Carrier:
                item.set_frontend_trace_id(trace_id)
        with context.new_entry_span(op="RQ", carrier=carrier) as span:
            functions.log("RQ span is: %r", span)
            return this.perform_job(job, queue)

    Worker.execute_job = _fast_execute_job
