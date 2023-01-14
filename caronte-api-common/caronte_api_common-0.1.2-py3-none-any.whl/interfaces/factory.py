from abc import ABC, abstractmethod
from typing import Awaitable, Generic, TypeVar


Tr = TypeVar("Tr")
Tp = TypeVar("Tp")


class AsyncFactory(ABC, Generic[Tr, Tp]):
    @abstractmethod
    async def manufacture(self, object_key: Tp) -> Awaitable[Tr]:
        raise NotImplementedError


class Factory(ABC, Generic[Tr, Tp]):
    @abstractmethod
    def manufacture(self, object_key: Tp) -> Tr:
        raise NotImplementedError
