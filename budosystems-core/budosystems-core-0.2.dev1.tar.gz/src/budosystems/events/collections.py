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
"""Support collections for models."""

from typing import TypeVar, Hashable, Iterable, Iterator, Generic, overload
from enum import Enum, auto
from collections.abc import MutableSet, MutableMapping, MutableSequence

import attr

from . import MESSAGE_BUS
from .base import Event, FieldType, Timing

_T = TypeVar("_T", bound=Hashable)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class Op(Enum):
    """Collection operation markers used in collection related events."""
    Add = auto()
    Mod = auto()
    Del = auto()
    Get = auto()


@attr.s(auto_attribs=True, kw_only=True)
class SetModifiedEvent(Generic[FieldType], Event):
    """Provides information to any observers about a `set` which is having its contents modified
    on an object they are watching."""
    instance: object
    property_name: str
    value: FieldType
    op: Op
    timing: Timing


@attr.s(auto_attribs=True, kw_only=True)
class MappingModifiedEvent(Generic[_KT, _VT], Event):
    """Provides information to any observers about a `mapping` which is having its contents modified
    on an object they are watching."""
    instance: object
    property_name: str
    key: _KT
    value: _VT
    op: Op
    timing: Timing


class SignallingSet(MutableSet[_T]):
    """An implementation of `set` which signals the `MessageBus`."""
    _owner: object
    _prop_name: str
    _data: set[_T]

    def __init__(self, *args: _T, owner: object, prop_name: str):
        self._owner = owner
        self._prop_name = prop_name
        self._data = set(args)

    def add(self, value: _T) -> None:
        """Adds `value` to this set, and signals `SetModifiedEvent` before and after the
        insertion."""
        op = Op.Add if value not in self._data else Op.Mod
        ev = SetModifiedEvent(
                instance=self._owner,
                property_name=self._prop_name,
                value=value,
                op=op,
                timing=Timing.Before
        )
        MESSAGE_BUS.signal(ev)

        self._data.add(value)

        ev = attr.evolve(ev, timing=Timing.After)
        MESSAGE_BUS.signal(ev)

    def discard(self, value: _T) -> None:
        """Removes `value` to this set, and signals `SetModifiedEvent` before and after the
        insertion."""
        ev = SetModifiedEvent(
                instance=self._owner,
                property_name=self._prop_name,
                value=value,
                op=Op.Del,
                timing=Timing.Before
        )
        MESSAGE_BUS.signal(ev)

        self._data.discard(value)

        ev = attr.evolve(ev, timing=Timing.After)
        MESSAGE_BUS.signal(ev)

    def __contains__(self, x: object) -> bool:
        return x in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._data)


class SignallingMapping(MutableMapping[_KT, _VT]):
    """An implementation of `dict` which signals the `MessageBus`."""
    _owner: object
    _prop_name: str
    _data: dict[_KT, _VT]

    def __setitem__(self, k: _KT, v: _VT) -> None:
        op = Op.Add if k not in self._data else Op.Mod
        ev = MappingModifiedEvent(
                instance=self._owner,
                property_name=self._prop_name,
                key=k,
                value=v,
                op=op,
                timing=Timing.Before
        )
        MESSAGE_BUS.signal(ev)

        self._data[k] = v

        ev = attr.evolve(ev, timing=Timing.After)
        MESSAGE_BUS.signal(ev)

    def __delitem__(self, k: _KT) -> None:
        value = self._data[k]
        ev = MappingModifiedEvent(
                instance=self._owner,
                property_name=self._prop_name,
                key=k,
                value=value,
                op=Op.Del,
                timing=Timing.Before
        )

        del self._data[k]

        ev = attr.evolve(ev, timing=Timing.After)
        MESSAGE_BUS.signal(ev)

    def __getitem__(self, k: _KT) -> _VT:
        # Signal type Get, before?
        value = self._data[k]
        # Signal type Get, after?
        return value

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[_KT]:
        return iter(self._data)


class SignallingSequence(MutableSequence[_T]):
    """An implementation of `list` which signals the `MessageBus`."""

    _owner: object
    _prop_name: str
    _data: list[_T]

    def insert(self, index: int, value: _T) -> None:
        pass

    @overload
    def __getitem__(self, i: int) -> _T: ...

    @overload
    def __getitem__(self, i: slice) -> MutableSequence[_T]: ...

    def __getitem__(self, i):  # type: ignore
        pass

    @overload
    def __setitem__(self, i: int, o: _T) -> None: ...

    @overload
    def __setitem__(self, i: slice, o: Iterable[_T]) -> None: ...

    def __setitem__(self, i, o):  # type: ignore
        pass

    @overload
    def __delitem__(self, i: int) -> None: ...

    @overload
    def __delitem__(self, i: slice) -> None: ...

    def __delitem__(self, i):  # type: ignore
        pass

    def __len__(self) -> int:
        return len(self._data)
