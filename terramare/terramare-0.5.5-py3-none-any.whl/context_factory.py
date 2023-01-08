"""Factory preventing deserialization of Context type."""

from dataclasses import dataclass
from typing import NoReturn

from typing_extensions import final

from .core import FactoryCore, InternalFactory
from .data import Context
from .errors import UnsupportedTargetTypeError
from .types import Target


@final
@dataclass(frozen=True)
class ContextFactory(FactoryCore):
    def create_constructor(
        self, factory: InternalFactory, target: Target[object]
    ) -> NoReturn:
        if not (isinstance(target, type) and issubclass(target, Context)):
            raise UnsupportedTargetTypeError
        raise factory.make_error(
            "construction explicitly disabled for this type. "
            " You may be using the `Context` type in an incorrect location."
        )
