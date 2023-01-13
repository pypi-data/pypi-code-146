from __future__ import annotations

from dataclasses import dataclass
from email.message import Message
from http.client import responses
from typing import Optional
import magic
import urllib.parse

from .protocol_commons import MalformedHeaderError, ProtocolHeader
from ..tcp import Connection


__all__ = ("ResponseHeader", "Response", "respond")


class ResponseHeader(ProtocolHeader):
    def __init__(self, raw_text: bytes):
        super().__init__(raw_text)
        self._status_code: Optional[int] = None
        self._status_text: Optional[str] = None


    def _format_first_line(self) -> bytes:
        return f"HTTP/1.1 {self._status_code} {self._status_text}\r\n".encode()


    def _reset_first_line(self):
        self._status_code = None
        self._status_text = None


    def _parse_first_line(self) -> list[str]:
        index = self._raw_text.find(b"\n")
        if index == 0:
            raise MalformedHeaderError("Header is empty")
        try:
            parts = self._raw_text[:index].decode().split(None, 2)
        except UnicodeDecodeError:
            raise MalformedHeaderError("First line is not in UTF-8")
        if len(parts) < 1 or parts[0] not in ("HTTP/1.0", "HTTP/1.1"):
            raise MalformedHeaderError("First line does not start with HTTP/1.0 or HTTP/1.1")
        return parts


    def _parse_status_code(self) -> int:
        info = self._parse_first_line()
        if len(info) < 2:
            raise MalformedHeaderError("Status code not present")
        if len(info[1]) > 3:
            raise MalformedHeaderError("Invalid status code")
        try:
            return int(info[1])
        except ValueError:
            raise MalformedHeaderError("Invalid status code")


    def _parse_status_text(self) -> str:
        info = self._parse_first_line()
        if len(info) < 3:
            raise MalformedHeaderError("Status text not present")
        return info[2]


    @property
    def status_code(self) -> int:
        if self._status_code is None:
            self._status_code = self._parse_status_code()
        return self._status_code

    @status_code.setter
    def status_code(self, value: int):
        self._status_code = value
        self._modified_first_line = True


    @property
    def status_text(self) -> str:
        if self._status_text is None:
            self._status_text = self._parse_status_text()
        return self._status_text

    @status_text.setter
    def status_text(self, value: str):
        self._status_text = value
        self._modified_first_line = True


    def __copy__(self):
        header = super().__copy__()
        header._status_code = self._status_code
        header._status_text = self._status_text
        return header


@dataclass
class Response:
    header: ResponseHeader
    data: Connection | bytes

    @property
    def raw_header(self) -> bytes:
        return self.header.raw_text
    @raw_header.setter
    def raw_header(self, value: bytes):
        self.header.raw_text = value

    @property
    def status_code(self) -> int:
        return self.header.status_code
    @status_code.setter
    def status_code(self, value: int):
        self.header.status_code = value

    @property
    def status_text(self) -> str:
        return self.header.status_text
    @status_text.setter
    def status_text(self, value: str):
        self.header.status_text = value

    @property
    def headers(self) -> Message:
        return self.header.headers
    @headers.setter
    def headers(self, value: Message):
        self.header.headers = value


def respond(status_code: int, data: Optional[bytes]=None, *, status_text: Optional[str]=None, content_type: str=None, headers: Message | dict[str, str | list[str]]={}) -> Response:
    if status_text is None:
        status_text = responses.get(status_code, "Unknown")

    resp_header = ResponseHeader(f"HTTP/1.1 {status_code} {status_text}\r\n\r\n".encode())

    if data is None:
        if status_code < 300:
            raise ValueError(f"Cannot generate an error page for non-error status code {status_code}")
        if content_type in (None, "text/html"):
            content_type = "text/html"
            data = f"""<!DOCTYPE html>
<html>
    <head>
        <title>{status_code} {status_text}</title>
    </head>
    <body>
        <center>
            <h1>{status_code} {status_text}</h1>
            <hr>
            kyzylborda_lib.server
        </center>
    </body>
</html>
""".encode()
        elif content_type == "text/plain":
            data = f"{status_code} {status_text}".encode()
        else:
            raise ValueError(f"Cannot generate an error page for content type {content_type}")

    if isinstance(headers, dict):
        new_headers = Message()
        for name, values in headers.items():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                new_headers[name] = value
    else:
        new_headers = headers

    if "Content-Type" not in new_headers:
        if content_type is None:
            content_type = magic.from_buffer(data)
        new_headers["Content-Type"] = content_type

    if "Connection" not in new_headers:
        new_headers["Connection"] = "close"

    resp_header.headers = new_headers

    return Response(resp_header, data)
