import datetime
import re

import orjson as json
import redis

from gdshoplib.core.settings import CacheSettings


class BaseCache:
    @classmethod
    def get_class(cls, key):
        for _class in cls.__subclasses__():
            if _class.__name__ == key:
                return _class
        return DumpCache


class KeyDBCache(BaseCache):
    CONNECT = None

    def __init__(self, namespace=None):
        self.settings = CacheSettings()
        self.namespace = namespace or self.settings.CACHE_HSTORE
        self.system_namespace = self.settings.CACHE_SYSTEM_HSTORE

    @staticmethod
    def update_time_key(id, /, type):
        return f"{type}:{id}_update_time"

    def get_update_time(self, id, /, type):
        value = self.connect.hget(
            self.settings.CACHE_SYSTEM_HSTORE, self.update_time_key(id, type)
        )
        if value:
            return json.loads(value)

    def set_update_time(self, id, /, type):
        now = datetime.datetime.now()
        content = json.dumps(now)
        self.connect.hset(
            self.settings.CACHE_SYSTEM_HSTORE, self.update_time_key(id, type), content
        )

    def clean_system_cache(self):
        self.connect.delete(self.settings.CACHE_SYSTEM_HSTORE)

    @property
    def connect(self):
        if not self.CONNECT:
            self.CONNECT = redis.Redis.from_url(self.settings.CACHE_DSN)
        return self.CONNECT

    def get(self, key, default=None):
        return self[key] or default

    def __getitem__(self, key):
        value = self.connect.hget(self.settings.CACHE_HSTORE, key)
        if value:
            return json.loads(value)

    def __setitem__(self, key, value):
        content = value if isinstance(value, bytes) else json.dumps(value)
        self.connect.hset(self.settings.CACHE_HSTORE, key, content)

    def count(self):
        return self.connect.hlen(self.settings.CACHE_HSTORE)

    def delete(self, key):
        self.connect.hdel(self.settings.CACHE_HSTORE, key)

    def exists(self, key):
        return self.connect.hexists(self.settings.CACHE_HSTORE, key)

    def search(self, pattern):
        result = []
        for k in self.connect.hkeys(self.settings.CACHE_HSTORE):
            if re.match(pattern, k.decode("utf-8")):
                result.append(k.decode("utf-8"))
        return result

    def clean(self, pattern=r"*"):
        for key in self.search(pattern):
            self.delete(key)


class DumpCache(BaseCache):
    CACHE = {}

    def __init__(self, *args, dsn, cache_period):
        self.cache_period = cache_period

    def get(self, *args, **kwargs):
        return self.CACHE.get(*args, **kwargs)

    def __getitem__(self, key):
        cached = self.CACHE.get(key)
        if cached and cached["time"] > datetime.datetime.now():
            return self.CACHE[key]["data"]

    def __setitem__(self, key, value):
        self.CACHE[key] = {
            "data": value,
            "time": datetime.datetime.now()
            + datetime.timedelta(seconds=self.cache_period),
        }
