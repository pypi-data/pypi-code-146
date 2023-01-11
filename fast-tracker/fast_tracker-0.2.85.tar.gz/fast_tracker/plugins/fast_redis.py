#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils import functions


def install():
    from redis.connection import Connection

    _send_command = Connection.send_command

    def _fast_send_command(this: Connection, *args, **kwargs):
        peer = "%s:%s" % (this.host, this.port)
        op = args[0]
        context = get_context()
        with context.new_exit_span(op="Redis/" + op or "/", peer=peer) as span:
            span.layer = Layer.Cache
            span.component = ComponentType.Redis
            res = _send_command(this, *args, **kwargs)
            span.tag(Tag(key=tags.CacheType, val=ComponentType.Redis))
            span.tag(Tag(key=tags.CacheInstance, val=this.db))
            span.tag(Tag(key=tags.CacheCommand, val=op))
            functions.log("redis span is: %r", span)

            return res

    Connection.send_command = _fast_send_command
