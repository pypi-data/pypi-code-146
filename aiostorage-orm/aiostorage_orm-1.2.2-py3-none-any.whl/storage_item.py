from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Any, Type, Union

from storage_orm.operation_result import OperationResult


class StorageItem(metaclass=ABCMeta):
    """
        Базовая модель для объекта БД
        - Для создания модели на основе текущей, необходимо определить класс
          конфигурации Meta и создать поля объекта, например:

            class MyModel(StorageItem):
                date_time: float
                any_value: int

                class Meta:
                    table = "subsystem.{subsystem_id}.tag.{tag_id}"
                    ttl = 3600  # sec, default None
    """

    @classmethod
    @abstractmethod
    async def get(cls, _item, **kwargs) -> Union[StorageItem, None]:
        """
            Получение одного объекта по выбранному фильтру

                StorageItem.get(subsystem_id=10, tag_id=55)
                StorageItem.get(_item=StorageItem(subsystem_id=10))
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def filter(cls, _items, **kwargs) -> list:
        """
            Получение объектов по фильтру переданных аргументов, например:

                StorageItem.filter(subsystem_id=10, tag_id=55)
                StorageItem.filter(_items=[StorageItem(subsystem_id=10), ...])
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def using(cls, db_instance) -> StorageItem:
        """
            Выполнение операций с БД путём direct-указания используемого
            подключения, например:

                another_client: redis.Redis = redis.Redis(host="8.8.8.8", db=12)
                StorageItem.using(db_instance=another_client).get(subsystem_id=10)
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self) -> OperationResult:
        """
            Одиночная вставка
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> OperationResult:
        """
            Удаление одного элемента
        """
        raise NotImplementedError

    @abstractmethod
    def set_ttl(self, new_ttl) -> None:
        """ Установка настройки времени жизни объекта 'на лету' """
        raise NotImplementedError

    @abstractmethod
    def set_frame_size(self, new_frame_size) -> None:
        """ Установка настройки максимального размера frame'а 'на лету' """
        raise NotImplementedError
