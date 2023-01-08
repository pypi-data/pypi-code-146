"""Class-specific metadata."""

import enum
from dataclasses import dataclass
from typing import (
    AbstractSet,
    Any,
    ClassVar,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import Final

from ..metadata import Metadata
from ..types import Target


@dataclass(frozen=True)
class _disallow_unknown_fields(Metadata[bool]):

    KEY: ClassVar[str] = f"{__name__}._disallow_unknown_fields"
    DEFAULT: ClassVar[bool] = False

    @property
    def value(self) -> bool:
        return True


#: Raise :exc:`terramare.errors.ConstructorError` if there are fields present in
#: the primitive that are not defined by the decorated class.
disallow_unknown_fields = _disallow_unknown_fields()


@dataclass(init=False)
class handle_exception_types(Metadata[Tuple[Type[Exception], ...]]):
    """
    Handle the listed exception types when constructing an instance of the decorated class.

    An exception of one of these types will be caught and re-raised as a
    :exc:`terramare.errors.ValidationError` including the full construction
    context.

    >>> import attr
    >>> import terramare
    >>>
    >>> @terramare.handle_exception_types(ValueError)
    ... @attr.s(auto_attribs=True)
    ... class User:
    ...     id: int = attr.ib()
    ...     name: str
    ...
    ...     @id.validator
    ...     def positive(self, _, value):
    ...         if not value > 0:
    ...             raise ValueError("id must be positive!")
    >>>
    >>> terramare.structure({"id": 0, "name": "Alice"}, into=User)
    Traceback (most recent call last):
    ...
    terramare.errors.ConstructorError: .: id must be positive!
    ...
    """

    KEY: ClassVar[str] = f"{__name__}.handle_exception_types"
    DEFAULT: ClassVar[Tuple[Type[Exception], ...]] = ()

    _value: Tuple[Type[Exception], ...]

    @property
    def value(self) -> Tuple[Type[Exception], ...]:
        return self._value

    def __init__(self, *exceptions: Type[Exception]) -> None:
        self._value = exceptions


@enum.unique
class _FromType(enum.Enum):
    OBJECT = "object"
    ARRAY = "array"
    LEAF = "leaf"


FromType = AbstractSet[_FromType]

OBJECT: Final = frozenset({_FromType.OBJECT})
ARRAY: Final = frozenset({_FromType.ARRAY})
VALUE: Final = frozenset({_FromType.LEAF})

_AUTO_KEY: Final[str] = f"{__name__}.auto"

_T_in = TypeVar("_T_in")
_Target = TypeVar("_Target", bound=Target[Any])


@dataclass(frozen=True)
class _auto(Metadata[Optional[FromType]]):
    KEY: ClassVar[str] = _AUTO_KEY
    DEFAULT: ClassVar[Optional[FromType]] = None

    @dataclass(frozen=True)
    class inner(Metadata[Optional[FromType]]):
        KEY: ClassVar[str] = _AUTO_KEY
        DEFAULT: ClassVar[Optional[FromType]] = None

        _value: FromType

        @property
        def value(self) -> FromType:
            return self._value

    @property
    def value(self) -> FromType:
        return OBJECT

    @overload
    def __call__(self, __enable: bool) -> "_auto.inner":
        ...  # pragma: no cover

    @overload
    def __call__(self, *, from_: FromType) -> "_auto.inner":
        ...  # pragma: no cover

    @overload
    def __call__(self, target: _Target) -> _Target:
        ...  # pragma: no cover

    def __call__(
        self,
        target: Optional[Union[bool, Target[_T_in]]] = None,
        from_: Optional[FromType] = None,
    ) -> Union["_auto.inner", Target[_T_in]]:
        if isinstance(target, bool):
            # First overload
            if target:
                return _auto.inner(OBJECT)
            return _auto.inner(frozenset())
        if from_ is not None:
            # Second overload
            return _auto.inner(from_)
        # Third overload
        assert target is not None
        return _auto.inner(self.value)(target)


#: Automatically create a constructor for the decorated class.
auto = _auto()
