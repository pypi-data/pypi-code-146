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

"""Stuff definitions for enitty and stuffs designing."""

from __future__ import annotations

import builtins
from abc import ABC, ABCMeta
from sys import modules
from types import FunctionType
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    NamedTuple,
    Tuple,
    Type,
    TypeVar,
    get_type_hints,
)

from .exceptions import BadMemberError

__all__ = ("Field",)

T = TypeVar("T")


class KindnameError(BadMemberError):
    """Raised when a member definition for a kindname can not be found. May also
    be raised when the kind is not a string."""


class _MetaStuff(ABCMeta):
    """Metaclass for Stuff

    To state members with the names needed. For example,

    .. code-block: python
      class Publication(Stuff):
        count: int

    ``Publication.count`` needs to know the name ``count`` defined.
    """

    def __init__(cls, name: str, bases: Tuple[str], namespace: Dict[str, Any]):
        super(_MetaStuff, cls).__init__(name, bases, namespace)
        cls._StateMembers()

    def __repr__(cls):
        fields = [f"{f.name}={f!r}" for _, f in sorted(cls._fields.items())]
        return f'{cls.__name__}<{", ".join(fields)}>'


class Stuff(ABC, metaclass=_MetaStuff):
    """A class describing domain stuffs.

    All stuff classes inheriting from :class:`Stuff` automatically have
    :class:`_MetaStuff` as their metaclass, so that members are stated
    properly after class definition."""

    __slots__ = ()

    _fields = {}
    _kinds = {}

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        fields = [f"{f.name}={f!r}" for _, f in sorted(self._fields.items())]
        return f'{self._kindname()}<{", ".join(fields)}>'

    def ReflectionEquals(self, other: Stuff) -> bool:
        """Compare two stuff by fields."""
        if len(self._fields) != len(other._fields):
            return False
        return not any(
            name not in other._fields
            or field != other._fields[name]
            or getattr(self, name) != getattr(other, name)
            for name, field in self._fields.items()
        )

    @classmethod
    def _kindname(cls):
        """Return the kind name for this class.

        Defaults to ``cls.__name__``; users may override this to return a
        different name when stored than the name of the class.
        """
        return cls.__name__

    @classmethod
    def _StateMembers(cls):
        """State member calling their ``_FixState()`` method.

        .. note::

          Called by :class:`_MetaStuff`, but may also be called
          manually after dynamically updating a stuff class.

        Raises:
          KindnameError: When returned kind name from ``_kindname()`` is not a
            :class:`str`.
        """
        kindname = cls._kindname()
        if not isinstance(kindname, str):
            raise KindnameError(
                f"Class {cls.__name__} defines a ``_kindname()`` method that"
                f" returns a non-string ({kindname!r})"
            )

        typeHints = get_type_hints(cls)
        if typeHints:
            cls._fields = {}
            cls._kinds = {}

            for name, field in typeHints.items():
                # TODO: back compatibility - remove after migration
                if not isinstance(field, Field):
                    field = Field[field]
                field._FixState(cls, name)  # pylint:disable=protected-access
                cls._fields[name] = field
            cls._UpdateKinds()

            if (
                hasattr(cls, "Meta")
                and hasattr(cls.Meta, "__init__")
                and isinstance(cls.Meta.__init__, bool)
                and cls.Meta.__init__
            ):
                _StateNewAttribute(
                    cls,
                    "__init__",
                    _InitFn(
                        cls._fields.values(),
                        "self",
                        modules[cls.__module__].__dict__
                        if cls.__module__ in modules
                        else {},
                    ),
                )

    @classmethod
    def _UpdateKinds(cls: Type[Stuff]):
        """Update kinds dict to include this class."""
        cls._kinds[cls._kindname()] = cls


def _InitFn(
    fields: List[Field], selfname: str, globalns: Dict[str, Type[object]]
):
    """Init Function."""
    localns = {f"_type_{f.name}": f.kind for f in fields}
    lines = [f"{selfname}.{f.name}={f.name}" for f in fields]
    params = [f"{f.name}:{f.kind.__name__}" for f in fields]

    return _NewFn(
        "__init__",
        [selfname] + params,
        lines,
        localns=localns,
        globalns=globalns,
        return_type=bool,
    )


def _StateNewAttribute(
    cls: Type[object], name: str, value: Callable[..., None]
):
    """Never overwrites an existing member."""
    if name in cls.__dict__:
        raise ValueError(f"{cls}: has attribute name={name} with value={value}")
    _StateQualname(cls, value)
    setattr(cls, name, value)


def _StateQualname(cls, value):
    """_NewFn uses proper __qualname__."""
    if isinstance(value, FunctionType):
        value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    return value


def _NewFn(
    name: str,
    args: List[str],
    body: List[str],
    *,
    globalns: Dict[str, Type[object]] = None,
    localns: Dict[str, Type[object]] = None,
    return_type: Type[object] = None,
):
    """Create new function. localns mutates on exec()."""
    if localns is None:
        localns = {}
    if "BUILTINS" not in localns:
        localns["BUILTINS"] = builtins
    return_annotation = ""
    if return_type:
        localns["_return_type"] = return_type
        return_annotation = "->_return_type"
    args = ",".join(args)
    body = "\n".join(f"  {b}" for b in body)
    txt = f" def {name}({args}){return_annotation}:\n{body}"
    localvars = ", ".join(localns.keys())
    txt = f"def __new_fn__({localvars}):\n{txt}\n return {name}"
    ns = {}
    exec(txt, globalns, ns)  # pylint:disable=exec-used
    return ns["__new_fn__"](**localns)


class Field(Generic[T]):
    """A class describing a persisted kind member."""

    __slots__ = ("kind", "validator", "pkind", "name")

    def __init__(self, kind: Type[T], validator: Callable[[T], None] = None):
        self.kind = kind
        self.validator = validator
        self.name = None
        self.pkind = None

    def __repr__(self):
        return (
            f"Field[{self.kind} name={self.name},"
            f" pkind={self.pkind._kindname()}]"
        )

    def __call__(self, *args, **kwds):
        raise TypeError(f"Cannot instantiate {self!r}")

    def __eq__(self, other: Field) -> bool:
        return (
            other
            and isinstance(other, Field)
            and self.kind is other.kind
            and self.name == other.name
        )

    def _FixState(self, pkind: Type[T], name: str):
        """Helper called to tell member its name."""
        self.pkind = pkind
        self.name = name

    def __class_getitem__(
        cls, item: T | Tuple[Type[T], Callable[[T], None] | Arg]
    ):
        return cls(*item) if isinstance(item, Arg) else cls(item)


class Arg(NamedTuple):
    """To describe Field definition."""

    kind: Type[T]
    validator: Callable[[T], None] = None
