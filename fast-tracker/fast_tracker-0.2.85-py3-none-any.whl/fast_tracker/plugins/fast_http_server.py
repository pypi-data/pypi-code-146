#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

import inspect

from fast_tracker import Layer, ComponentType, config
from fast_tracker.trace import tags
from fast_tracker.trace.carrier import Carrier
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag


def install():
    from http.server import BaseHTTPRequestHandler

    _handle = BaseHTTPRequestHandler.handle

    def _fast_handle(handler: BaseHTTPRequestHandler):
        clazz = handler.__class__
        if 'werkzeug.serving.WSGIRequestHandler' == ".".join([clazz.__module__, clazz.__name__]):
            wrap_werkzeug_request_handler(handler)
        else:
            wrap_default_request_handler(handler)
        _handle(handler)

    BaseHTTPRequestHandler.handle = _fast_handle

    def _fast_send_response_only(self, code, *args, **kwargs):
        self._status_code = code

        return _send_response_only(self, code, *args, **kwargs)

    _send_response_only = BaseHTTPRequestHandler.send_response_only
    BaseHTTPRequestHandler.send_response_only = _fast_send_response_only


def wrap_werkzeug_request_handler(handler):
    """
    Wrap run_wsgi of werkzeug.serving.WSGIRequestHandler to add fast_tracker instrument code.
    """
    _run_wsgi = handler.run_wsgi

    def _wrap_run_wsgi():
        context = get_context()
        carrier = Carrier()
        trace_id_name = config.get_trace_id_name()
        for item in carrier:
            if trace_id_name.capitalize() in handler.headers and type(item) is Carrier:
                item.set_frontend_trace_id(handler.headers[trace_id_name.capitalize()])
            item.val = handler.headers[item.key.capitalize()]
        path = handler.path or '/'
        with context.new_entry_span(op=path.split("?")[0], carrier=carrier) as span:
            url = 'http://' + handler.headers["Host"] + path if 'Host' in handler.headers else path
            span.layer = Layer.Http
            span.component = ComponentType.General
            span.peer = '%s:%s' % handler.client_address
            span.tag(Tag(key=tags.HttpMethod, val=handler.command))
            span.tag(Tag(key=tags.HttpUrl, val=url))
            # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
            span.tag(Tag(key=tags.HttpPath, val=path))

            try:
                return _run_wsgi()
            finally:
                status_code = int(getattr(handler, '_status_code', -1))
                if status_code > -1:
                    span.tag(Tag(key=tags.HttpStatus, val=status_code, overridable=True))
                    if status_code >= 400:
                        span.error_occurred = True

    handler.run_wsgi = _wrap_run_wsgi

    def _fast_send_response(self, code, *args, **kwargs):
        self._status_code = code

        return _send_response(self, code, *args, **kwargs)

    WSGIRequestHandler = handler.__class__

    if not getattr(WSGIRequestHandler, '_fast_wrapped', False):
        _send_response = WSGIRequestHandler.send_response
        WSGIRequestHandler.send_response = _fast_send_response
        WSGIRequestHandler._fast_wrapped = True


def wrap_default_request_handler(handler):
    http_methods = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH')
    for method in http_methods:
        _wrap_do_method(handler, method)


def _wrap_do_method(handler, method):
    if hasattr(handler, 'do_' + method) and inspect.ismethod(getattr(handler, 'do_' + method)):
        _do_method = getattr(handler, 'do_' + method)

        def _fast_do_method():
            context = get_context()
            carrier = Carrier()
            trace_id_name=config.get_trace_id_name()
            for item in carrier:
                item.val = handler.headers[item.key.capitalize()]
                if trace_id_name.capitalize() in handler.headers and type(item) is Carrier:
                    item.set_frontend_trace_id(handler.headers[trace_id_name.capitalize()])
            path = handler.path or '/'
            with context.new_entry_span(op=path.split("?")[0], carrier=carrier) as span:
                url = 'http://' + handler.headers["Host"] + path if 'Host' in handler.headers else path
                span.layer = Layer.Http
                span.component = ComponentType.General
                span.peer = '%s:%s' % handler.client_address
                span.tag(Tag(key=tags.HttpMethod, val=method))
                span.tag(Tag(key=tags.HttpUrl, val=url))

                try:
                    _do_method()
                finally:
                    status_code = int(getattr(handler, '_status_code', -1))
                    if status_code > -1:
                        span.tag(Tag(key=tags.HttpStatus, val=status_code, overridable=True))
                        if status_code >= 400:
                            span.error_occurred = True

        setattr(handler, 'do_' + method, _fast_do_method)
