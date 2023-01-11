#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


def install():
    from elasticsearch import Transport

    _perform_request = Transport.perform_request

    def _fast_perform_request(this: Transport, method, url, headers=None, params=None, body=None):
        context = get_context()
        peer = ",".join([host["host"] + ":" + str(host["port"]) for host in this.hosts])
        with context.new_exit_span(op="Elasticsearch/" + method + url, peer=peer) as span:
            span.layer = Layer.Database
            span.component = ComponentType.Elasticsearch
            res = _perform_request(this, method, url, headers=headers, params=params, body=body)

            span.tag(Tag(key=tags.DbType, val=ComponentType.Elasticsearch))
            # have no instance
            span.tag(Tag(key=tags.DbInstance, val=""))
            span.tag(Tag(key=tags.DbStatement, val="" if body is None else body))
            # have no parameters
            span.tag(Tag(key=tags.DbSqlParameters, val=""))

            return res

    Transport.perform_request = _fast_perform_request
