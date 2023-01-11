# pylint: disable=W0401,W0614
# copyright 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""exceptions used in the core of the CubicWeb web application"""

import http.client as http_client

from cubicweb import CubicWebException, Unauthorized  # noqa # backward compatibility
from cubicweb.to_refactor._exceptions import (  # noqa # backward compatibility
    PublishException,
    Redirect,
    LogOut,
    RemoteCallFailed,
    RequestError,
    NotFound,
)


class DirectResponse(Exception):
    """Used to supply a twitted HTTP Response directly"""

    def __init__(self, response):
        self.response = response


class InvalidSession(CubicWebException):
    """raised when a session id is found but associated session is not found or
    invalid"""


# Publish related exception


class StatusResponse(PublishException):
    def __init__(self, status, content=""):
        super().__init__(status=status)
        self.content = content

    def __repr__(self):
        return f"{self.__class__.__name__}({self.status!r}, {self.content!r})"


# Publish related error


class NothingToEdit(RequestError):
    """raised when an edit request doesn't specify any eid to edit"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("status", http_client.BAD_REQUEST)
        super().__init__(*args, **kwargs)


class ProcessFormError(RequestError):
    """raised when posted data can't be processed by the corresponding field"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("status", http_client.BAD_REQUEST)
        super().__init__(*args, **kwargs)
