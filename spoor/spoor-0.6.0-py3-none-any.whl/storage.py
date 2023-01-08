from abc import ABC, abstractmethod
from collections import Counter
from threading import RLock
from typing import List, Tuple


class Storage(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplementedError("Provide implementation")

    @abstractmethod
    def get_name(self, key):
        raise NotImplementedError("Provide implementation")

    @abstractmethod
    def set_name(self, key, name):
        raise NotImplementedError("Provide implementation")

    @abstractmethod
    def inc(self, key):
        raise NotImplementedError("Provide implementation")

    @abstractmethod
    def most_common(self, top_n: int = 3) -> List[Tuple[str, int]]:
        raise NotImplementedError("Provide implementation")


class MemoryStorage(Storage):
    def __init__(self, strict: bool = False):
        self._lock = RLock()
        self._registry = Counter()
        self._names = {}
        self.strict = strict

    def get_value(self, key):
        if self.strict and key not in self._registry:
            raise KeyError(f"{key} not found")
        return self._registry[key]

    def inc(self, key):
        with self._lock:
            self._registry[key] += 1

    def get_name(self, key) -> str:
        if self.strict and key not in self._names:
            raise KeyError(f"{key} not found")
        return self._names.get(key, "")

    def set_name(self, key, name: str):
        self._names[key] = name

    def most_common(self, top_n: int = 3):
        result = []
        for key, value in self._registry.most_common(n=top_n):
            name = self.get_name(key)
            result.append((name, value))
        return result
