from typing import Optional, Union

from storages.types import StorageType

from storages.async_storages.pickle_storage import PickleStorage
from storages.async_storages.json_storage import JSONStorage
from storages.async_storages.redis_storage import RedisStorage


async def load_storage(storage_type: StorageType,
                       file_path: Optional[str] = None,
                       redis_url: Optional[str] = None,
                       redis_data_key: Optional[str] = None):
    storage = {
        StorageType.PICKLE: PickleStorage,
        StorageType.JSON: JSONStorage,
        StorageType.REDIS: RedisStorage,
    }
    if storage_type in [StorageType.PICKLE, StorageType.JSON]:
        return await storage[storage_type].create(file_path)
    elif storage_type == StorageType.REDIS:
        return await storage[storage_type].create(redis_url, redis_data_key)


Storage = Union[
    PickleStorage, JSONStorage, RedisStorage,
]

__all__ = (
    "PickleStorage",
    "JSONStorage",
    "RedisStorage",
    "Storage",
    "load_storage",
)
