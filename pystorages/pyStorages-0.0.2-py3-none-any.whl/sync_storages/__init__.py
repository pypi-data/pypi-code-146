from typing import Optional, Union

from storages.types import StorageType

from storages.sync_storages.pickle_storage import PickleStorage
from storages.sync_storages.json_storage import JSONStorage
from storages.sync_storages.redis_storage import RedisStorage


def load_storage(storage_type: StorageType,
                 file_path: Optional[str] = None,
                 redis_url: Optional[str] = None,
                 redis_data_key: Optional[str] = None):
    storage = {
        StorageType.PICKLE: PickleStorage,
        StorageType.JSON: JSONStorage,
        StorageType.REDIS: RedisStorage,
    }
    if storage_type in [StorageType.PICKLE, StorageType.JSON]:
        return storage[storage_type](file_path)
    elif storage_type == StorageType.REDIS:
        return storage[storage_type](redis_url, redis_data_key)


Storage = Union[
    PickleStorage, JSONStorage, RedisStorage
]

__all__ = (
    "PickleStorage",
    "JSONStorage",
    "RedisStorage",
    "Storage",
    "load_storage",
)
