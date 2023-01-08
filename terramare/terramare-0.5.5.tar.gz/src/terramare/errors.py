"""Common error types."""

from dataclasses import dataclass
from typing import Tuple


class TerramareError(Exception):
    """Base class for all exceptions raised by terramare."""


@dataclass(frozen=True)
class ConstructorError(TerramareError):
    """Raised when failing to construct an instance of a class from a primitive value."""

    summary: str
    detail: str = ""
    _depth: Tuple[int, int] = (0, 0)

    def __str__(self) -> str:
        return f"{self.summary}\n{self.detail}"

    def __lt__(self, other: "ConstructorError") -> bool:
        return self._depth < other._depth


class ContextTypeError(TerramareError, TypeError):
    """Raised when required context is missing."""


class ValidationException(TerramareError):
    """Base class for field validation errors automatically caught by terramare."""


@dataclass(frozen=True)
class FactoryError(TerramareError):
    """Raised when failing to create a constructor for a type."""

    message: str


@dataclass(frozen=True)
class InternalError(TerramareError):
    """Raised on unexpected internal errors."""

    message: str

    def __str__(self) -> str:  # pragma: no cover
        return f"an internal error occured: {self.message}"


@dataclass(frozen=True)
class UnsupportedTargetTypeError(TerramareError):
    """Raised when a factory is called with a target type it does not support."""
