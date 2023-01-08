"""
MIT License

Copyright (c) 2023 Avimetry Development

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class WaifuImExcpetion(Exception):
    """
    Base exception for waifuim. All other exceptions inherit from this.
    """


class HTTPException(WaifuImExcpetion):
    """
    Exception for HTTP Exceptions.
    """

    def __init__(self, response: ClientResponse, data: dict[str, Any] | str):
        self.response = response
        self.code = response.status
        if isinstance(data, dict):
            self.message = data.get("detail", "")

        super().__init__(f"{self.code}: {self.message}")


class NotFound(HTTPException):
    """
    Raised when a 404 error is encountered.
    """


class Forbidden(HTTPException):
    """
    Raised when a 403 error is encountered.
    """


class Unauthorized(HTTPException):
    """
    Raised when a 401 error is encountered.
    """


class InvalidArgument(WaifuImExcpetion):
    """
    Raised when an invalid argument is passed.
    """

    def __init__(self, argument: Any, message: str):
        self.message = message
        self.argument = argument
        super().__init__(message)
