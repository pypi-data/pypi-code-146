import logging
import redis.asyncio as redis
from redis.asyncio.sentinel import Sentinel
from redis.exceptions import ReadOnlyError, ConnectionError
import traceback
import time


class AsyncRedisManager:
    def __new__(cls, is_sentinel: bool = False, sentinel_host_and_port: str = None, sentinel_master_name: str = "mymaster", single_host: str = None, single_port: int = None, redis_passwd: str = None):
        if not hasattr(cls, "instance"):
            cls.instance = super(AsyncRedisManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, is_sentinel: bool = False, sentinel_host_and_port: str = None, sentinel_master_name: str = "mymaster", single_host: str = None, single_port: int = None, redis_passwd: str = None):
        self.is_sentinel = is_sentinel
        self.sentinel_host_and_port = sentinel_host_and_port
        self.sentinel_master_name = sentinel_master_name
        self.redis_passwd = redis_passwd
        self.single_host = single_host
        self.single_port = single_port
        self.reconnect_function = None
        self.redis_client = None
        self.reconnect = False

        if self.is_sentinel:
            if None in (self.sentinel_host_and_port, self.sentinel_master_name):
                raise Exception(f"redis sentinel 정보를 확인 바랍니다. host: {self.sentinel_host_and_port}, masterName: {self.sentinel_master_name}, passwd: {self.sentinel_passwd}")
            self.reconnect_function = self._connect_sentinel_master
        else:
            if None in (self.single_host, self.single_port):
                raise Exception(f"redis(single) 정보를 확인 바랍니다. host: {self.single_host}, port: {self.single_port}, password: {self.single_passwd}")
            self.reconnect_function = self._connect_single

        self.reconnect_function()

    def _reconnect_redis_master(self):
        if self.reconnect == False:
            self.reconnect = True
            time.sleep(2.5)
            self.reconnect_function()
            self.reconnect = False
        else:
            time.sleep(3)

    def _connect_sentinel_master(self):
        """
        connect redis sentinel

        @param sentinelHostAndPort: ex) 172.21.112.61:26379,172.21.115.40:26379,172.21.115.46:26379
        """
        host_port_list = self._make_host_and_port_tuples(self.sentinel_host_and_port)
        sentinel = Sentinel(
            host_port_list,
            sentinel_kwargs={
                "password": self.redis_passwd,
                "charset": "utf-8",
                "decode_responses": True,
            },
            password=self.redis_passwd,
            charset="utf-8",
            decode_responses=True,
        )

        # self.redis_client = sentinel.master_for(self.sentinel_master_name)
        # logging.info(f"redis_client: {self.redis_client}")

        logging.debug(f"sentinel.sentinels: {sentinel.sentinels}")

        for sentinel_no, sentinel_obj in enumerate(sentinel.sentinels):
            try:
                logging.debug(f"sentinel_obj: {sentinel_obj}")
                masters = sentinel_obj.sentinel_masters()
                logging.debug(f"redis masters: {masters}")
            except (ConnectionError, TimeoutError):
                logging.warn(traceback.format_exc())
                continue

        host, port = sentinel.discover_master(self.sentinel_master_name)
        self.redis_client = redis.StrictRedis(
            host=host,
            port=port,
            encoding="utf-8",
            password=self.redis_passwd,
            decode_responses=True,
        )
        logging.info(f"redis_client: {self.redis_client}")
        logging.info(f"connect redis sentinel master: {host}:{port}")
        self.redis_client.pipeline()

    def _connect_single(self):
        """
        connect redis single
        """
        pool = redis.ConnectionPool(max_connections=10, host=self.single_host, port=self.single_port, db=0)
        self.redis_client = redis.Redis(connection_pool=pool, encoding="utf-8", decode_responses=True, password=self.redis_passwd)
        logging.info(f"connect redis single: {self.single_host}:{self.single_port}")

    def _make_host_and_port_tuples(self, host_and_port):
        host_port_list = []
        csv_list = host_and_port.split(",", -1)
        for host_port in csv_list:
            hosts = host_port.split(":", -1)
            host_port_list.append((hosts[0], int(hosts[1])))

        return host_port_list


__client__: AsyncRedisManager = None


def init(is_sentinel: bool = False, sentinel_host_and_port: str = None, sentinel_master_name: str = None, single_host: str = None, single_port: int = None, redis_passwd: str = None) -> AsyncRedisManager:
    global __client__
    if __client__ is None:
        __client__ = AsyncRedisManager(is_sentinel=is_sentinel, sentinel_host_and_port=sentinel_host_and_port, sentinel_master_name=sentinel_master_name, single_host=single_host, single_port=single_port, redis_passwd=redis_passwd)
    return __client__


async def set_ttl(key, value, seconds):
    try:
        return await __client__.redis_client.setex(key, seconds, value)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await set_ttl(key, value, seconds)


async def get_ttl(key):
    try:
        return await __client__.redis_client.ttl(key)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await get_ttl(key)


async def set(key, value):
    try:
        return await __client__.redis_client.set(key, value)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await set(key)


async def get(key):
    try:
        return _convert_to_string_from_bytes(await __client__.redis_client.get(key))
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await get(key)


async def delete(*key):
    try:
        return await __client__.redis_client.delete(*key)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await delete(*key)


async def hset(hash_name, key, value):
    try:
        return await __client__.redis_client.hset(hash_name, key, value)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hset(hash_name, key, value)


async def hget(hash_name, key):
    try:
        return _convert_to_string_from_bytes(await __client__.redis_client.hget(hash_name, key))
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hget(hash_name, key)


async def hdel(hash_name, key):
    try:
        return await __client__.redis_client.hdel(hash_name, key)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hdel(hash_name, key)


async def hgetall(hash_name):
    try:
        return _convert_to_string_from_bytes(await __client__.redis_client.hgetall(hash_name))
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hgetall(hash_name)


async def hincr_by(hash_name, key, amount=1):
    try:
        return await __client__.redis_client.hincrby(hash_name, key, amount=amount)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hincr_by(hash_name, key, amount)


async def hincr_by_float(hash_name, key, amount=1.0):
    try:
        return await __client__.redis_client.hincrbyfloat(hash_name, key, amount=amount)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hincr_by_float(hash_name, key, amount)


async def lpush(key, *values):
    try:
        return await __client__.redis_client.lpush(key, *values)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await lpush(key, *values)


async def rpush(key, *values):
    try:
        return await __client__.redis_client.rpush(key, *values)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await rpush(key, *values)


async def blpop(keys, timeout=None):
    """
    blpop 사용시 timeout을 이용하여 graceful shutdown 구현이 필요함
    timeout이 없을 경우 blpop 무한 대기 중에 pop을 해버릴 가능성이 있음
    redis connection을 다 끊어버리면 현재 동작중인 작업에 문제가 있을 수 있음
    """
    try:
        pop_data = await __client__.redis_client.blpop(keys, timeout=timeout)
        if pop_data is None:
            return None
        return _convert_to_string_from_bytes(pop_data[1])
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await blpop(keys, timeout)


async def lpop(key, count=None):
    try:
        return _convert_to_string_from_bytes(await __client__.redis_client.lpop(key, count))
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await lpop(key)


async def brpop(keys, timeout=None):
    """
    brpop 사용시 timeout을 이용하여 graceful shutdown 구현이 필요함
    timeout이 없을 경우 brpop 무한 대기 중에 pop을 해버릴 가능성이 있음
    redis connection을 다 끊어버리면 현재 동작중인 작업에 문제가 있을 수 있음
    """
    try:
        pop_data = await __client__.redis_client.brpop(keys, timeout=timeout)
        if pop_data is None:
            return None
        return _convert_to_string_from_bytes(pop_data[1])
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await brpop(keys, timeout)


async def rpop(key, count=None):
    try:
        return _convert_to_string_from_bytes(await __client__.redis_client.rpop(key, count))
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await rpop(key)


async def llen(key):
    try:
        return await __client__.redis_client.llen(key)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await llen(key)


async def expire(key, seconds=1):
    try:
        return await __client__.redis_client.expire(key, seconds)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await expire(key, seconds)


async def incr(key, amount=1):
    try:
        return await __client__.redis_client.incr(key, amount)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await incr(key)


async def incr_and_expire(key, seconds=1):
    count = await incr(key)
    if 1 == count:
        await expire(key, seconds)
    return count


async def incr_and_expire_duplicate(key, seconds=1):
    count = await incr(key)
    await expire(key, seconds)
    return count


async def keys(key="*"):
    try:
        return _convert_to_string_from_bytes(await __client__.redis_client.keys(key))
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await keys(key)


async def hscan(key, cursor: int, matcher: str, count=100000):
    try:
        return await __client__.redis_client.hscan(key, cursor, match=f"{matcher}", count=count)
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await hscan(key, matcher, count)


async def lrange(key, start: int, end: int) -> list:
    try:
        result = await __client__.redis_client.lrange(key, start, end)
        # return list(map(lambda x: x.decode(), result))
        return result
    except (ReadOnlyError, ConnectionError):
        logging.warn(traceback.format_exc())
        __client__._reconnect_redis_master()
        return await lrange(key, start, end)


def _convert_to_string_from_bytes(data):
    if data is None:
        return None
    if isinstance(data, bytes):
        return data.decode()
    elif isinstance(data, dict):
        return _decode_dict(data)
    elif isinstance(data, list):
        return _decode_list(data)
    return data


def _decode_dict(data: dict):
    result = {}
    for d in data.items():
        key = d[0]
        value = d[1]
        if isinstance(key, bytes):
            key = key.decode()
        if isinstance(value, bytes):
            value = value.decode()
        result[key] = value
    return result


def _decode_list(data: list):
    result = []
    for d in data:
        if isinstance(d, bytes):
            d = d.decode()
        result.append(d)

    return result
