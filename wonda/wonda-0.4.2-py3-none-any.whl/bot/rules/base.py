from asyncio import iscoroutinefunction
from typing import Callable, List, Optional, Type, Union

from wonda.bot.rules.abc import ABCRule
from wonda.bot.states.types import BaseStateGroup, get_state_repr
from wonda.bot.updates import BaseBotUpdate


class Function(ABCRule[BaseBotUpdate]):
    """
    A rule that calls a sync/async function to check
    if the update should be handled. It can accept
    any update objects, but always returns a boolean.
    """

    def __init__(self, func: Callable[[BaseBotUpdate], bool]) -> None:
        self.func = func

    async def check(self, update: BaseBotUpdate) -> bool:
        if iscoroutinefunction(self.func):
            return await self.func(update)
        return self.func(update)


class HasAttr(ABCRule[BaseBotUpdate]):
    """
    A rule that checks if the update dataclass
    has the specified attributes at its upper level.
    """

    def __init__(self, attr_names: Union[str, List[str]]) -> None:
        self.attr_names = [attr_names] if isinstance(attr_names, str) else attr_names

    async def check(self, update: BaseBotUpdate) -> bool:
        return all(bool(getattr(update, attr, None)) for attr in self.attr_names)


class State(ABCRule[BaseBotUpdate]):
    def __init__(
        self,
        state: Optional[Union[BaseStateGroup, List[BaseStateGroup]]] = None,
    ):
        if not isinstance(state, list):
            state = [] if state is None else [state]
        self.state = [get_state_repr(s) for s in state]

    async def check(self, update: BaseBotUpdate) -> bool:
        if update.state_repr is None:
            return not self.state
        return update.state_repr.state in self.state


class StateGroup(ABCRule[BaseBotUpdate]):
    def __init__(
        self,
        state_group: Union[Type[BaseStateGroup], List[Type[BaseStateGroup]]],
    ):
        if not isinstance(state_group, list):
            state_group = [] if state_group is None else [state_group]
        self.state_group = [group.__name__ for group in state_group]

    async def check(self, update: BaseBotUpdate) -> bool:
        if update.state_repr is None:
            return not self.state_group

        group_name = update.state_repr.state.split(":", maxsplit=1)[0]
        return group_name in self.state_group
