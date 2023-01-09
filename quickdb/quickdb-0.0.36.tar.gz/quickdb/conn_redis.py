"""
    pip install redis
    pip install redis-py-cluster

    RedisConn：创建 redis 连接
    RedisLock：所有使用该锁的都会等待锁，直到获取并执行
    RedisLockNoWait：所有使用该锁的，获取到锁才会执行，获取不到就不执行

    注意：默认锁住的最大时间是 60s，超过则释放

    使用示例：
        with RedisLock(lock_name=""):
            ...

        with RedisLockNoWait(lock_name=") as lock:
            if lock.lock_success:
                ...
"""
import uuid
import redis
import rediscluster


# redis 集群
class RedisClusterConn:
    def __init__(
            self,
            startup_nodes=None,
            pwd: str = None,
            max_connections: int = None,
            pool_kwargs: dict = None,
            conn_kwargs: dict = None
    ):
        pool_kwargs = pool_kwargs or {}
        conn_kwargs = conn_kwargs or {}

        pool = rediscluster.ClusterBlockingConnectionPool(
            startup_nodes=startup_nodes,
            password=pwd,
            max_connections=max_connections,
            **pool_kwargs
        )

        self.conn = rediscluster.RedisCluster(connection_pool=pool, **conn_kwargs)

    def close(self):
        """
        关闭连接

        :return:
        """
        self.conn.close()

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# redis 连接
class RedisConn:
    def __init__(
            self,
            host: str = '127.0.0.1',
            port: int = 6379,
            pwd: str = None,
            db: int = 0,
            pool_kwargs: dict = None,
            conn_kwargs: dict = None
    ):
        pool_kwargs = pool_kwargs or {}
        conn_kwargs = conn_kwargs or {}

        pool = redis.BlockingConnectionPool(
            host=host,
            port=port,
            password=pwd,
            db=db,
            **pool_kwargs
        )

        if 'health_check_interval' not in conn_kwargs:
            conn_kwargs.update({
                'health_check_interval': 10
            })

        self.conn = redis.Redis(connection_pool=pool, decode_responses=True, **conn_kwargs)

    def close(self):
        """
        关闭连接

        :return:
        """
        self.conn.close()

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class RedisConnLazy:
    def __init__(
            self,
            host: str = '127.0.0.1',
            port: int = 6379,
            pwd: str = None,
            pool_kwargs: dict = None,
            conn_kwargs: dict = None
    ):
        self.host = host
        self.port = port
        self.pwd = pwd
        self.pool_kwargs = pool_kwargs or {}
        self.conn_kwargs = conn_kwargs or {}

        self._map = {}

    def conn_to(self, db: int) -> redis.Redis:
        """
        连接到指定 db

        :param db:
        :return:
        """
        if db in self._map:
            return self._map[db]

        pool = redis.BlockingConnectionPool(
            host=self.host,
            port=self.port,
            password=self.pwd,
            db=db,
            **self.pool_kwargs
        )

        if 'health_check_interval' not in self.conn_kwargs:
            self.conn_kwargs.update({
                'health_check_interval': 10
            })

        self._map[db] = redis.Redis(connection_pool=pool, decode_responses=True, **self.conn_kwargs)

        return self._map[db]

    def close(self, db: int) -> None:
        """
        关闭连接

        :param db:
        :return:
        """
        if db in self._map:
            self._map[db].close()

    def close_all(self) -> None:
        """
        关闭所有连接

        :return:
        """
        for db in self._map.keys():
            self.close(db)


# redis 等待锁
class RedisLock:
    def __init__(
            self,
            conn,
            lock_name: str,
            block_timeout: int = None,
            wait_timeout: int = None,
            frequency: float = None,
            drop_release_error: bool = False
    ):
        """

        :param conn: redis 连接
        :param lock_name: 锁的名字
        :param block_timeout: 锁住的最大时间
        :param wait_timeout: 等待锁的最大时间
        :param frequency: 检查锁的频率
        :param drop_release_error: 释放锁报错是否抛出
        """
        self._conn = conn
        self._lock_name = lock_name
        self._block_timeout = block_timeout or 60
        self._wait_timeout = wait_timeout
        self._frequency = frequency or 0.1
        self._drop_release_error = drop_release_error

        self._lock = self._conn.lock(
            name=self._lock_name,
            timeout=self._block_timeout,
            blocking_timeout=self._wait_timeout,
            sleep=self._frequency
        )

    def acquire(self):
        """
        获取锁

        :return:
        """
        return self._lock.acquire()

    def release(self):
        """
        释放锁

        :return:
        """
        try:
            return self._lock.release()
        except:
            if self._drop_release_error:
                raise

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


# redis 不等待锁
class RedisLockNoWait:
    def __init__(
            self,
            conn,
            lock_name: str,
            block_timeout: int = None,
            auto_lock: bool = True,
    ):
        """

        :param conn: redis 连接
        :param lock_name: 锁的名字
        :param block_timeout: 锁住的最大时间
        :param auto_lock: 是否 with 时自动上锁
        """
        self._conn = conn
        self._lock_name = lock_name
        self._block_timeout = block_timeout or 60
        self._auto_lock = auto_lock

        self.lock_success = False  # 是否成功上锁
        self._token = uuid.uuid1().hex.encode()  # 生成的 token 是 byte

    def acquire(self) -> bool:
        """
        获取锁

        :return:
        """

        self.lock_success = bool(self._conn.set(
            name=self._lock_name,
            value=self._token,
            nx=True,
            ex=self._block_timeout
        ))

        return self.lock_success

    def release(self) -> bool:
        """
        释放锁

        :return:
        """
        token = self._conn.get(self._lock_name)
        if token is None:
            return True

        if token == self._token:
            return bool(self._conn.delete(self._lock_name))

        return False

    def exists(self) -> bool:
        """
        是否含有锁

        :return:
        """
        return bool(self._conn.exists(self._lock_name))

    def __enter__(self):
        self._auto_lock and self.acquire()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock_success and self.release()
