#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by iprobeyang@gmail.com 2021/4/20
"""

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.span import NoopSpan
from fast_tracker.trace.tags import Tag
from fast_tracker.utils.reader_type import ReaderType


def install():
    from falcon import API, request, response

    _original_falcon_api = API.__call__
    _original_falcon_handle_exception = API._handle_exception

    def params_tostring(params):
        return "\n".join([k + "=" + v for k, v in params.items()])

    def _fast_falcon_api(this: API, env, start_response):
        context = get_context()
        carrier = Carrier()
        headers = get_headers(env)
        trace_id_name = config.get_trace_id_name()
        for item in carrier:
            if item.key.capitalize() in headers:
                item.val = headers[item.key.capitalize()]
            if item.key.upper() in headers:
                item.val = headers[item.key.upper()]
            if trace_id_name.capitalize() in headers and type(item) is Carrier:
                item.set_frontend_trace_id(headers[trace_id_name.capitalize()])
            if trace_id_name.upper() in headers and type(item) is Carrier:
                item.set_frontend_trace_id(headers[trace_id_name.upper()])
        with context.new_entry_span(op="/", carrier=carrier) as span:
            span.layer = Layer.Http
            span.component = ComponentType.Falcon

            resp = _original_falcon_api(this, env, start_response)

            from falcon import RequestOptions
            from falcon import ResponseOptions

            req = request.Request(env, RequestOptions())
            resp_obj = response.Response(ResponseOptions())

            span.op = str(req.url).split("?")[0]
            span.peer = "%s:%s" % (req.remote_addr, req.port)
            span.tag(Tag(key=tags.HttpMethod, val=req.method))
            span.tag(Tag(key=tags.HttpUrl, val=str(req.url)))
            span.tag(Tag(key=tags.HttpPath, val=str(req.url).split("?")[0]))
            if req.params:
                span.tag(
                    Tag(key=tags.HttpParams, val=params_tostring(req.params)[0:])
                )

            set_code(config.tenant_code_reader, req, "tenant_code")
            set_code(config.user_code_reader, req, "user_code")
            set_code(config.env_code_reader, req, "env_code")

            resp_status = parse_status(resp_obj.status)
            if int(resp_status[0]) >= 400:
                span.error_occurred = True

            return resp

    def _fast_handle_exception(this: API, req, resp, ex, params):
        if ex is not None:
            entry_span = get_context().active_span()
            if entry_span is not None and type(entry_span) is not NoopSpan:
                entry_span.raised()

        return _original_falcon_handle_exception(this, req, resp, ex, params)

    def set_code(reader, request, code_type="tenant_code"):
        """
        根据配置从不同渠道（cookie\header\querystring\env）获取tenant_code、user_code、env_code等数据
        :param reader:
        :param request:
        :param code_type:
        :return:
        """
        code = ""
        if not reader:
            return code

        reader_type = reader.get("ReaderType")

        if reader_type == ReaderType.Cookie:
            code = request.cookies.get(reader.get("ReaderKey"), "")
        elif reader_type == ReaderType.RequestHeader:
            # 下划线转中横杠
            code = ""
            if '_' in reader.get("ReaderKey"):
                reader["ReaderKey"] = reader.get("ReaderKey").replace('_', '-')
            if reader.get("ReaderKey") in request.headers:
                code = request.headers[reader.get("ReaderKey")]
            elif reader.get("ReaderKey").upper() in request.headers:
                code = request.headers[reader.get("ReaderKey").upper()]
            elif reader.get("ReaderKey").capitalize() in request.headers:
                code = request.headers[reader.get("ReaderKey").capitalize()]
        elif reader_type == ReaderType.QueryString:
            # import json
            # raw = request.stream.read()
            # raw_json = request.bounded_stream.read()
            # from urllib import parse
            # params = parse.parse_qsl(raw_json)
            code = request.params.get(reader.get("ReaderKey"), "")
        elif reader_type == ReaderType.Environment:
            import os

            code = os.getenv(reader.get("ReaderKey"), "")
        else:
            code = ""

        # 设置用户自定义字段值
        if code_type == "tenant_code" and not config.custom_tenant_code:
            config.custom_tenant_code = code
        elif code_type == "user_code" and not config.custom_user_code:
            config.custom_user_code = code
        elif code_type == "env_code" and not config.custom_env_code:
            config.custom_env_code = code

        return code

    API.__call__ = _fast_falcon_api
    API._handle_exception = _fast_handle_exception


def get_headers(env):
    """
    获取headers数据
    :param dict env: 环境变量
    :return:
    """
    headers = {}
    wsgi_content_headers = frozenset(["CONTENT_TYPE", "CONTENT_LENGTH"])

    for name, value in env.items():
        if name.startswith("HTTP_"):
            headers[name[5:].replace("_", "-")] = value

        elif name in wsgi_content_headers:
            headers[name.replace("_", "-")] = value

    return headers


def parse_status(status_str):
    """
    解析falcon的response的status数据，其结构类似：200 OK,参考：python3.8/site-packages/falcon/status_codes.py
    :param status_str:
    :return:
    """
    return status_str.split(" ") if status_str else [404, "status is empty"]
