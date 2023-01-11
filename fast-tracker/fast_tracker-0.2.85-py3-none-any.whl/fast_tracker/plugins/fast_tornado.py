#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
from inspect import iscoroutinefunction, isawaitable

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils import functions
from fast_tracker.utils.reader_type import ReaderType


def install():
    # todo: 后续需要对此插件做版本控制，现在仅支持5.1.1版本， 6+没支持
    from tornado.web import RequestHandler

    old_execute = RequestHandler._execute
    old_log_exception = RequestHandler.log_exception
    RequestHandler._execute = _gen_fast_get_response_func(old_execute)

    def _fast_handler_uncaught_exception(self: RequestHandler, ty, value, tb, *args, **kwargs):
        if value is not None:
            entry_span = get_context().active_span()
            if entry_span is not None:
                entry_span.raised()

        return old_log_exception(self, ty, value, tb, *args, **kwargs)

    RequestHandler.log_exception = _fast_handler_uncaught_exception


def _gen_fast_get_response_func(old_execute):
    from tornado.gen import coroutine

    awaitable = iscoroutinefunction(old_execute)
    if awaitable:
        # Starting Tornado 6 RequestHandler._execute method is a standard Python coroutine (async/await)
        # In that case our method should be a coroutine function too
        async def _fast_get_response(self, *args, **kwargs):
            request = self.request
            context = get_context()
            carrier = Carrier()
            trace_id_name = config.get_trace_id_name()
            for item in carrier:
                if item.key.capitalize() in request.headers:
                    item.val = request.headers[item.key.capitalize()]
                if item.key.upper() in request.headers:
                    item.val = request.headers[item.key.upper()]
                if trace_id_name.capitalize() in request.headers and type(item) is Carrier:
                    item.set_frontend_trace_id(request.headers[trace_id_name.capitalize()])
                if trace_id_name.upper() in request.headers and type(item) is Carrier:
                    item.set_frontend_trace_id(request.headers[trace_id_name.upper()])
            with context.new_entry_span(op=request.path, carrier=carrier) as span:
                span.layer = Layer.Http
                span.component = ComponentType.Tornado
                try:
                    # self.request.connection.context.address  get ('::1', 52857, 0, 0) sometimes got error
                    span.peer = self.request.host  # got like: localhost:8888
                except BaseException as e:
                    span.peer = self.request.headers.get("X-Real-IP") or \
                            self.request.headers.get("X-Forwarded-For") or \
                            self.request.remote_ip  # ::1
                    pass
                span.tag(Tag(key=tags.HttpMethod, val=request.method))
                span.tag(Tag(key=tags.HttpUrl, val="{}://{}{}".format(request.protocol, request.host, request.path)))
                # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
                span.tag(Tag(key=tags.HttpPath, val=(request.path).split("?")[0]))
                result = old_execute(self, *args, **kwargs)
                if isawaitable(result):
                    result = await result
                span.tag(Tag(key=tags.HttpStatus, val=self._status_code, overridable=True))
                if self._status_code >= 400:
                    span.error_occurred = True

                # tenant_code\user_code\env_code 根据配置动态获取并更新
                set_code(config.tenant_code_reader, request, "tenant_code")
                set_code(config.user_code_reader, request, "user_code")
                set_code(config.env_code_reader, request, "env_code")
            return result

    else:

        @coroutine
        def _fast_get_response(self, *args, **kwargs):
            request = self.request
            context = get_context()
            carrier = Carrier()
            trace_id_name = config.get_trace_id_name()
            for item in carrier:
                if item.key.capitalize() in request.headers:
                    item.val = request.headers[item.key.capitalize()]
                if item.key.upper() in request.headers:
                    item.val = request.headers[item.key.upper()]
                if trace_id_name.capitalize() in request.headers and type(item) is Carrier:
                    item.set_frontend_trace_id(request.headers[trace_id_name.capitalize()])
                if trace_id_name.upper() in request.headers and type(item) is Carrier:
                    item.set_frontend_trace_id(request.headers[trace_id_name.upper()])
            with context.new_entry_span(op=request.path, carrier=carrier) as span:
                span.layer = Layer.Http
                span.component = ComponentType.Tornado
                # v6+use this
                # peer = request.connection.stream.socket.getpeername()
                # peer = self.stream.socket.getpeername()
                # v5.1.1 use this
                try:
                    # self.request.connection.context.address  get ('::1', 52857, 0, 0) sometimes got error
                    span.peer = self.request.host
                except BaseException as e:
                    span.peer = self.request.headers.get("X-Real-IP") or \
                            self.request.headers.get("X-Forwarded-For") or \
                            self.request.remote_ip  # ::1
                    pass
                span.tag(Tag(key=tags.HttpMethod, val=request.method))
                span.tag(Tag(key=tags.HttpUrl, val="{}://{}{}".format(request.protocol, request.host, request.path)))
                result = yield from old_execute(self, *args, **kwargs)
                span.tag(Tag(key=tags.HttpStatus, val=self._status_code, overridable=True))
                if self._status_code >= 400:
                    span.error_occurred = True

                set_code(config.tenant_code_reader, request, "tenant_code")
                set_code(config.user_code_reader, request, "user_code")
                set_code(config.env_code_reader, request, "env_code")

                functions.log("tornado span is: %r", span)
            return result

    return _fast_get_response


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
    reader_key = reader.get("ReaderKey")
    try:
        if reader_type == ReaderType.Cookie:
            # # tornado6.0.4 is ok
            # code = request.get_cookie(reader_key, "")
            # tornado5.1.1 is ok
            # code: Set-Cookie: env_c=gog <Morsel: env_c=gog>
            # request.cookies is A dictionary of Cookie.Morsel objects
            # tornado5.1.1 source code->tornado-httputil.py-HTTPServerRequest-cookies
            cookie = request.cookies.get(reader_key, "")
            if type(cookie) == str:
                code = cookie
            else:
                code = request.cookies.get(reader_key, "").value
            # code = request.cookies.get(reader_key, "").value
        elif reader_type == ReaderType.RequestHeader:
            code = request.headers[reader_key] if reader_key in request.headers else ""
        elif reader_type == ReaderType.QueryString:
            # data = json.loads(request.body.decode('utf-8'))
            # # tornado6.0.4 is ok
            # code = request.get_argument(reader_key, default="") if request.arguments.has_key(reader_key) else ""
            # tornado5.1.1
            arg = request.arguments.get(reader_key)
            code = arg[0].decode("utf-8") if type(arg) == list else ""
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
    except BaseException as e:
        functions.log("tornado 获取code错误，错误信息: %r", str(e))

    return code
