"""
Waifu.im API Wrapper for Python 3.10+

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

from .client import Client
from .exceptions import WaifuImExcpetion, HTTPException, NotFound, Forbidden, Unauthorized
from .models import ImageResponseData, Tag, Image, Tags, Order, Orientation
from .utils import generate_authorization_link, generate_deauthorization_link


__version__ = "1.0.3"

__all__ = (
    "Client",
    "WaifuImExcpetion",
    "HTTPException",
    "NotFound",
    "Forbidden",
    "Unauthorized",
    "ImageResponseData",
    "Tag",
    "Image",
    "Tags",
    "Order",
    "Orientation",
    "generate_authorization_link",
    "generate_deauthorization_link",
)
