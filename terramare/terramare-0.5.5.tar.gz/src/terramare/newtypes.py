"""Deserializer for a newtype alias."""

from typing import Any, NewType, TypeVar

from .core import ConstructorCore, FactoryCore, InternalFactory
from .errors import UnsupportedTargetTypeError
from .types import Target

_T_co = TypeVar("_T_co", covariant=True)


class NewTypeFactory(FactoryCore):
    def create_constructor(
        self, factory: "InternalFactory", target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not _is_newtype(target):
            raise UnsupportedTargetTypeError
        return factory.create_constructor(getattr(target, "__supertype__")).unwrap()


def _is_newtype(target: Target[Any]) -> bool:
    if isinstance(NewType, type):  # pragma: no cover
        # In Python 3.10+ NewType is a class, so we can use isinstance to
        # determine whether a type is a NewType.
        return isinstance(  # pylint: disable=isinstance-second-argument-not-valid-type
            target, NewType
        )
    else:
        # Before Python 3.10 NewType is a function. We have to use the qualified
        # name of the type to figure out whether it is a NewType.
        return getattr(target, "__qualname__", None) == "NewType.<locals>.new_type"
