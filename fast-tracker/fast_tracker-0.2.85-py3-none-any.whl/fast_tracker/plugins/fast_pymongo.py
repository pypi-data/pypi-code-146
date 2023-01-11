#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag

version_rule = {"name": "pymongo", "rules": [">=3.7.0"]}


def install():
    from pymongo.bulk import _Bulk
    from pymongo.cursor import Cursor
    from pymongo.pool import SocketInfo

    bulk_op_map = {0: "insert", 1: "update", 2: "delete"}
    # handle insert_many and bulk write
    inject_bulk_write(_Bulk, bulk_op_map)

    # handle find() & find_one()
    inject_cursor(Cursor)

    # handle other commands
    inject_socket_info(SocketInfo)


def inject_socket_info(SocketInfo):
    _command = SocketInfo.command

    def _fast_command(this: SocketInfo, dbname, spec, *args, **kwargs):
        # pymongo sends `ismaster` command continuously. ignore it.
        if spec.get("ismaster") is None:
            address = this.sock.getpeername()
            peer = "%s:%s" % address
            context = get_context()

            operation = list(spec.keys())[0]
            fast_op = operation.capitalize() + "Operation"
            with context.new_exit_span(op="MongoDB/" + fast_op, peer=peer) as span:
                result = _command(this, dbname, spec, *args, **kwargs)

                span.layer = Layer.Database
                span.component = ComponentType.MongoDB
                span.tag(Tag(key=tags.DbType, val="MongoDB"))
                span.tag(Tag(key=tags.DbInstance, val=dbname))

                # get filters
                filters = _get_filter(operation, spec)
                span.tag(Tag(key=tags.DbStatement, val=filters))

        else:
            result = _command(this, dbname, spec, *args, **kwargs)

        return result

    SocketInfo.command = _fast_command


def _get_filter(request_type, spec):
    """
    :param request_type: the request param send to MongoDB
    :param spec: maybe a bson.SON class or a dict
    :return: filter string
    """
    from bson import SON

    if isinstance(spec, SON):
        spec = spec.to_dict()
        spec.pop(request_type)
    elif isinstance(spec, dict):
        spec = dict(spec)
        spec.pop(request_type)

    return request_type + " " + str(spec)


def inject_bulk_write(_Bulk, bulk_op_map):
    _execute = _Bulk.execute

    def _fast_execute(this: _Bulk, *args, **kwargs):
        address = this.collection.database.client.address
        peer = "%s:%s" % address
        context = get_context()

        fast_op = "MixedBulkWriteOperation"
        with context.new_exit_span(op="MongoDB/" + fast_op, peer=peer) as span:
            span.layer = Layer.Database
            span.component = ComponentType.MongoDB

            bulk_result = _execute(this, *args, **kwargs)

            span.tag(Tag(key=tags.DbType, val="MongoDB"))
            span.tag(Tag(key=tags.DbInstance, val=this.collection.database.name))
            filters = ""
            bulk_ops = this.ops
            for bulk_op in bulk_ops:
                opname = bulk_op_map.get(bulk_op[0])
                _filter = opname + " " + str(bulk_op[1])
                filters = filters + _filter + " "

            span.tag(Tag(key=tags.DbStatement, val=filters))

            return bulk_result

    _Bulk.execute = _fast_execute


def inject_cursor(Cursor):
    __send_message = Cursor._Cursor__send_message

    def _fast_send_message(this: Cursor, operation):
        address = this.collection.database.client.address
        peer = "%s:%s" % address

        context = get_context()
        op = "FindOperation"

        with context.new_exit_span(op="MongoDB/" + op, peer=peer) as span:
            span.layer = Layer.Database
            span.component = ComponentType.MongoDB

            # __send_message return nothing
            __send_message(this, operation)

            span.tag(Tag(key=tags.DbType, val=ComponentType.MongoDB))
            span.tag(Tag(key=tags.DbInstance, val=this.collection.database.name))

            filters = "find " + str(operation.spec)
            span.tag(Tag(key=tags.DbStatement, val=filters))

            return

    Cursor._Cursor__send_message = _fast_send_message
