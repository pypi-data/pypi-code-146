#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""Convenience module for commonly used type-hints."""

from __future__ import annotations
# import sys as _sys

#: Export everything from `typing` module
from typing import *  # pylint: disable=unused-wildcard-import,unused-import,wildcard-import
import datetime

# from abc import abstractmethod as _abstractmethod
import dataclasses as _dc

import attr as _attr

# pylint: disable=unused-import

PY36 = (3, 6)
PY37 = (3, 7)
PY38 = (3, 8)
PY39 = (3, 9)


# if _sys.version_info >= PY39:
#     #: Import only non-deprecated members from `typing`
#     from typing import (
#         NewType, Generic, TypeVar, Any, NoReturn, Union, Optional, Literal, ClassVar,
#         Final, Annotated, AnyStr, Protocol, runtime_checkable, NamedTuple, NewType,
#         TypedDict, IO, TextIO, BinaryIO, Text, SupportsAbs, SupportsBytes,
#         SupportsFloat, SupportsIndex, SupportsInt, SupportsComplex, SupportsRound,
#         cast, overload, final, no_type_check, no_type_check_decorator,
#         get_type_hints, get_args, get_origin, ForwardRef, TypeAlias,
#         TYPE_CHECKING,
#     )
#
#     #: Import members from other packages that used to be in `typing`, alias as needed
#     from collections.abc import (
#         Callable, Set as AbstractSet, ByteString, Collection, Container,
#         ItemsView, KeysView, Mapping, MappingView, MutableMapping,
#         MutableSequence, MutableSet, Sequence, ValuesView, Iterable,
#         Iterator, Generator, Hashable, Sized, Coroutine, AsyncGenerator,
#         AsyncIterable, AsyncIterator, Awaitable,
#     )
#
#     from collections import (
#         defaultdict as DefaultDict, OrderedDict, ChainMap, Counter,
#         deque as Deque,
#     )
#
#     from re import Pattern, Match
#
#     from contextlib import (
#         AbstractAsyncContextManager as AsyncContextManager,
#         AbstractContextManager as ContextManager,
#     )
#
#     #: Create aliases for the types that used to be in `typing` but now implement
#     #  generic interfaces
#     Type = type
#     Dict = dict
#     List = list
#     Set = set
#     FrozenSet = frozenset
#     Tuple = tuple
# else:
#     from typing import *


#: Mapping with string keys, read-only (Immutable) operations
IMapStrAny = Mapping[str, Any]

#: Mapping with string keys, read-write (Mutable) operations
MMapStrAny = MutableMapping[str, Any]

#: Dictionary with string keys
DictStrAny = dict[str, Any]

#: Dictionary with string keys and boolean values
DictStrBool = dict[str, bool]

#: Optional string
OptStr = Optional[str]

#: Optional integer
OptInt = Optional[int]

#: Optional boolean
OptBool = Optional[bool]

#: Optional date
OptDate = Optional[datetime.date]

#: Optional datetime
OptDateTime = Optional[datetime.datetime]

#: Optional time
OptTime = Optional[datetime.time]

#: Optional timedelta (a.k.a. duration)
OptTimeDelta = Optional[datetime.timedelta]

#: Tuple of concrete types, used for bases in metaclasses
Bases = Tuple[type, ...]    # https://github.com/python/mypy/issues/10242

#: Signature of comparators in the `operator` lib
BoolBinOp = Callable[[Any, Any], bool]


# ## Dataclasses ## #

# pylint: disable=inherit-non-class, too-few-public-methods
class DataClassArgs(TypedDict, total=False):
    """Represents all the optional parameter options of a dataclass."""
    init: bool
    repr: bool
    eq: bool
    order: bool
    unsafe_hash: bool
    frozen: bool

@runtime_checkable
class DataClass(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol-ly way of identifying dataclasses (if needed for typehints).

    .. Note::
        For general testing whether a class or object is a dataclass use
        `dataclasses.is_dataclass` instead of `isinstance(o, DataClass)`.

        `assert isinstance(o, DataClass)` can be used to quell static checkers if you need to
        use the attributes defined here.
    """
    __dataclass_fields__: Dict[str, _dc.Field[Any]]
    __dataclass_params__: DataClassArgs  # Really _dc._DataclassParams

# ## attrs ## #

@runtime_checkable
class AttrsClass(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol-ly way of identifying attrs classes (if needed for typehints).

    .. Note::
        For general testing whether a class or object is an attrs use
        `attr.has` instead of `isinstance(o, DataClass)`.

        `assert isinstance(o, AttrsClass)` can be used to quell static checkers if you need to
        use the attributes defined here.
    """
    __attrs_attrs__: Dict[str, _attr.Attribute[Any]]


# ## Properties ## #

#: Property type type-variable for typed property
PropType = TypeVar('PropType')
OwnerType = TypeVar('OwnerType')

class Property(property, Generic[PropType]):
    """Generic implementation of the property class."""

    def __init__(self,
                 fget: Optional[Callable[[Any], PropType]] = None,
                 fset: Optional[Callable[[Any, PropType], None]] = None,
                 fdel: Optional[Callable[[Any], None]] = None,
                 doc: OptStr = None):
        super().__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)

    def __get__(self, obj: OwnerType, obj_type: Optional[type] = None) -> PropType:
        return cast(PropType, super().__get__(obj, obj_type))

    def __set__(self, obj: OwnerType, value: PropType) -> None:
        # pylint: disable=useless-super-delegation
        super().__set__(obj, value)

    def __delete__(self, obj: OwnerType) -> None:
        # pylint: disable=useless-super-delegation
        super().__delete__(obj)

    def getter(self, fget: Callable[[Any], PropType]) -> Property[PropType]:
        """Descriptor to change the getter on a property."""
        return cast(Property[PropType], super().getter(fget))

    def setter(self, fset: Callable[[Any, PropType], None]) -> Property[PropType]:
        """Descriptor to change the setter on a property."""
        return cast(Property[PropType], super().setter(fset))

    def deleter(self, fdel: Callable[[Any], None]) -> Property[PropType]:
        """Descriptor to change the deleter on a property."""
        return cast(Property[PropType], super().deleter(fdel))


#: String property
StrProperty = Property[str]

#: Integer property
IntProperty = Property[int]
