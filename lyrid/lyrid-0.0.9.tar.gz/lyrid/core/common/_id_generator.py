from abc import abstractmethod
from typing import Protocol


class IdGenerator(Protocol):

    @abstractmethod
    def generate(self) -> str:
        pass
