"""Common types and re-exports."""

from typing import Any, Callable, Dict, List, Type, TypeVar, Union

from typing_extensions import Literal, Protocol

TypedDictMetas = set()

# pylint: disable=unused-import
try:  # pragma: no cover
    from typing import _TypedDictMeta  # type: ignore[attr-defined]

    TypedDictMetas.add(_TypedDictMeta)

except ImportError:  # pragma: no cover
    pass

# pylint: disable=unused-import
try:  # pragma: no cover
    from typing_extensions import _TypedDictMeta  # type: ignore[attr-defined]

    TypedDictMetas.add(_TypedDictMeta)
except ImportError:  # pragma: no cover
    pass

try:  # pragma: no cover
    from typing_extensions import _Literal  # type: ignore[attr-defined]

    LiteralMeta = _Literal
except ImportError:  # pragma: no cover
    LiteralMeta = Literal


_T_in = TypeVar("_T_in")
_T_co = TypeVar("_T_co", covariant=True)

_PrimitiveRecursor = Union[
    None,
    bool,
    int,
    float,
    str,
    List[_T_co],
    Dict[str, _T_co],
]
_Primitive0 = _PrimitiveRecursor[Any]
_Primitive1 = _PrimitiveRecursor[_Primitive0]
_Primitive2 = _PrimitiveRecursor[_Primitive1]

Primitive = _PrimitiveRecursor[_Primitive2]
ArrayPrimitive = List[_Primitive2]
ObjectPrimitive = Dict[str, _Primitive2]


Target = Union[Type[_T_co], Callable[..., _T_co]]


class Lazy(Protocol[_T_co]):
    def __call__(self) -> _T_co:
        ...  # pragma: no cover


class Decorator(Protocol):
    def __call__(self, __target: Target[_T_in]) -> Target[_T_in]:
        ...  # pragma: no cover
