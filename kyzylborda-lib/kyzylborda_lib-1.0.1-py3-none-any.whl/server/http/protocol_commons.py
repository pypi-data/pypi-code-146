import copy
from email.message import Message
import urllib.parse

from ..tcp import Connection


__all__ = ("MalformedHeaderError", "ProtocolHeader")


class MalformedHeaderError(ValueError):
    pass


class ProtocolHeader:
    def __init__(self, raw_text: bytes):
        self._raw_text = raw_text

        self._headers = None
        self._original_headers = None

        self._modified_first_line = False


    def _format_first_line(self) -> bytes:
        raise NotImplementedError

    def _reset(self):
        raise NotImplementedError


    def _parse_headers(self) -> Message:
        message = Message()
        for line in self._raw_text.split(b"\n")[1:]:
            try:
                text = urllib.parse.unquote_to_bytes(line.strip(b"\r").decode()).decode()
            except UnicodeDecodeError:
                raise MalformedHeaderError("Header is not in UTF-8")
            if not text.strip():
                continue
            if ":" not in text:
                raise MalformedHeaderError("Header does not contain a colon")
            name, value = [part.strip() for part in text.split(":", 1)]
            message[name] = value
        return message


    @property
    def raw_text(self):
        if self._modified_first_line or self._headers != self._original_headers:
            raw_text = bytearray()

            if self._modified_first_line:
                raw_text += self._format_first_line()
            else:
                index = self._raw_text.find(b"\n")
                if index == -1:
                    raise MalformedHeaderError("Header is empty")
                raw_text += self._raw_text[:index + 1]

            if self._headers != self._original_headers:
                for name, value in self._headers.items():
                    raw_text += name.encode()
                    raw_text += b": "
                    raw_text += value.encode()
                    raw_text += b"\r\n"
                raw_text += b"\r\n"
            else:
                index = self._raw_text.find(b"\n")
                raw_text += self._raw_text[index + 1:]

            self._raw_text = bytes(raw_text)
            self._modified_first_line = False
            self._original_headers = copy.copy(self._headers)

        return self._raw_text


    @raw_text.setter
    def raw_text(self, value: bytes):
        self._reset_first_line()
        self._headers = None
        self._original_headers = None
        self._raw_text = value
        self._modified_first_line = False


    @property
    def headers(self) -> Message:
        if self._headers is None:
            self._original_headers = self._parse_headers()
            self._headers = copy.copy(self._original_headers)
        return self._headers

    @headers.setter
    def headers(self, value: Message):
        self._headers = value


    def __copy__(self):
        header = type(self)(self._raw_text)
        header._headers = self._headers
        header._original_headers = self._original_headers
        header._modified_first_line = self._modified_first_line
        return header
