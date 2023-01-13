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
    from urllib3.request import RequestMethods

    _request = RequestMethods.request

    def _fast_request(this: RequestMethods, method, url, fields=None, headers=None, **urlopen_kw):

        from urllib.parse import urlparse

        # from urllib.parse import urlsplit
        # split_result=urlsplit("https://www.google.com.hk/search?q=python+url%3F+%E8%A7%A3%E6%9E%90%3F&newwindow=1&safe=strict&sxsrf=ALeKk00UWlOugflkW77YePhdTqe0wGavqA%3A1618295940827&ei=hDx1YLjzMder3AOd67a4Cw&oq=python+url%3F+%E8%A7%A3%E6%9E%90%3F&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgAEB4yBAgAEB4yBggAEAgQHjoHCAAQRxCwA1C9Ili9ImCjJmgBcAJ4AIABpAKIAZgEkgEDMi0ymAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwi4xcaVzvrvAhXXFXcKHZ21DbcQ4dUDCA4&uact=5")
        # SplitResult(scheme='https', netloc='www.google.com.hk', path='/search', query='q=python+url%3F+%E8%A7%A3%E6%9E%90%3F&newwindow=1&safe=strict&sxsrf=ALeKk00UWlOugflkW77YePhdTqe0wGavqA%3A1618295940827&ei=hDx1YLjzMder3AOd67a4Cw&oq=python+url%3F+%E8%A7%A3%E6%9E%90%3F&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgAEB4yBAgAEB4yBggAEAgQHjoHCAAQRxCwA1C9Ili9ImCjJmgBcAJ4AIABpAKIAZgEkgEDMi0ymAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwi4xcaVzvrvAhXXFXcKHZ21DbcQ4dUDCA4&uact=5', fragment='')
        url_param = urlparse(url)
        # ParseResult(scheme='https', netloc='www.google.com.hk', path='/search', params='', query='q=python+url%3F+%E8%A7%A3%E6%9E%90%3F&newwindow=1&safe=strict&sxsrf=ALeKk00UWlOugflkW77YePhdTqe0wGavqA%3A1618295940827&ei=hDx1YLjzMder3AOd67a4Cw&oq=python+url%3F+%E8%A7%A3%E6%9E%90%3F&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgAEB4yBAgAEB4yBggAEAgQHjoHCAAQRxCwA1C9Ili9ImCjJmgBcAJ4AIABpAKIAZgEkgEDMi0ymAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwi4xcaVzvrvAhXXFXcKHZ21DbcQ4dUDCA4&uact=5', fragment='')
        context = get_context()
        with context.new_exit_span(op=url_param.path or "/", peer=url_param.netloc) as span:
            carrier = span.inject()
            span.layer = Layer.Http
            span.component = ComponentType.Urllib3

            if headers is None:
                headers = {}
            for item in carrier:
                headers[item.key] = item.val

            span.tag(Tag(key=tags.HttpMethod, val=method.upper()))
            span.tag(Tag(key=tags.HttpUrl, val=url))
            # HttpPath 只需要获取PATH_INFO信息即可，不需要？后的内容
            span.tag(Tag(key=tags.HttpPath, val=(url_param.path).split("?")[0]))

            res = _request(this, method, url, fields=fields, headers=headers, **urlopen_kw)

            span.tag(Tag(key=tags.HttpStatus, val=res.status, overridable=True))
            if res.status >= 400:
                span.error_occurred = True

            functions.log("urllib3 span is: %r", span)

            return res

    RequestMethods.request = _fast_request
