# Copyright 2022 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Temporary module to put domain related classes."""


class Service:  # pylint:disable=too-few-public-methods
    """TODO: Domain service declaration."""


class Repository:  # pylint:disable=too-few-public-methods
    """TODO: Domain model entity repository."""


class QuerySet:  # pylint:disable=too-few-public-methods
    """TODO: Domain model query set application."""


class Error(Exception):
    """DDD Errors"""


class DomainError(Error):
    """Entities, repositories and services base error for user cases.
    This exceptions does not break the workflow."""


class NoIdentityError(DomainError):
    """Notify the use"""

    def __init__(self, cls):
        super().__init__(cls)
        self._cls = cls

    def __str__(self):
        return f"{self._cls.__qualname__} without identity"


class RepositoryError(DomainError):
    """Find, Store, Delete, Remove errors"""


class ServiceError(DomainError):
    """Service logic error."""


class NotFoundError(RepositoryError):
    """Raised when Repository.Find doest not foun.
    Connection and transaction errors not included.
    """
