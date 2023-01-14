import threading
from typing import Any, Optional
from weakref import WeakValueDictionary


class CachedManager(WeakValueDictionary):
    """
    永久缓存，需要手动删除
    """
    cache_lock: threading.Lock = threading.Lock()

    def get(self, key: Any) -> Optional[Any]:
        with self.cache_lock:
            if not super(CachedManager, self).get(key):
                data = Cache()
                self.__setitem__(key, data)
            return super(CachedManager, self).get(key)


class Cache(dict):
    _m: CachedManager = CachedManager()

    @classmethod
    def fetch(cls, key: Any):
        return cls._m.get(key)


__all__ = ('Cache',)
