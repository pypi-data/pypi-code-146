#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils import functions
from fast_tracker.utils.reader_type import ReaderType

version_rule = {"name": "django", "rules": [">=2.0"]}


def install():
    from django.core.handlers.base import BaseHandler
    from django.core.handlers import exception

    _get_response = BaseHandler.get_response
    _handle_uncaught_exception = exception.handle_uncaught_exception

    def _fast_get_response(this, request):
        if request is None:
            resp = _get_response(this, request)
            return resp

        context = get_context()
        carrier = Carrier()
        for item in carrier:
            # Any HTTP headers in the request are converted to META keys by converting all characters to uppercase,
            # replacing any hyphens with underscores and adding an HTTP_ prefix to the name.
            # https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpRequest.META
            fast_http_header_key = "HTTP_%s" % item.key.upper().replace("-", "_")
            if fast_http_header_key in request.META:
                item.val = request.META[fast_http_header_key]

        with context.new_entry_span(op=request.path, carrier=carrier) as span:
            span.layer = Layer.Http
            span.component = ComponentType.Django
            span.peer = "%s:%s" % (request.META.get("REMOTE_ADDR"), request.META.get("REMOTE_PORT") or "80")

            span.tag(Tag(key=tags.HttpMethod, val=request.method))
            http_url = request.build_absolute_uri().split("?")[0]
            span.tag(Tag(key=tags.HttpUrl, val=http_url))
            span.tag(Tag(key=tags.HttpPath, val=request.META.get("PATH_INFO")))

            # tenant_code\user_code\env_code 根据配置动态获取并更新
            set_code(config.tenant_code_reader, request, "tenant_code")
            set_code(config.user_code_reader, request, "user_code")
            set_code(config.env_code_reader, request, "env_code")

            # you can get request parameters by `request.GET` even though client are using POST or other methods
            if request.GET:
                span.tag(
                    Tag(key=tags.HttpParams, val=params_tostring(request.GET)[0:])
                )

            resp = _get_response(this, request)
            span.tag(Tag(key=tags.HttpStatus, val=resp.status_code, overridable=True))
            if resp.status_code >= 400:
                span.error_occurred = True
            functions.log("django span is: %r", span)
            return resp

    def _fast_handle_uncaught_exception(request, resolver, exc_info):
        if exc_info is not None:
            entry_span = get_context().active_span()
            if entry_span is not None:
                entry_span.raised()

        return _handle_uncaught_exception(request, resolver, exc_info)

    BaseHandler.get_response = _fast_get_response
    exception.handle_uncaught_exception = _fast_handle_uncaught_exception

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
        reader_key = reader.get("ReaderKey")

        if reader_type == ReaderType.Cookie:
            code = request.COOKIES.get(reader_key, "")
        elif reader_type == ReaderType.RequestHeader:
            code = request.META[reader_key] if reader_key in request.headers else ""
        elif reader_type == ReaderType.QueryString:
            if request.method == "GET":
                code = request.GET.get(reader_key, default="")
            elif request.method == "POST":
                code = request.POST.get(reader_key, default="")
        elif reader_type == ReaderType.Environment:
            import os

            code = os.getenv(reader_key, "")
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


def params_tostring(params):
    return "\n".join([k + "=[" + ",".join(params.getlist(k)) + "]" for k, _ in params.items()])
