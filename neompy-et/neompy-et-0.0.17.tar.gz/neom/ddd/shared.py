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

import contextlib
from abc import ABCMeta, abstractmethod
from functools import lru_cache, wraps
from sys import version_info
from types import CodeType, FunctionType
from typing import (
    Callable,
    Generic,
    NoReturn,
    Type,
    TypeVar,
    _GenericAlias,
    _SpecialForm,
    cast,
    get_type_hints,
)


class Stuff:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


T = TypeVar("T")
ID = TypeVar("ID")
ORD = -3

# TODO: remove after move new_ddd support
if version_info.minor > 9:
    ORD -= 1


class MetaEntity(ABCMeta):
    def __init__(cls, cname, bases, namespace):
        if "__annotations__" in namespace:
            initlines = ["def __init__(self"]
            initbody = []
            slots = []
            idname = None
            for name, kind in get_type_hints(cls).items():
                if isinstance(kind, _GenericAlias):
                    kind = cast(_GenericAlias, kind).__origin__
                initlines.append(f", {name}: {kind.__name__}")
                initbody.append(f"\n  self.{name} = {name}")
                slots.append(name)
                if isinstance(kind, IdentityAlias):
                    idname = name
            initlines.append('):\n  """Entity init"""')
            initlines.extend(initbody)
            initlines.append("\n  self.Validate()")
            initcode = compile("".join(initlines), "<ddd.shared>", "exec")
            initfunc = FunctionType(
                InitCodeType(initcode.co_consts[ORD]),
                globals(),
                "__init__",
                None,
                cls.__init__.__closure__,
            )
            super().__init__(cname, bases, namespace)
            cls.__init__ = initfunc
            cls.__slots__ = tuple(slots)
            if idname:
                annotations = cls.identity.__annotations__
                cls.identity = FunctionType(
                    compile(
                        f"def identity(self) -> ID: return self.{idname}\n",
                        "<ddd.shared>",
                        "single",
                    ).co_consts[ORD],
                    globals(),
                )
                cls.identity.__annotations__ = annotations
            else:
                cls.identity = MetaEntity.identity(cls)

    @staticmethod
    def identity(cls) -> Callable[[], ID]:
        def wrapper(_) -> NoReturn:
            raise NoIdentityError(cls)

        return wrapper

    def __repr__(cls):
        items = cls.__annotations__.items()
        props = ("{}={!r}".format(name, prop) for name, prop in items)
        return "{}<{}>".format(cls.__name__, ", ".join(props))


def InitCodeType(c):
    return CodeType(
        c.co_argcount,
        c.co_posonlyargcount,
        c.co_kwonlyargcount,
        c.co_nlocals,
        c.co_stacksize,
        c.co_flags,
        c.co_code,
        c.co_consts,
        c.co_names,
        c.co_varnames,
        c.co_filename,
        c.co_name,
        c.co_firstlineno,
        c.co_lnotab,
        c.co_freevars + ("__class__",),
        c.co_cellvars,
    )


class Entity(Generic[T, ID], metaclass=MetaEntity):
    """TODO: Domain model entity."""

    def __init__(self):
        super().__init__()

    def Validate(self):
        """Execute domain member validations."""

    def identity(self) -> ID:
        return NotImplemented

    def SameIdentityAs(other: T) -> bool:
        return NotImplemented

    def __repr__(self):
        vals = (
            "{}={!r}".format(m, getattr(self, m)) for m in self.__annotations__
        )
        return "{}<{}>".format(self.__class__.__name__, ", ".join(vals))

    @classmethod
    def Make(cls, **kwargs) -> Entity:
        entity = cls.__new__(cls)
        for key, value in kwargs.items():
            setattr(entity, key, value)
        return entity


class EntitySupport:
    def __eq__(self, other: Entity):
        return all(
            getattr(self, name) == getattr(other, name)
            for name in self.__slots__
        )

    def __hash__(self):
        return hash(self.identity())


class MetaValueObject(ABCMeta):
    def __init__(cls, cname, bases, namespace):
        if "__annotations__" in namespace:
            initlines = ["def __init__(self"]
            initbody = []
            slots = []
            for name, kind in get_type_hints(cls).items():
                if isinstance(kind, _GenericAlias):
                    kind = cast(_GenericAlias, kind).__origin__
                if isinstance(kind, _SpecialForm):
                    initlines.append(f", {name}: {kind}")
                else:
                    initlines.append(f", {name}: {kind.__name__}")
                initbody.append(f"\n  self.{name} = {name}")
                slots.append(name)
                if isinstance(kind, IdentityAlias):
                    raise TypeError("Use Identity in ValueObject es invalid")
            initlines.append("):")
            initlines.extend(initbody)
            initlines.append("\n  self.Validate()")
            initcode = compile("".join(initlines), "<ddd.shared>", "exec")
            initfunc = FunctionType(
                InitCodeType(initcode.co_consts[ORD]),
                globals(),
                "__init__",
                None,
                cls.__init__.__closure__,
            )
            super().__init__(cname, bases, namespace)
            cls.__init__ = initfunc
            cls.__slots__ = tuple(slots)

    def __repr__(cls):
        items = cls.__annotations__.items()
        props = ("{}={!r}".format(name, prop) for name, prop in items)
        return "{}<{}>".format(cls.__name__, ", ".join(props))


class ValueObject(metaclass=MetaValueObject):
    """TODO: Domain model value object."""

    def __init__(self):
        super().__init__()

    def Validate(self):
        """Execute domain member validations."""

    def __eq__(self, other: ValueObject) -> bool:
        return all(
            getattr(self, name) == getattr(other, name)
            for name in self.__slots__
        )

    def __repr__(self):
        vals = (
            "{}={!r}".format(m, getattr(self, m)) for m in self.__annotations__
        )
        return "{}<{}>".format(self.__class__.__name__, ", ".join(vals))

    @classmethod
    def Make(cls, **kwargs) -> ValueObject:
        valueObject = cls.__new__(cls)
        for key, value in kwargs.items():
            setattr(valueObject, key, value)
        return valueObject


def _idcache(fn=None, /, *, typed=False):
    def wrapper(fn):
        cached = lru_cache(typed=typed)(fn)
        _idcache.clears.append(cached.cache_clear)

        @wraps(fn)
        def inner(*args, **kwds):
            with contextlib.suppress(TypeError):
                return cached(*args, **kwds)
            return fn(*args, **kwds)

        return inner

    if fn is not None:
        return wrapper(fn)
    return wrapper


_idcache.clears = []


class Final:
    __slots__ = ("__weakref__",)

    def __init_subclass__(self, /, *_, **ks):
        if "_root" not in ks:
            raise TypeError("Cannot subclass")


class Immutable:
    __slots__ = ()

    def __copy__(self):
        return self

    def __deepcopy__(self, _):
        return self


class Identity(Immutable):
    """TODO: Domain model annotation for identity."""

    @_idcache
    def __class_getitem__(cls, member: Type[object]):
        return IdentityAlias(member)


class IdentityAlias(Final, Immutable, _root=True):
    __slots__ = ("_kind", "__name__")

    def __init__(self, kind: Type[object]):
        self._kind = kind
        self.__name__ = kind.__name__

    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    def __subclasscheck__(self, cls):
        return cls == self._kind

    def __mro_entries__(self, bases):
        raise TypeError(f"Cannot subclass {self!r}")

    def __repr__(self):
        return f"{self._kind}"

    def __reduce__(self):
        return self._name

    def __call__(self, *args, **kwds):
        raise TypeError(f"Cannot instantiate {self!r}")


class Service(Stuff):
    """TODO: Domain service declaration."""


class Repository(Stuff):
    """TODO: Domain model entity repository."""


class Action:
    """TODO: Domain model action service."""

    @abstractmethod
    def Apply(self):
        raise NotImplementedError


class QuerySet:
    """TODO: Domain model query set application."""


class Error(Exception):
    """DDD Errors"""


class DomainError(Error):
    """Entities, repositories and services base error for user cases.
    This exceptions does not break the workflow."""


class NoIdentityError(DomainError):
    """Notify the use"""

    def __init__(self, cls):
        self._cls = cls

    def __str__(self):
        return f"{self._cls.__qualname__} without identity"


class RepositoryError(DomainError):
    """Find, Store, Delete, Remove errors"""


class ServiceError(DomainError):
    pass


class NotFoundError(RepositoryError):
    """Raised when Repository.Find doest not foun.
    Connection and transaction errors not included.
    """
