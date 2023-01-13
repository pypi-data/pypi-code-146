#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from fast_tracker import Layer, ComponentType
from fast_tracker.trace import tags
from fast_tracker.trace.context import get_context
from fast_tracker.trace.tags import Tag
from fast_tracker import config
from fast_tracker.utils import functions


def install():
    from requests import Session

    _request = Session.request

    def _fast_request(
        this: Session,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):

        from urllib.parse import urlparse

        url_param = urlparse(url)

        # ignore trace fast_tracker self request
        if config.protocol == "http" and config.collector_address.rstrip("/").endswith(url_param.netloc):
            return _request(
                this,
                method,
                url,
                params,
                data,
                headers,
                cookies,
                files,
                auth,
                timeout,
                allow_redirects,
                proxies,
                hooks,
                stream,
                verify,
                cert,
                json,
            )

        context = get_context()
        with context.new_exit_span(op=url_param.path or "/", peer=url_param.netloc) as span:
            carrier = span.inject()
            span.layer = Layer.Http
            span.component = ComponentType.Requests

            if headers is None:
                headers = {}
            for item in carrier:
                headers[item.key] = item.val

            span.tag(Tag(key=tags.HttpMethod, val=method.upper()))
            span.tag(Tag(key=tags.HttpUrl, val=url))
            # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
            span.tag(Tag(key=tags.HttpPath, val=url_param.path))

            res = _request(
                this,
                method,
                url,
                params,
                data,
                headers,
                cookies,
                files,
                auth,
                timeout,
                allow_redirects,
                proxies,
                hooks,
                stream,
                verify,
                cert,
                json,
            )

            span.tag(Tag(key=tags.HttpStatus, val=res.status_code, overridable=True))
            if res.status_code >= 400:
                span.error_occurred = True

            functions.log("requests span is: %r", span)

            return res

    Session.request = _fast_request
