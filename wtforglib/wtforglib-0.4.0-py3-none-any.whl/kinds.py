"""Top-level module kinds for wtforglib.

The kinds module supports defintions of types used in
the wtforglib package and used in various projects
the author provides.

Types
-----
KeyType
    Genery mapping key type
ValueType
    Generic mapping value type
Fspec
    Fspec = Union[str, PathLike[str]]
StrAnyDict
    StrAnyDict = Dict[str, Any]
"""

import sys
from os import PathLike
from typing import Any, Dict, TypeVar, Union

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


if sys.version_info >= (3, 9):
    Fspec = Union[str, PathLike[str]]
else:
    Fspec = Union[str, "PathLike[str]"]

StrAnyDict = Dict[str, Any]  # type: ignore
