from abc import ABC, abstractmethod
from typing import Awaitable, Generic, TypeVar


T = TypeVar("T")


class AsyncCommand(ABC, Generic[T]):
    @abstractmethod
    async def execute(self) -> Awaitable[T]:
        raise NotImplementedError


class Command(ABC, Generic[T]):
    @abstractmethod
    def execute(self) -> T:
        raise NotImplementedError
