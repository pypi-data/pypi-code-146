from __future__ import annotations

from dataclasses import dataclass
from email.message import Message
from typing import Optional
import urllib.parse

from .protocol_commons import MalformedHeaderError, ProtocolHeader
from ..tcp import Connection


__all__ = ("RequestHeader", "Request", "SUPPORTED_METHODS")


SUPPORTED_METHODS = ["GET", "POST", "PATCH", "PUT", "DELETE", "TRACE", "CONNECT", "HEAD"]


class RequestHeader(ProtocolHeader):
    def __init__(self, raw_text: bytes):
        super().__init__(raw_text)
        self._method: Optional[str] = None
        self._path: Optional[str] = None


    def _format_first_line(self) -> bytes:
        assert self._path is not None
        return f"{self._method} {urllib.parse.quote(self._path)} HTTP/1.1\r\n".encode()


    def _reset_first_line(self):
        self._method = None
        self._path = None


    def _parse_first_line(self) -> list[str]:
        index = self._raw_text.find(b"\n")
        if index == 0:
            raise MalformedHeaderError("Header is empty")
        try:
            return self._raw_text[:index].decode().split()
        except UnicodeDecodeError:
            raise MalformedHeaderError("First line is not in UTF-8")


    def _parse_method(self) -> str:
        info = self._parse_first_line()
        if len(info) < 1:
            raise MalformedHeaderError("Method not present")
        method = info[0]
        if method.upper() not in SUPPORTED_METHODS:
            raise MalformedHeaderError("Unsupported method")
        return method.upper()


    def _parse_path(self) -> str:
        info = self._parse_first_line()
        if len(info) < 2:
            raise MalformedHeaderError("Path not present")
        try:
            return urllib.parse.unquote_to_bytes(info[1]).decode()
        except UnicodeDecodeError:
            raise MalformedHeaderError("Path is not in UTF-8")


    @property
    def method(self) -> str:
        if self._method is None:
            self._method = self._parse_method()
        return self._method

    @method.setter
    def method(self, value: str):
        self._method = value
        self._modified_first_line = True


    @property
    def path(self) -> str:
        if self._path is None:
            self._path = self._parse_path()
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value
        self._modified_first_line = True


    def __copy__(self):
        header = super().__copy__()
        header._method = self._method
        header._path = self._path
        return header


@dataclass
class Request:
    header: RequestHeader
    data: Connection | bytes

    @property
    def raw_header(self) -> bytes:
        return self.header.raw_text
    @raw_header.setter
    def raw_header(self, value: bytes):
        self.header.raw_text = value

    @property
    def method(self) -> str:
        return self.header.method
    @method.setter
    def method(self, value: str):
        self.header.method = value

    @property
    def path(self) -> str:
        return self.header.path
    @path.setter
    def path(self, value: str):
        self.header.path = value

    @property
    def headers(self) -> Message:
        return self.header.headers
    @headers.setter
    def headers(self, value: Message):
        self.header.headers = value
