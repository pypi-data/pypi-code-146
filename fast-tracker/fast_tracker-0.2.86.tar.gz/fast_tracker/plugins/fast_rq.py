#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2023/1/9
"""

from fast_tracker import config, ComponentType
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.utils import functions


def install():
    from rq.job import Job

    _job_perform = Job.perform

    def _fast_job_perform(this: Job):
        context = get_context()
        carrier = Carrier()
        trace_id_name = config.get_trace_id_name()
        trace_id = this.meta.get(trace_id_name)
        for item in carrier:
            if type(item) is Carrier and trace_id:
                item.set_frontend_trace_id(trace_id)
        functions.log("job info %s %s", this.kwargs, this.meta)
        with context.new_entry_span(op="RQ", carrier=carrier) as span:
            span.extract(carrier)
            return _job_perform(this)

    Job.perform = _fast_job_perform

    _job_create = Job.create

    def _fast_job_create(this: Job, *arg, **kwargs):
        context = get_context()
        trace_id_name = config.get_trace_id_name()
        trace_id = ""
        with context.new_exit_span(op=ComponentType.Falcon, peer="rq queue") as span:
            carrier = span.inject()
            for item in carrier:
                if getattr(item, "trace_id", None):
                    trace_id = item.trace_id
                    break
            if not kwargs.get("meta"):
                kwargs["meta"] = {trace_id_name: trace_id}
            else:
                kwargs["meta"][trace_id_name] = trace_id
        return _job_create(this, *arg, **kwargs)

    Job.create = _fast_job_create
