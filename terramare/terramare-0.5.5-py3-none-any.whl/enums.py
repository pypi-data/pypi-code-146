"""Deserializer for an enum."""

import enum
import logging
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    List,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from typing_extensions import Final, Literal, Protocol, final

from . import pretty_printer, type_utils
from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import ConstructorError, UnsupportedTargetTypeError
from .types import Target

# We should really support bool type literals, too, but it is surprisingly
# tricky to tell the difference between Literal[1] and Literal[True] (and
# similarly Literal[0] and Literal[False]).
# The behaviour varies between Python versions and even depending on execution
# order. In a Python 3.8 interpreter session, for example, the value of
# Literal[1].__args__ and Literal[True].__args__ is either (True,) or (1,)
# depending on which was evaluated first!
_SUPPORTED_TYPES: Final[Sequence[type]] = [type(None), int, str]

_log = logging.getLogger(__name__)


_VariantType = TypeVar("_VariantType", None, int, str)
_T_co = TypeVar("_T_co", covariant=True)


@final
@dataclass(frozen=True)
class EnumFactory(FactoryCore):
    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not (isinstance(target, type) and issubclass(target, enum.Enum)):
            raise UnsupportedTargetTypeError
        variants: Sequence[_EnumVariant] = list(target)
        _log.debug("Extracted enum variants %s", variants)
        for variant in variants:
            if type(variant.value) not in _SUPPORTED_TYPES:
                raise factory.push_stack(
                    type(variant.value), frame=f"variant {variant.name}"
                ).make_error(
                    "only enum values of type None, bool, int, and str are supported"
                )
        return _Constructor(
            _variant_constructors=[
                _VariantConstructorImpl(
                    v,
                    v.value,
                    factory.create_constructor(
                        type(v.value), frame=f"variant {v.name}"
                    ),
                )
                for v in variants
            ],
        )


@final
@dataclass(frozen=True)
class LiteralFactory(FactoryCore):
    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if type_utils.get_base_of_generic_type(target) is not Literal:
            raise UnsupportedTargetTypeError
        variants = type_utils.get_type_parameters(target)
        _log.debug("Extracted literal variants %s", variants)
        for variant in variants:
            if not any(isinstance(variant, t) for t in _SUPPORTED_TYPES):
                raise factory.push_stack(
                    type(variant),
                    frame=f"variant {variant}",
                ).make_error(
                    "only literal variants of type None, int, and str are supported"
                )
        return _Constructor(
            _variant_constructors=[
                _VariantConstructorImpl(
                    variant,
                    variant,
                    factory.create_constructor(
                        type(variant), frame=f"variant {variant}"
                    ),
                )
                for variant in variants
            ],
        )


@dataclass(frozen=True)
class _VariantConstructorImpl(Generic[_VariantType]):
    variant: _VariantType
    value: Any
    constructor: InternalConstructor[_VariantType]


@dataclass(frozen=True)
class _Constructor(ConstructorCore[_T_co]):
    _variant_constructors: Sequence[_VariantConstructorImpl[Any]]

    def __call__(self, data: Value) -> _T_co:
        possible_variants: List[Tuple[_VariantConstructorImpl[Any], Any]] = []
        for variant in self._variant_constructors:
            try:
                possible_variants.append((variant, variant.constructor(data)))
            except ConstructorError:
                pass

        if not possible_variants:
            coercing_strings_str = ""
            if data.config.coerce_strings:
                coercing_strings_str = "(string representation of) "
            variant_types_str = _prepend_one_of(
                {
                    pretty_printer.print_type_name(type(variant.value))
                    for variant in self._variant_constructors
                }
            )
            raise data.make_error(f"expected {coercing_strings_str}{variant_types_str}")

        for variant, value in possible_variants:
            if variant.value == value:
                return variant.variant

        coercing_strings_str = ""
        if data.config.coerce_strings:
            coercing_strings_str = "(string representation of) "
        variants_str = _prepend_one_of(
            _quote_literal_variant(v.value) for v in self._variant_constructors
        )
        raise data.make_error(
            f"unknown variant - expected {coercing_strings_str}{variants_str}"
        )

    def get_children(self) -> Iterator[InternalConstructor[Any]]:
        for variant in self._variant_constructors:
            yield variant.constructor


def _prepend_one_of(elements: Iterable[str]) -> str:
    elements = list(elements)
    if len(elements) == 1:
        return elements[0]
    return f"one of {{{','.join(sorted(elements))}}}"


def _quote_literal_variant(variant: Union[None, bool, int, str]) -> str:
    if variant is None or isinstance(variant, (bool, int, bytes)):
        return str(variant)
    return variant.replace("\\", "\\\\").replace('"', '\\"')


class _EnumVariant(Protocol):
    name: str
    value: Any
