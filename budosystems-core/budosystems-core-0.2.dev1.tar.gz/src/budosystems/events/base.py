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

"""Core events."""
from __future__ import annotations
from typing import TypeVar, Generic
from enum import Enum, auto

import attr

@attr.s
class Event:
    """Base event class."""


class Timing(Enum):
    """Timing markers used in events where it's import to track whether it's
    signalled before or after the operation happened."""
    Before = auto()
    After = auto()


FieldType = TypeVar('FieldType')
"""Type variable for fields reported by `FieldModifiedEvent`."""

@attr.s(auto_attribs=True, kw_only=True)
class FieldModifiedEvent(Generic[FieldType], Event):
    """Provides information to any observers about a field that has been modified on an
    object they are watching."""
    instance: object
    field_name: str
    old_value: FieldType
    new_value: FieldType
    timing: Timing
