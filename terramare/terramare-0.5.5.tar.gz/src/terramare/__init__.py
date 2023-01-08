"""Automatically construct complex objects from simple Python types."""

from .classes import (
    ARRAY,
    OBJECT,
    VALUE,
    auto,
    disallow_unknown_fields,
    handle_exception_types,
)
from .data import Context
from .errors import ConstructorError, FactoryError, TerramareError
from .metadata import METADATA_KEY, fields, from_context, skip, with_
from .tagged_constructors import externally_tagged, internally_tagged
from .terramare import structure

# Expose the package version as __version__ (see PEP 396).
__version__ = "0.5.5"

__all__ = [
    "ARRAY",
    "METADATA_KEY",
    "OBJECT",
    "VALUE",
    "ConstructorError",
    "Context",
    "FactoryError",
    "TerramareError",
    "auto",
    "disallow_unknown_fields",
    "externally_tagged",
    "fields",
    "from_context",
    "handle_exception_types",
    "internally_tagged",
    "skip",
    "structure",
    "with_",
]
