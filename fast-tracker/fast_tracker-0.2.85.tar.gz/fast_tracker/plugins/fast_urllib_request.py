#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from urllib.request import Request

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker.utils import functions


def install():
    import socket
    from urllib.request import OpenerDirector
    from urllib.error import HTTPError
    from urllib.parse import urlsplit

    _open = OpenerDirector.open

    def _fast_open(this: OpenerDirector, fullurl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        if isinstance(fullurl, str):
            fullurl = Request(fullurl, data)

        context = get_context()
        url = fullurl.selector.split("?")[0] if fullurl.selector else "/"
        with context.new_exit_span(op=url, peer=fullurl.host) as span:
            carrier = span.inject()
            span.layer = Layer.Http
            span.component = ComponentType.General
            code = None

            [fullurl.add_header(item.key, item.val) for item in carrier]

            try:
                res = _open(this, fullurl, data, timeout)
                code = res.code
            except HTTPError as e:
                code = e.code
                raise
            finally:  # we do this here because it may change in _open()
                span.tag(Tag(key=tags.HttpMethod, val=fullurl.get_method()))
                span.tag(Tag(key=tags.HttpUrl, val=fullurl.full_url))
                # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
                # urlsplit 与 urlparse 的对比参考 fast_urllib3.py
                split_url = urlsplit(fullurl.selector)
                span.tag(Tag(key=tags.HttpPath, val=split_url.path))

                if code is not None:
                    span.tag(Tag(key=tags.HttpStatus, val=code, overridable=True))

                    if code >= 400:
                        span.error_occurred = True

            functions.log("urllib_request span is: %r", span)

            return res

    OpenerDirector.open = _fast_open
