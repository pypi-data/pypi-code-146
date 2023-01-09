import asyncio
import typing
from functools import cached_property
import uuid

from dip.pool import ConnectionPool
from dip import errors


DEFAULT_UUID = uuid.UUID('00000000-0000-0000-0000-00000dee9f03')


class Client:
    shared_pool: typing.Dict[int, ConnectionPool] = {}

    def __init__(
        self,
        sockname: str,
        id: typing.Union[str, uuid.UUID] = DEFAULT_UUID,
        loop: asyncio.BaseEventLoop = None,
        use_shared_pool: bool = True,
        pool_size: int = 16,
        **conn_options,
    ):
        if isinstance(id, str):
            self._id = uuid.UUID(id)
        else:
            self._id = id
        self._sockname = sockname
        self._loop = loop or asyncio.get_running_loop()
        self._use_shared_pool = use_shared_pool
        self._pool_size = pool_size
        self._conn_opts = conn_options
        self._inited = False

    @cached_property
    def _pool_key(self):
        return (self._id, id(self._loop))

    @cached_property
    def pool(self) -> ConnectionPool:
        self._inited = True
        if self._use_shared_pool:
            shared_pool = self.__class__.shared_pool
            if (pool := shared_pool.get(self._pool_key)) is None:
                pool = self._new_connection_pool()
                shared_pool[self._pool_key] = pool
            return pool
        else:
            return self._new_connection_pool()

    def _new_connection_pool(self):
        return ConnectionPool(
            self._sockname,
            self._loop,
            maxsize=self._pool_size,
            connection_id=self._id,
            **self._conn_opts
        )

    async def send_msg(self, mtype: str, message: typing.Any):
        """向服务端发送数据"""
        async with self.pool() as conn:
            r = await conn.request(mtype, message)
            if r != b'ok':
                raise errors.ResponseError(f"Server respond with: {r.decode()}")

    async def send_json(self, json_obj: typing.Any):
        """发送json数据"""
        await self.send_msg('J', json_obj)

    async def send_obj(self, obj: typing.Any):
        """发送任意python对象（使用pickle）"""
        await self.send_msg('P', obj)

    def quit(self):
        if self._inited:
            self.pool.dispose()
            self._inited = False
            if self._use_shared_pool:
                self.shared_pool.pop(self._pool_key, None)

    close = quit
