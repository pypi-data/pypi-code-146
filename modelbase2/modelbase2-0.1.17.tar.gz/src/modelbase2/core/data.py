from __future__ import annotations

from ..types import Array
from .utils import check_function_arity
from dataclasses import dataclass, field
from typing import Any, Callable, Generator, Iterable, Protocol, TypeVar, Union

T = TypeVar("T")


class Arithmetic(Protocol[T]):
    def __add__(self, other: T) -> T:
        ...

    def __mul__(self, other: T) -> T:
        ...


RateFunction = Callable[..., float]
ModuleFunction = Callable[..., Iterable[float]]
StoichiometryByReaction = dict[str, float]
StoichiometryByVariable = dict[str, float]
ValueData = Union[
    dict[str, float],
    dict[str, list[float]],
    dict[str, Array],
    Array,
    list[float],
]
TimeData = Union[float, list[float], Array]


@dataclass
class Variable:
    name: str
    unit: str


@dataclass
class Constant:
    name: str
    value: float
    unit: str
    sources: list[str] = field(default_factory=list)


@dataclass
class DerivedConstant:
    name: str
    function: RateFunction
    args: list[str]
    unit: str


@dataclass
class DerivedStoichiometry:
    function: RateFunction
    args: list[str]


@dataclass
class AlgebraicModule:
    name: str
    function: ModuleFunction
    derived_variables: list[str]
    args: list[str]

    def __post_init__(self) -> None:
        if not check_function_arity(function=self.function, arity=len(self.args)):
            raise ValueError(f"Function arity does not match args of {self.name}")

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __iter__(self) -> Generator:
        yield from self.__dict__

    def keys(self) -> tuple[str, ...]:
        """Get all valid keys of the algebraic module"""
        return tuple(self.__dict__)


@dataclass
class Rate:
    name: str
    function: RateFunction
    args: list[str]

    def __post_init__(self) -> None:
        if not check_function_arity(function=self.function, arity=len(self.args)):
            raise ValueError(f"Function arity does not match args of {self.name}")

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __iter__(self) -> Generator:
        yield from self.__dict__

    def keys(self) -> tuple[str, ...]:
        return tuple(self.__dict__)


@dataclass
class Reaction:
    name: str
    function: RateFunction
    stoichiometry: StoichiometryByReaction
    args: list[str]
    derived_stoichiometry: dict[str, DerivedStoichiometry] = field(default_factory=dict)
