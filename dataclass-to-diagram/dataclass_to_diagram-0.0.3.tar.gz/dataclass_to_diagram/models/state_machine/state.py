"""Классы для описания диаграммы состояний."""

from dataclasses import dataclass, field
from typing import Iterable, Literal, Self

from ..alias_generator import AliasFenerator
from ..base_model import BaseModel


@dataclass(frozen=True)
class State(object):
    """Состояние."""

    alias: int = field(init=False, default_factory=AliasFenerator().new_alias)
    name: str
    internal_states: Iterable[Self] | None = None
    description: str | None = None

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False
        return self.name == other.name


@dataclass(frozen=True)
class StateStart(State):
    name: str = field(init=False, default="")
    internal_states: None = field(init=False, default=None)
    description: None = field(init=False)


@dataclass(frozen=True)
class StateEnd(State):
    name: str = field(init=False, default="")
    internal_states: None = field(init=False, default=None)
    description: None = field(init=False)


@dataclass(frozen=True)
class StateFork(State):
    name: str = field(init=False, default="")
    internal_states: None = field(init=False, default=None)
    description: None = field(init=False)


@dataclass(frozen=True)
class StateJoin(State):
    name: str = field(init=False, default="")
    internal_states: None = field(init=False, default=None)
    description: None = field(init=False)


@dataclass(frozen=True)
class StateChoice(State):
    name: str = field(init=False, default="")
    internal_states: None = field(init=False, default=None)
    description: None = field(init=False)


@dataclass(frozen=True)
class Transition(object):
    """Переход между состояниями."""

    begin: State
    end: State
    description: str | None = None
    option: Literal["history", "deep_history"] | None = None


@dataclass(frozen=True)
class Diagram(BaseModel):
    """Диаграмма состояний."""

    states: Iterable[State] | None = None
    transitions: Iterable[Transition] | None = None
    hide_empty_description: bool = False
