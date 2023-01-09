from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Iterable

logger = logging.getLogger(__name__)


@dataclass
class NameContainer:
    names: dict[str, str] = field(default_factory=dict)

    def add(self, name: str, element_type: str) -> None:
        if (old_type := self.names.get(name)) is not None:
            raise KeyError(f"Cannot add {element_type} {name}, as there already exists a {old_type} with that name.")

        logger.info(f"Adding name {name}")
        self.names[name] = element_type

    def remove(self, name: str) -> None:

        logger.info(f"Removing name {name}")
        del self.names[name]

    def require_multiple(self, names: Iterable[str]) -> None:
        if bool(difference := set(names).difference(self.names)):
            raise KeyError(f"Names '{', '.join(difference)}' are missing.")
