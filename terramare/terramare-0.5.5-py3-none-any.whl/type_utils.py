"""Common utility functions for dealing with generic types."""

import contextlib
import inspect
import sys
import typing
from collections import abc
from dataclasses import dataclass
from functools import partial
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Set,
    Tuple,
    cast,
)

from typing_extensions import Literal, TypedDict

from .errors import InternalError, TerramareError
from .types import LiteralMeta, Target, TypedDictMetas


def get_base_of_generic_type(type_: Target[object]) -> Optional[Target[object]]:
    """Return the generic type of which a type_ is an instance."""
    type_ = _normalize_type(type_)
    for attribute in ("__origin__", "__class__"):
        if hasattr(type_, attribute):
            return _coalesce_type(getattr(type_, attribute))
    return None  # pragma: no cover


def get_type_parameters(from_type: Target[Any]) -> List[type]:
    """Extract the type parameters from a parametrized type."""

    def extract_type_parameters(type_: Target[Any]) -> List[type]:
        type_ = _normalize_type(type_)
        with contextlib.suppress(AttributeError):
            if type_.__args__ is not None:  # type: ignore[union-attr]
                return list(type_.__args__)  # type: ignore[union-attr]
        # Not covered on Python 3.8+.
        with contextlib.suppress(AttributeError):  # pragma: no cover
            if type_.__values__ is not None:  # type: ignore[union-attr]
                return list(type_.__values__)  # type: ignore[union-attr]
        return []

    from_type = _normalize_type(from_type)
    type_params = extract_type_parameters(_normalize_type(from_type))
    # Not covered on Python 3.8+.
    if getattr(from_type, "__class__", None) is LiteralMeta:  # pragma: no cover
        # Special-case Literal types, as Literal[()] != Literal[]
        return type_params
    return type_params if type_params != [()] else []


@dataclass(frozen=True)
class Parameter:
    """
    A function parameter.

    A view on 'inspect.Parameter' with convenience functions for our use case.
    """

    parameter: inspect.Parameter

    @property
    def name(self) -> str:
        return self.parameter.name

    @property
    def annotation(self) -> Any:
        return self.parameter.annotation

    def is_positional(self) -> bool:
        return self.parameter.kind in {
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.VAR_POSITIONAL,
        }

    def is_positional_only(self) -> bool:
        return self.parameter.kind in {
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.VAR_POSITIONAL,
        }

    def is_optional(self) -> bool:
        if self.parameter.default == inspect.Parameter.empty:
            return False
        return True

    @property
    def default(self) -> object:
        if not self.is_optional():
            raise InternalError(
                f"attempted to retrieve default of required parameter {self.name}"
            )
        return self.parameter.default

    def is_required(self) -> bool:
        return not (self.is_optional() or self.is_variadic())

    def is_variadic(self) -> bool:
        return self.parameter.kind in {
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        }


@dataclass(frozen=True)
class ParameterError(TerramareError):
    """Raised when failing to determine the parameters of a callable."""

    message: str


def get_parameters(type_: Target[object]) -> List[Parameter]:
    """Retrieve the parameters of the given callable."""
    try:
        return [Parameter(p) for p in inspect.signature(type_).parameters.values()]
    except ValueError as e:
        raise ParameterError(str(e)) from e


def get_type_hints(
    type_: Target[object], params: Sequence[Parameter]
) -> Dict[str, Target[object]]:
    """Retrieve the type hints of the parameters of the given callable."""
    if hasattr(type_, "__globals__"):
        globals_ = getattr(type_, "__globals__")
    elif hasattr(type_, "__module__"):
        globals_ = vars(sys.modules[getattr(type_, "__module__")])
    else:  # pragma: no cover TODO
        globals_ = {}

    # For some reason `get_type_hints` can't handle the type returned by
    # `functools.partial` - but it _can_ handle its `__call__` method.
    if isinstance(type_, partial):
        type_ = type_.__call__

    try:
        type_hints = typing.get_type_hints(type_, globals_)
    except TypeError as e:  # pragma: no cover
        raise ParameterError(str(e)) from None

    def get_type_hint(p: Parameter) -> Any:
        if p.name in type_hints:
            return type_hints[p.name]
        if p.annotation == inspect.Parameter.empty:
            return Any
        if not isinstance(p.annotation, str):
            return p.annotation
        return eval(  # pragma: no cover, pylint: disable=eval-used
            p.annotation, globals_
        )

    return {p.name: get_type_hint(p) for p in params}


def _normalize_type(type_: Target[object]) -> Target[object]:
    type_ = _coalesce_type(type_)
    try:
        return cast(
            Target[object],
            {
                AbstractSet: AbstractSet[Any],
                Callable: Callable[..., Any],
                Dict: Dict[str, Any],
                FrozenSet: FrozenSet[Any],
                Iterable: Iterable[Any],
                Iterator: Iterator[Any],
                List: List[Any],
                Mapping: Mapping[str, Any],
                MutableMapping: Mapping[str, Any],
                MutableSequence: MutableSequence[Any],
                Sequence: Sequence[Any],
                Set: Set[Any],
                Tuple: Tuple[Any, ...],
            }[type_],
        )
    except (KeyError, TypeError):
        return type_


def _coalesce_type(type_: Target[object]) -> Target[object]:
    try:
        return cast(
            Target[object],
            {
                abc.Callable: Callable,
                abc.Iterable: Iterable,
                abc.Iterator: Iterator,
                abc.Mapping: Mapping,
                abc.MutableMapping: MutableMapping,
                abc.MutableSequence: MutableSequence,
                abc.Sequence: Sequence,
                abc.Set: Set,
                dict: Dict,
                frozenset: FrozenSet,
                list: List,
                LiteralMeta: Literal,
                set: Set,
                tuple: Tuple,
                **{meta: TypedDict for meta in TypedDictMetas},
            }[type_],
        )
    except (KeyError, TypeError):
        return type_
