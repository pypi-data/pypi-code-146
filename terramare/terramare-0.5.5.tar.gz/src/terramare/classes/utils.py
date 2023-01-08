"""Internal utilities for class deserialization."""

import logging
from dataclasses import InitVar, dataclass
from typing import Any, List, Sequence, Union

import terramare.metadata
from terramare.errors import InternalError

from .. import type_utils
from ..core import InternalConstructor, InternalFactory
from ..data import Context
from ..metadata import MetadataCollection
from ..types import Target

_log = logging.getLogger(__name__)


class _PseudoField:
    pass


@dataclass(frozen=True)
class SingleField:
    constructor: InternalConstructor[Any]
    required: bool


@dataclass(frozen=True)
class ContextField(_PseudoField):
    pass


NO_DEFAULT = object()


@dataclass(frozen=True)
class FromContextField(_PseudoField):
    key: str
    type_: Target[Any]
    _default: object

    @property
    def required(self) -> bool:
        return self._default == NO_DEFAULT

    @property
    def default(self) -> object:
        if self._default == NO_DEFAULT:  # pragma: no cover
            raise InternalError(
                f"attempted to retrieve default of required from_context parameter {self.key}"
            )
        return self._default

    @staticmethod
    def from_parameter(key: str, parameter: "TypedParameter") -> "FromContextField":
        return FromContextField(
            key,
            parameter.type_hint,
            NO_DEFAULT if parameter.is_required() else parameter.default,
        )


@dataclass(frozen=True)
class SkippedField(_PseudoField):
    default: object


PseudoField = Union[ContextField, FromContextField, SkippedField]

Field = Union[SingleField, PseudoField]


@dataclass(frozen=True)
class VariadicField:
    constructor: InternalConstructor[object]


@dataclass(frozen=True)
class TypedParameter(type_utils.Parameter):
    type_hint: Target[object]

    def is_context(self) -> bool:
        return self.type_hint is Context


def add_type_hints(
    type_: Target[object], params: Sequence[type_utils.Parameter]
) -> List[TypedParameter]:
    type_hints = type_utils.get_type_hints(type_, params)
    return [
        TypedParameter(p.parameter, _strip_initvar(type_hints[p.name])) for p in params
    ]


def skip(
    metadata: MetadataCollection,
    factory: InternalFactory,
    target: Target[Any],
    parameter: type_utils.Parameter,
) -> bool:
    if not terramare.metadata.skip.read(metadata, target, parameter.name):
        return False
    if parameter.is_required():
        raise factory.make_error(f"cannot skip required parameter: {parameter.name}")
    return True


def handle_positional_pseudo_field(
    index: int, field: PseudoField, context: Context
) -> object:
    if isinstance(field, ContextField):
        _log.debug("Positional parameter %d using context: %s", index, context)
        return context
    elif isinstance(field, FromContextField):
        if field.key in context:
            value = context[field.key]
            _log.debug(
                "Positional parameter %d using context field '%s': %s",
                index,
                field.key,
                value,
            )
            return value
        elif field.required:  # pragma: no cover
            raise InternalError(f"missing required context: {field.key}")
        else:
            _log.debug(
                "Positional parameter %d using default value for context field '%s': %s",
                index,
                field.key,
                field.default,
            )
            return field.default
    elif isinstance(field, SkippedField):
        _log.debug(
            "Positional parameter %d using default value for skipped field: %s",
            index,
            field.default,
        )
        return field.default
    else:  # pragma: no cover
        raise InternalError(f"Unknown PseudoField variant ({type(field)}): {field}")


OMIT = object()


def handle_keyword_pseudo_field(
    name: str, field: PseudoField, context: Context
) -> object:
    if isinstance(field, ContextField):
        _log.debug("Keyword parameter '%s' using context: %s", name, context)
        return context
    elif isinstance(field, FromContextField):
        if field.key in context:
            value = context[field.key]
            _log.debug(
                "Keyword parameter '%s' using context field '%s': %s",
                name,
                field.key,
                value,
            )
            return value
        elif field.required:  # pragma: no cover
            raise InternalError(f"missing required context: {field.key}")
        else:
            _log.debug(
                "Omitting keyword parameter '%s' for optional context field '%s'",
                name,
                field.key,
            )
            return OMIT
    elif isinstance(field, SkippedField):
        _log.debug("Keyword parameter '%s' field skipped", name)
        return OMIT
    else:  # pragma: no cover
        raise InternalError(f"Unknown PseudoField variant ({type(field)}): {field}")


def _strip_initvar(target: Target[object]) -> Target[object]:
    # One or other of these branches is covered, depending on the Python
    # version.
    if isinstance(target, InitVar) and hasattr(target, "type"):  # pragma: no cover
        return target.type
    if target is InitVar:  # pragma: no cover
        raise type_utils.ParameterError(
            "'InitVar' is not supported before Python 3.8 as it does not "
            "contain the necessary type information - see "
            "https://bugs.python.org/issue33569."
        )
    return target
