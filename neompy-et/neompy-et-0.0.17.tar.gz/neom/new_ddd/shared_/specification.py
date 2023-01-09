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

"""Specification interface module."""


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

__all__ = ("Specification",)

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """Specification interface.
    AbstractSpecification is the base for creating specifications and only
    the method ``IsSatisfiedBy(object)`` must be implemented.
    """

    @abstractmethod
    def IsSatisfiedBy(self, t: T) -> bool:
        """Check if ``t`` is satisfied by the specification."""

    @abstractmethod
    def And(self, specification: Specification[T]) -> Specification[T]:
        """New specification that is AND operation of ``self`` specification
        and another specification."""

    @abstractmethod
    def Or(self, specification: Specification[T]) -> Specification[T]:
        """New specification that is OR operation of ``self`` specification
        and another specification."""

    @abstractmethod
    def Not(self, specification: Specification[T]) -> Specification[T]:
        """New specification that is NOT operation of ``self`` specification."""
