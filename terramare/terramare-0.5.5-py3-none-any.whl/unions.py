"""Deserializer for a union of types."""

import logging
from dataclasses import dataclass
from typing import Any, Iterator, List, Sequence, TypeVar, Union

from typing_extensions import final

from . import type_utils
from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import ConstructorError, UnsupportedTargetTypeError
from .types import Target

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)


@final
@dataclass(frozen=True)
class UnionFactory(FactoryCore):
    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[_T_co]):
        _variant_constructors: Sequence[InternalConstructor[_T_co]]

        def __call__(self, data: "Value") -> _T_co:
            errors: List[ConstructorError] = []
            for index, constructor in enumerate(self._variant_constructors):
                try:
                    _log.debug("Trying union variant %d: %s", index, constructor)
                    value = constructor(data)
                    _log.debug("Successfully constructed union variant %d", index)
                    return value
                except ConstructorError as e:
                    _log.debug("Constructor error for union variant %d: %s", index, e)
                    errors.append(e)
            raise sorted(errors, reverse=True)[0]

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(self._variant_constructors)

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if type_utils.get_base_of_generic_type(target) is not Union:
            raise UnsupportedTargetTypeError
        return type(self)._Constructor(
            [
                factory.create_constructor(variant_type, frame=f"union variant {index}")
                for index, variant_type in enumerate(
                    type_utils.get_type_parameters(target)
                )
            ]
        )
