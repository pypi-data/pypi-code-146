import json
import atexit
from typing import Optional
from storages.async_storages.base_nosql_storage import BaseNoSQLStorage

redis_installed = True
try:
    import aioredis
except ModuleNotFoundError:
    try:
        from redis import asyncio as aioredis
    except ModuleNotFoundError:
        redis_installed = False


def create_connection_pool(redis_url):
    if not redis_installed:
        raise ModuleNotFoundError("AioRedis is not installed. Install it via 'pip install aioredis'")
    return aioredis.ConnectionPool.from_url(redis_url)


class RedisStorage(BaseNoSQLStorage):
    def __init__(self, redis_url: Optional[str], data_key: Optional[str]):
        super().__init__()
        self.redis = create_connection_pool(redis_url if redis_url is not None else "redis://localhost/")
        self.data_key = data_key if data_key is not None else "data"

        atexit.register(self.dump)

    @classmethod
    async def create(cls, file_path: Optional[str], data_key: Optional[str]):
        obj = cls(file_path, data_key)
        await obj.load()
        return obj

    async def load(self):
        connection = aioredis.Redis(connection_pool=self.redis)
        result = await connection.get(self.data_key)
        await connection.close()
        if result is not None:
            self._data = json.loads(result)

    async def dump(self):
        connection = aioredis.Redis(connection_pool=self.redis)
        await connection.set(self.data_key, json.dumps(self.data))
        await connection.close()
