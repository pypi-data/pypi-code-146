"""Deserializer for a generalized homogenous sequence."""

from dataclasses import dataclass
from typing import (
    AbstractSet,
    Any,
    Callable,
    FrozenSet,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableSequence,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    cast,
)

from typing_extensions import Final, Protocol, final

from . import type_utils
from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import UnsupportedTargetTypeError
from .types import Target

_T_co = TypeVar("_T_co", covariant=True)

_SEQUENCE_TYPES: Final[Mapping[Target[Any], Callable[[Sequence[Any]], Any]]] = {
    AbstractSet: set,
    FrozenSet: frozenset,
    Iterable: list,
    Iterator: iter,
    List: list,
    MutableSequence: list,
    Sequence: list,
    Set: set,
}


_E_in = TypeVar("_E_in")
_E_contra = TypeVar("_E_contra", contravariant=True)


class _ConstructFn(Protocol[_E_contra, _T_co]):
    def __call__(self, __sequence: Sequence[_E_contra]) -> _T_co:
        ...  # pragma: no cover


@final
@dataclass(frozen=True)
class SequenceFactory(FactoryCore):
    # Logically _Constructor: ConstructorImpl[SequenceLike[_T_co]] for
    # SequenceLike in {Sequence, List, ...}. Representing this requires HKTs
    # which are not currently available.
    @dataclass(frozen=True)
    class _Constructor(Generic[_T_co, _E_in], ConstructorCore[_T_co]):
        _element_constructor: InternalConstructor[_E_in]
        _construct_fn: _ConstructFn[_E_in, _T_co]

        def __call__(self, data: Value) -> _T_co:
            array_data = data.as_array()
            return self._construct_fn(
                [
                    self._element_constructor(array_data[index])
                    for index in range(len(array_data))
                ]
            )

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            yield self._element_constructor

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        base = type_utils.get_base_of_generic_type(target)
        if not base or base not in _SEQUENCE_TYPES:
            raise UnsupportedTargetTypeError
        [element_type] = type_utils.get_type_parameters(target)
        return cast(
            ConstructorCore[_T_co],
            type(self)._Constructor(
                factory.create_constructor(element_type, frame="element type"),
                _SEQUENCE_TYPES[base],
            ),
        )


_E = TypeVar("_E")


@final
@dataclass(frozen=True)
class TupleFactory(FactoryCore):
    @dataclass(frozen=True)
    class _TupleConstructor(ConstructorCore[Tuple[Any, ...]]):
        _element_constructors: Sequence[InternalConstructor[Any]]

        def __call__(self, data: Value) -> Tuple[Any, ...]:
            array_data = data.as_array()
            if len(array_data) < len(self._element_constructors):
                raise data.make_error(
                    f"too few elements ({len(array_data)}) - "
                    f"expected {len(self._element_constructors)}"
                )
            if len(array_data) > len(self._element_constructors):
                raise data.make_error(
                    f"too many elements ({len(array_data)}) - "
                    f"expected {len(self._element_constructors)}"
                )
            return tuple(
                self._element_constructors[index](array_data[index])
                for index in range(len(self._element_constructors))
            )

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(self._element_constructors)

    @dataclass(frozen=True)
    class _VariadicTupleConstructor(ConstructorCore[Tuple[_E, ...]]):
        _element_constructor: InternalConstructor[_E]

        def __call__(self, data: Value) -> Tuple[_E, ...]:
            array_data = data.as_array()
            return tuple(
                self._element_constructor(array_data[index])
                for index in range(len(array_data))
            )

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            yield self._element_constructor

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if type_utils.get_base_of_generic_type(target) is not Tuple:
            raise UnsupportedTargetTypeError
        element_types = type_utils.get_type_parameters(target)
        if element_types and element_types[-1] == Ellipsis:
            constructor: ConstructorCore[Any] = type(self)._VariadicTupleConstructor(
                factory.create_constructor(element_types[0], frame="tuple element 0")
            )
        else:
            constructor = type(self)._TupleConstructor(
                [
                    factory.create_constructor(
                        element_type, frame=f"tuple element {index}"
                    )
                    for index, element_type in enumerate(element_types)
                ]
            )
        return constructor
