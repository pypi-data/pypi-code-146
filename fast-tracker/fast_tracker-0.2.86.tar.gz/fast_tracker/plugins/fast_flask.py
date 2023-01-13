#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.span import NoopSpan
from fast_tracker.trace.tags import Tag
from fast_tracker.utils import functions
from fast_tracker.utils.reader_type import ReaderType


def install():
    from flask import Flask

    _full_dispatch_request = Flask.full_dispatch_request
    _handle_user_exception = Flask.handle_user_exception
    _handle_exception = Flask.handle_exception

    def params_tostring(params):
        return "\n".join([k + "=[" + ",".join(params.getlist(k)) + "]" for k, _ in params.items()])

    def _fast_full_dispatch_request(this: Flask):
        import flask

        req = flask.request
        context = get_context()
        carrier = Carrier()
        trace_id_name = config.get_trace_id_name()
        for item in carrier:
            if item.key.capitalize() in req.headers:
                item.val = req.headers[item.key.capitalize()]
            if trace_id_name.capitalize() in req.headers and type(item) is Carrier:
                item.set_frontend_trace_id(req.headers[trace_id_name.capitalize()])
        with context.new_entry_span(op=req.path, carrier=carrier) as span:
            span.layer = Layer.Http
            span.component = ComponentType.Flask
            span.peer = "%s:%s" % (req.environ["REMOTE_ADDR"], req.environ["REMOTE_PORT"])
            span.tag(Tag(key=tags.HttpMethod, val=req.method))
            span.tag(Tag(key=tags.HttpUrl, val=req.url.split("?")[0]))
            # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
            span.tag(Tag(key=tags.HttpPath, val=req.path))
            set_code(config.tenant_code_reader, req, "tenant_code")
            set_code(config.user_code_reader, req, "user_code")
            set_code(config.env_code_reader, req, "env_code")
            if req.values:
                span.tag(
                    Tag(key=tags.HttpParams, val=params_tostring(req.values)[0:])
                )
            resp = _full_dispatch_request(this)

            if resp.status_code >= 400:
                span.error_occurred = True

            span.tag(Tag(key=tags.HttpStatus, val=resp.status_code, overridable=True))
            functions.log("flask span is: %r", span)
            return resp

    def _fast_handle_user_exception(this: Flask, e):
        if e is not None:
            entry_span = get_context().active_span()
            if entry_span is not None and type(entry_span) is not NoopSpan:
                entry_span.raised()

        return _handle_user_exception(this, e)

    def _fast_handle_exception(this: Flask, e):
        if e is not None:
            entry_span = get_context().active_span()
            if entry_span is not None and type(entry_span) is not NoopSpan:
                entry_span.raised()

        return _handle_exception(this, e)

    Flask.full_dispatch_request = _fast_full_dispatch_request
    Flask.handle_user_exception = _fast_handle_user_exception
    Flask.handle_exception = _fast_handle_exception

    def set_code(reader, request, type="tenant_code"):
        """
        根据配置从不同渠道（cookie\header\querystring\env）获取tenant_code、user_code、env_code等数据
        :param reader:
        :param request:
        :param type:
        :return:
        """
        code = ""
        if not reader:
            return code

        reader_type = reader.get("ReaderType")

        if reader_type == ReaderType.Cookie:
            code = request.cookies.get(reader.get("ReaderKey"), "")
        elif reader_type == ReaderType.RequestHeader:
            code = request.headers[reader.get("ReaderKey")] if reader.get("ReaderKey") in request.headers else ""
        elif reader_type == ReaderType.QueryString:
            code = request.args.get(reader.get("ReaderKey"), "")
        elif reader_type == ReaderType.Environment:
            import os

            code = os.getenv(reader.get("ReaderKey"), "")
        else:
            code = ""

        if code:
            # 设置config的code，让其全局适用
            if type == "tenant_code":
                config.set_tenant_code(code)
            elif type == "user_code":
                config.set_user_code(code)
            elif type == "env_code":
                config.set_env_code(code)

        return code
