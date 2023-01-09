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

"""This module is under construction.
It's used to mark the domain role for classes and models defined in the domain.
"""

from __future__ import annotations

from typing import Type, TypeVar

from .entity import Entity
from .identity import Identity

__all__ = ("EntitySupport",)

T = TypeVar("T")
ID = TypeVar("ID", bound=Identity)


class EntitySupport(Entity[T, ID]):
    """EntitySupport."""

    __slots__ = ()

    _identityField = None

    def Identity(self) -> ID:
        if not self._identityField:
            self._identityField = self._LazyIdentityDetermination()
        return getattr(self, self._identityField.name)

    def SameIdentityAs(self, other: T) -> bool:
        return other and self.Identity() == other.Identity()

    def __eq__(self, other: T) -> bool:
        return (self is other) or (
            other
            and isinstance(other, type(self))
            and self.SameIdentityAs(other)
        )

    def __hash__(self) -> int:
        return hash(self.Identity())

    def _LazyIdentityDetermination(self) -> Type[ID]:
        identityField = None
        for field in self._fields.values():
            if isinstance(field, Identity):
                if identityField:
                    raise TypeError("Only one field can be an identity")
                identityField = field
        if not identityField:
            raise TypeError("Must have a unique identity field")
        return identityField
