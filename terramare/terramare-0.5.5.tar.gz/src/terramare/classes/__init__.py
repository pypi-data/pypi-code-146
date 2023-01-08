"""Deserializer factory to construct an instance of a class type."""

import dataclasses
import logging
from dataclasses import dataclass
from typing import Any, Iterator, Optional, Tuple, Type, TypeVar

from typing_extensions import final

from .. import type_utils
from ..core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from ..data import Value
from ..errors import UnsupportedTargetTypeError, ValidationException
from ..metadata import MetadataCollection
from ..types import Target
from .from_array import FromArrayConstructor
from .from_object import FromObjectConstructor
from .from_value import FromValueConstructor
from .metadata import (
    ARRAY,
    OBJECT,
    VALUE,
    FromType,
    auto,
    disallow_unknown_fields,
    handle_exception_types,
)
from .utils import add_type_hints

__all__ = [
    "ARRAY",
    "OBJECT",
    "VALUE",
    "ClassFactory",
    "FromType",
    "auto",
    "disallow_unknown_fields",
    "handle_exception_types",
]

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)


@final
@dataclass(frozen=True)
class ClassFactory(FactoryCore):
    _metadata: MetadataCollection

    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[_T_co]):
        _from_object: Optional[InternalConstructor[_T_co]]
        _from_array: Optional[InternalConstructor[_T_co]]
        _from_value: Optional[InternalConstructor[_T_co]]
        _handle_exception_types: Tuple[Type[Exception], ...]

        def __call__(self, data: "Value") -> _T_co:
            def get_constructor() -> Optional[InternalConstructor[_T_co]]:
                if data.is_object() and self._from_object:
                    return self._from_object
                if data.is_array() and self._from_array:
                    return self._from_array
                if self._from_value:
                    return self._from_value
                return None

            constructor = get_constructor()
            if not constructor:
                constructors = []
                if self._from_object:
                    constructors.append("object")
                if self._from_array:
                    constructors.append("array")
                raise data.make_error(f"expected {' or '.join(constructors)}")
            core = constructor.unwrap()
            try:
                return core(data)
            except self._handle_exception_types as e:  # pylint: disable=catching-non-exception
                raise data.make_error(  # pylint: disable=bad-exception-context
                    str(e)
                ) from e

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            if self._from_object:
                yield self._from_object
            if self._from_array:
                yield self._from_array
            if self._from_value:
                yield self._from_value

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not hasattr(target, "__call__"):
            raise UnsupportedTargetTypeError

        try:
            add_type_hints(target, type_utils.get_parameters(target))
        except type_utils.ParameterError as e:
            raise factory.make_error(str(e))

        fromtypes = _get_fromtypes(self._metadata, target)
        if fromtypes is None:
            raise factory.make_error("class construction not enabled for target")
        if not fromtypes:
            raise factory.make_error("class construction disabled for target")

        from_object = None
        if OBJECT <= fromtypes:
            from_object = FromObjectConstructor.new(self._metadata, factory, target)

        from_array = None
        if ARRAY <= fromtypes:
            from_array = FromArrayConstructor.new(self._metadata, factory, target)

        from_value = None
        if VALUE <= fromtypes:
            from_value = FromValueConstructor.new(self._metadata, factory, target)

        return type(self)._Constructor(
            _from_object=from_object,
            _from_array=from_array,
            _from_value=from_value,
            _handle_exception_types=(
                ValidationException,
                *handle_exception_types.read(self._metadata, target),
            ),
        )


def _get_fromtypes(
    metadata: MetadataCollection, target: Target[Any]
) -> Optional[FromType]:
    from_types = auto.read(metadata, target)
    if from_types is not None:
        return from_types
    if dataclasses.is_dataclass(target) or hasattr(target, "__attrs_attrs__"):
        return OBJECT
    if _is_namedtuple(target):
        return OBJECT | ARRAY
    return None


def _is_namedtuple(target: Target[_T_co]) -> bool:
    if getattr(target, "__bases__", None) != (tuple,):
        return False
    fields = getattr(target, "_fields", None)
    return isinstance(fields, tuple) and all(isinstance(field, str) for field in fields)
