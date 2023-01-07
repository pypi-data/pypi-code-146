import time
from collections import OrderedDict
from dataclasses import dataclass
from threading import RLock
from typing import Any, Optional

# Based on https://github.com/mobilityhouse/ttldict


@dataclass
class TTLItem:
    value: Any
    expire_ts: float


class TTLDict(OrderedDict):
    def __init__(self, default_ttl: float, *args, **kwargs):
        """
        :param default_ttl: Default TTL for items, in seconds.
        """
        self._default_ttl = default_ttl
        self._lock = RLock()
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<default_ttl=%r, items=%r;>" % (self._default_ttl, self.items())

    def __len__(self):
        with self._lock:
            self._purge()
            return super().__len__()

    def __contains__(self, item: Any) -> bool:
        with self._lock:
            if not super().__contains__(item):
                return False
            return not self.is_expired(item)

    def __iter__(self):
        for key in super().__iter__():
            if not self.is_expired(key):
                yield key

    def __getitem__(self, key: Any) -> Any:
        with self._lock:
            if self.is_expired(key):
                self.__delitem__(key)
                raise KeyError
            item: TTLItem = super().__getitem__(key)
            return item.value

    def __setitem__(self, key: Any, value: Any):
        self.set(key=key, value=value, ttl=self._default_ttl)

    def __delitem__(self, key: Any):
        with self._lock:
            super().__delitem__(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def set(self, key: Any, value: Any, ttl: Optional[float] = None):
        if not ttl:
            ttl = self._default_ttl
        with self._lock:
            expire_ts = time.time() + ttl
            ttl_item = TTLItem(value=value, expire_ts=expire_ts)
            super().__setitem__(key, ttl_item)

    def is_expired(self, key: Any, now: Optional[float] = None) -> bool:
        with self._lock:
            if now is None:
                now = time.time()
            ttl_item: TTLItem = super().__getitem__(key)
            return ttl_item.expire_ts < now

    def _purge(self):
        now = time.time()
        all_keys = list(super().keys())
        for key in all_keys:
            if self.is_expired(key, now=now):
                self.__delitem__(key)

    def keys(self):
        for key in super().keys():
            if not self.is_expired(key):
                yield key

    def values(self):
        for key, ttl_item in super().items():
            if not self.is_expired(key):
                yield ttl_item.value

    def items(self):
        for key, ttl_item in super().items():
            if not self.is_expired(key):
                yield key, ttl_item.value

    def double_lock_test(self):
        with self._lock:
            print("1")
            with self._lock:
                print("double lock test")

    # def set_ttl(self, key, ttl: int, now=None):
    #     """Set TTL for the given key"""
    #     if now is None:
    #         now = time.time()
    #     with self._lock:
    #         value = self[key]
    #         super().__setitem__(key, (now + ttl, value))
    #
    # def get_ttl(self, key, now=None):
    #     """Return remaining TTL for a key"""
    #     if now is None:
    #         now = time.time()
    #     with self._lock:
    #         expire, _value = super().__getitem__(key)
    #         return expire - now
    #
    # def expire_at(self, key, timestamp):
    #     """Set the key expire timestamp"""
    #     with self._lock:
    #         value = self.__getitem__(key)
    #         super().__setitem__(key, (timestamp, value))
