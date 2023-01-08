"""Deserializers for primitive types."""

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Mapping, TypeVar, cast

from typing_extensions import Final, final

from .core import ConstructorCore, FactoryCore, InternalConstructor, InternalFactory
from .data import Value
from .errors import UnsupportedTargetTypeError
from .types import Primitive, Target

_T_co = TypeVar("_T_co", covariant=True)


_BOOL_STRINGS: Final[Mapping[str, bool]] = {
    "y": True,
    "Y": True,
    "yes": True,
    "Yes": True,
    "YES": True,
    "n": False,
    "N": False,
    "no": False,
    "No": False,
    "NO": False,
    "true": True,
    "True": True,
    "TRUE": True,
    "false": False,
    "False": False,
    "FALSE": False,
    "on": True,
    "On": True,
    "ON": True,
    "off": False,
    "Off": False,
    "OFF": False,
}


@final
@dataclass(frozen=True)
class NoneFactory(FactoryCore):
    class _Constructor(ConstructorCore[None]):
        def __call__(self, data: Value) -> None:
            if data.raw is not None:
                raise data.make_error("expected null")
            return data.raw

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not type(None):  # noqa: E721
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())


@final
@dataclass(frozen=True)
class BoolFactory(FactoryCore):
    @dataclass(frozen=True)
    class _Constructor(ConstructorCore[bool]):
        values: Mapping[str, bool]

        def __call__(self, data: Value) -> bool:
            if data.config.coerce_strings:
                return self._construct_coerce(data)
            else:
                return self._construct_no_coerce(data)

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

        def _construct_no_coerce(self, data: Value) -> bool:
            if isinstance(data.raw, bool):
                return data.raw
            raise data.make_error("expected bool")

        def _construct_coerce(self, data: Value) -> bool:
            if isinstance(data.raw, str):
                if data.raw in self.values:
                    return self.values[data.raw]
            values_str = "|".join(self.values)
            raise data.make_error(
                f"expected (string representation of) bool ({values_str})"
            )

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not bool:
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor(_BOOL_STRINGS))


@final
@dataclass(frozen=True)
class IntFactory(FactoryCore):
    class _Constructor(ConstructorCore[int]):
        def __call__(self, data: Value) -> int:
            if data.config.coerce_strings:
                return self._construct_coerce(data)
            else:
                return self._construct_no_coerce(data)

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

        def _construct_no_coerce(self, data: Value) -> int:
            # bool is a subclass of int - we want to make sure what we have is
            # actually an int.
            if isinstance(data.raw, int) and not isinstance(data.raw, bool):
                return data.raw
            raise data.make_error("expected integer")

        def _construct_coerce(self, data: Value) -> int:
            if isinstance(data.raw, str):
                try:
                    return int(data.raw)
                except ValueError:
                    pass
            raise data.make_error("expected (string representation of) integer")

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not int:
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())


@final
@dataclass(frozen=True)
class FloatFactory(FactoryCore):
    class _Constructor(ConstructorCore[float]):
        def __call__(self, data: Value) -> float:
            if data.config.coerce_strings:
                return self._construct_coerce(data)
            else:
                return self._construct_no_coerce(data)

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

        def _construct_no_coerce(self, data: Value) -> float:
            if isinstance(data.raw, float):
                return data.raw

            # Both floats and ints are acceptable.
            if isinstance(data.raw, int):
                return float(data.raw)
            raise data.make_error("expected number")

        def _construct_coerce(self, data: Value) -> float:
            if isinstance(data.raw, str):
                try:
                    return float(data.raw)
                except ValueError:
                    pass
            raise data.make_error("expected (string representation of) number")

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not float:
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())


@final
@dataclass(frozen=True)
class StrFactory(FactoryCore):
    class _Constructor(ConstructorCore[str]):
        def __call__(self, data: Value) -> str:
            if not isinstance(data.raw, str):
                raise data.make_error("expected string")
            return data.raw

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not str:
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())


@final
@dataclass(frozen=True)
class PrimitiveListFactory(FactoryCore):
    class _Constructor(ConstructorCore[List[Primitive]]):
        def __call__(self, data: Value) -> List[Primitive]:
            return data.as_array().raw

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not list:
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())


@final
@dataclass(frozen=True)
class PrimitiveDictFactory(FactoryCore):
    class _Constructor(ConstructorCore[Dict[str, Primitive]]):
        def __call__(self, data: Value) -> Dict[str, Primitive]:
            return data.as_object().raw

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if target is not dict:
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())


@final
@dataclass(frozen=True)
class AnyFactory(FactoryCore):
    class _Constructor(ConstructorCore[Any]):
        def __call__(self, data: Value) -> Any:
            return data.raw

        def get_children(self) -> Iterator[InternalConstructor[Any]]:
            return iter(())

    def create_constructor(
        self, _: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        if not (target is Any or target is object):
            raise UnsupportedTargetTypeError
        return cast(ConstructorCore[_T_co], type(self)._Constructor())
