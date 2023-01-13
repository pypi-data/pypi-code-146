import logging
from typing import Union
from typing import TypeVar

import redis.asyncio as redis
from redis.asyncio.client import Pipeline

from .aioredis_frame import AIORedisFrame
from .aioredis_item import AIORedisItem
from .aioredis_item import T as SubclassItemType
from ..operation_result import OperationResult
from ..operation_result import OperationStatus

from ..aiostorage_orm import AIOStorageORM

ChildItem = TypeVar('ChildItem', bound=AIORedisItem)


class AIORedisORM(AIOStorageORM):
    """ Работа с БД Redis через объектное представление """
    _pipe: Pipeline
    _client: redis.Redis
    _frame: AIORedisFrame

    def __init__(
        self,
        client: Union[redis.Redis, None] = None,
        host: Union[str, None] = None,
        port: int = 6379,
        db: int = 0,
    ) -> None:
        if client:
            self._client = client
        elif host:
            self._client = redis.Redis(host=host, port=port, db=db)
        else:
            raise Exception("AIOStorageORM-init must contains redis_client or host values...")

        self._pipe = self._client.pipeline()
        if not AIORedisItem._db_instance:
            AIORedisItem._set_global_instance(db_instance=self._client)

        self._frame = AIORedisFrame(client=self._client)

    @property
    def frame(self) -> AIORedisFrame:
        """ Подготовленный frame для работы со списками значений """
        return self._frame

    async def save(self, item: AIORedisItem) -> OperationResult:
        """ Одиночная вставка """
        return await item.save()

    async def bulk_create(self, items: list[SubclassItemType]) -> OperationResult:
        """ Групповая вставка """
        try:
            if hasattr(items[0], "_ttl") and items[0]._ttl:
                for redis_item in items:
                    for key, value in redis_item.mapping.items():
                        self._pipe.set(name=key, value=value, ex=redis_item._ttl)
            else:
                for redis_item in items:
                    self._pipe.mset(mapping=redis_item.mapping)
            await self._pipe.execute()
            return OperationResult(status=OperationStatus.success)
        except Exception as exception:
            self._on_error_actions(exception=exception)
            return OperationResult(
                status=OperationStatus.failed,
                message=str(exception),
            )

    async def bulk_delete(self, items: list[ChildItem]) -> OperationResult:
        """
            Удаление списка элементов
        """
        try:
            for redis_item in items:
                self._pipe.delete(*[key for key in redis_item.mapping.keys()])
            await self._pipe.execute()
            return OperationResult(status=OperationStatus.success)
        except Exception as exception:
            self._on_error_actions(exception=exception)
            return OperationResult(
                status=OperationStatus.failed,
                message=str(exception),
            )

    async def delete(self, item: AIORedisItem) -> OperationResult:
        """
            Удаление одного элемента
        """
        return await item.delete()

    def _on_error_actions(self, exception: Exception) -> None:
        """
            Действия, выполняющиеся в случае возникновения исключения
                во время вставки, сохранения, получения данных из БД
        """
        logging.exception(exception)
