"""Automatically deserialize complex objects from simple Python types."""

import logging
from typing import Any, Mapping, Optional, TypeVar, overload

from typing_extensions import Final

from .core import Factory
from .types import Primitive, Target

_log = logging.getLogger(__name__)

_DEFAULT_CONSTRUCTOR_FACTORY: Final[Factory] = Factory()

_T_co = TypeVar("_T_co", covariant=True)


@overload
def structure(
    data: Primitive,
    *,
    into: Target[_T_co],
    coerce_strings: bool = False,
    context: Optional[Mapping[str, object]] = None
) -> _T_co:
    # This overload is required to provide the correct return type for types
    # that are considered valid values of Type[T] (for some T) by mypy.
    ...  # pragma: no cover


@overload
def structure(
    data: Primitive,
    *,
    into: Any,
    coerce_strings: bool = False,
    context: Optional[Mapping[str, object]] = None
) -> Any:
    # This overload is required as 'typing' types, such as Tuple[int],
    # are not considered by mypy to be valid values of Type[T] for any T.
    ...  # pragma: no cover


def structure(
    data: Primitive,
    *,
    into: Target[Any],
    coerce_strings: bool = False,
    context: Optional[Mapping[str, object]] = None
) -> Any:
    """
    Construct a primitive into an instance of the specified target type.

    :param data: Primitive value from which to construct an instance of the
        target type.
    :param into: Target type.
    :param coerce_strings: If set, attempt to convert :python:`str` values to
        :python:`bool`, :python:`int`, or :python:`float` where a value of one
        of these types is required.

        >>> structure("1", into=int)
        Traceback (most recent call last):
            ...
        terramare.errors.ConstructorError: ...
        >>> structure("1", into=int, coerce_strings=True)
        1

        Note that setting this option will cause :python:`terramare` to reject
        non-string primitives where a :python:`bool`, :python:`int`, or :python:`float`
        is required.
        For example:

        >>> structure(1, into=int)
        1
        >>> structure(1, into=int, coerce_strings=True)
        Traceback (most recent call last):
            ...
        terramare.errors.ConstructorError: ...

        This option defaults to :python:`False`.

        :raises: :exc:`terramare.errors.FactoryError`: If a constructor for the
            target type cannot be created.
        :raises: :exc:`terramare.errors.ConstructorError`: If the primitive
            value has an incorrect type, incorrect structure, or fails value-
            level validation.
    """
    _log.debug("Using global default constructor factory")
    return _DEFAULT_CONSTRUCTOR_FACTORY.structure(
        data, into=into, coerce_strings=coerce_strings, context=context
    )
