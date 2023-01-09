from __future__ import annotations

from .data import Variable
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class VariableContainer:
    variables: dict[str, Variable] = field(default_factory=dict)

    def __iter__(self) -> Iterator[str]:
        return iter(self.variables)

    def add(self, variable: Variable) -> None:
        name = variable.name
        if name == "time":
            raise KeyError("'time' is a protected variable for the simulation time")
        if name in self.variables:
            raise KeyError(f"Variable {variable} already exists.")
        self.variables[variable.name] = variable

    def remove(self, variable: str) -> None:
        del self.variables[variable]
