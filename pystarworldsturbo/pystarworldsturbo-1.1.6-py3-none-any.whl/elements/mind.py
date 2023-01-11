from typing import Tuple

from ..common.action import Action


class Mind():
    def perceive(self, **_) -> None:
        # Abstract.
        raise NotImplementedError()

    def revise(self) -> None:
        # Abstract.
        raise NotImplementedError()

    def decide(self) -> None:
        # Abstract.
        raise NotImplementedError()

    def execute(self) -> Tuple[Action]:
        # Abstract.
        raise NotImplementedError()
