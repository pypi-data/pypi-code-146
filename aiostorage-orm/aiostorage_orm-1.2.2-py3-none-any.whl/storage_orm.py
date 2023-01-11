from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Any, Union

from .storage_item import StorageItem
from .storage_frame import StorageFrame
from .operation_result import OperationResult


class StorageORM(metaclass=ABCMeta):
    _db_instance: Any

    @abstractmethod
    def __init__(
        self,
        client: Any = None,
        host: Union[str, None] = None,
        port: int = 6379,
        db: int = 0,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, item) -> OperationResult:
        raise NotImplementedError

    @abstractmethod
    async def bulk_create(self, items: list) -> OperationResult:
        raise NotImplementedError

    @abstractmethod
    async def bulk_delete(self, items: list) -> OperationResult:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item) -> OperationResult:
        raise NotImplementedError

    @abstractproperty
    def frame(self) -> StorageFrame:
        raise NotImplementedError
