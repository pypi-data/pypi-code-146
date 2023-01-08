"""Deserializers for typed dictionaries."""

from dataclasses import dataclass
from typing import Any, Dict, Iterator, Mapping, MutableMapping, TypeVar, cast

from typing_extensions import TypedDict, final

from . import type_utils
from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import UnsupportedTargetTypeError
from .types import Target

_T_co = TypeVar("_T_co", covariant=True)
_V_in = TypeVar("_V_in")


@final
@dataclass(frozen=True)
class MappingFactory(FactoryCore):
    # Logically _Constructor: ConstructorImpl[MappingLike[_T_co]] for
    # SequenceLike in {Mapping, Dict, ...}. Representing this requires HKTs
    # which are not currently available.
    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[Dict[str, _V_in]]):
        _value_constructor: InternalConstructor[_V_in]

        def __call__(self, data: Value) -> Dict[str, _V_in]:
            object_data = data.as_object()
            return {
                key: self._value_constructor(object_data[key]) for key in object_data
            }

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            yield self._value_constructor

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if type_utils.get_base_of_generic_type(target) not in {
            Dict,
            Mapping,
            MutableMapping,
        }:
            raise UnsupportedTargetTypeError
        [key_type, value_type] = type_utils.get_type_parameters(target)
        if key_type is not str:
            raise factory.make_error("only dictionary keys of type str are supported")
        return cast(
            ConstructorCore[_T_co],
            type(self)._Constructor(
                factory.create_constructor(value_type, frame="value type"),
            ),
        )


@final
@dataclass(frozen=True)
class TypedDictFactory(FactoryCore):
    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[Dict[str, Any]]):
        fields: Mapping[str, InternalConstructor[Any]]
        total: bool

        def __call__(self, data: Value) -> Dict[str, Any]:
            object_data = data.as_object()
            result: Dict[str, Any] = {}

            for field, constructor in self.fields.items():
                if field in object_data:
                    result[field] = constructor(object_data[field])
                elif self.total:
                    raise data.make_error(f"missing required field: {field}")

            unused_fields = set(object_data) - set(result)
            if unused_fields:
                raise data.make_error(f"unknown field: {sorted(unused_fields)[0]}")
            return object_data.raw

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(self.fields.values())

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if type_utils.get_base_of_generic_type(target) is not TypedDict:
            raise UnsupportedTargetTypeError
        return cast(
            ConstructorCore[_T_co],
            type(self)._Constructor(
                {
                    field: factory.create_constructor(
                        field_type, frame=f'field "{field}"'
                    )
                    for field, field_type in target.__annotations__.items()
                },
                getattr(target, "__total__"),
            ),
        )
