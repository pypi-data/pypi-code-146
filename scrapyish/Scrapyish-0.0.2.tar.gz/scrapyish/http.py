import re
from urllib.parse import urljoin
import json


class Request:
    """
    Represents an HTTP request, which is usually generated in a Spider.
    """
    def __init__(self, url, callback=None, cb_kwargs=None) -> None:
        self._url = url
        self._callback = callback
        self._cb_kwargs = cb_kwargs

    @property
    def cb_kwargs(self) -> dict:
        if self._cb_kwargs is None:
            self._cb_kwargs = {}
        return self._cb_kwargs

    def _get_url(self) -> str:
        return self._url

    def _set_url(self, url: str) -> None:
        self._url = url

    @property
    def url(self):
        return self._url

    def __repr__(self) -> str:
        return f"<Req {self.url}>"



class Response:

    base_url_pattern = re.compile(r"<base\s[^>]*href\s*=\s*[\"\']\s*([^\"\'\s]+)\s*[\"\']", re.I)
    comments_pattern = re.compile("<!--.*?(?:-->|$)", re.DOTALL)


    def __init__(self, url, body=None, page=None, browser=None, request=None, *args, **kwargs):
        self._url = url
        self._body = body
        self._page = page
        self._browser = browser
        self._request = request
        self._cached_selector = None

    @property
    def body(self):
        return self._body

    text = body

    def json(self):
        try:
            data = json.load(self._body)
            return data
        except json.JSONDecodeError:
            return {}

    @property
    def raw(self):
        return self._body.encode("utf-8")

    def urljoin(self, url):
        text = self.comments_pattern.sub('', self.text)
        base = self.base_url_pattern.search(text)
        if base:
            return urljoin(url, base.group(1))
        return url

    @property
    def selector(self):
        from scrapyish.selector import Selector
        if self._cached_selector is None:
            self._cached_selector = Selector(self)
        return self._cached_selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)

    def css(self, query):
        return self.selector.css(query)

    @property
    def cb_kwargs(self):
        return self.request.cb_kwargs

    def _get_url(self):
        return self._url

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        if body is None:
            self._body = b''
        elif not isinstance(body, bytes):
            raise TypeError(
                "Response body must be bytes. "
                "If you want to pass unicode body use TextResponse "
                "or HtmlResponse.")
        else:
            self._body = body

    def __repr__(self):
        return f"<Resp {self.url}>"
