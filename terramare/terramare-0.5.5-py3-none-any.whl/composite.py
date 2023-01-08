"""Composite factory."""

import logging
from dataclasses import dataclass, field
from typing import Sequence, TypeVar

from typing_extensions import final

from .core import ConstructorCore, FactoryCore, InternalFactory
from .errors import UnsupportedTargetTypeError
from .pretty_printer import print_type_name
from .types import Target

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)


@final
@dataclass(frozen=True)
class CompositeFactory(FactoryCore):
    _factories: Sequence[FactoryCore] = field(default_factory=list)

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> "ConstructorCore[_T_co]":
        for f in self._factories:
            try:
                _log.debug("Attempting to create constructor using factory %s", f)
                constructor = f.create_constructor(factory, target)
                _log.debug("Successfully created constructor using factory %s", f)
                return constructor
            except UnsupportedTargetTypeError:
                _log.debug("Constructor mismatch for factory %s", f)
        raise factory.make_error(
            f"unable to construct type '{print_type_name(target)}'"
        )
