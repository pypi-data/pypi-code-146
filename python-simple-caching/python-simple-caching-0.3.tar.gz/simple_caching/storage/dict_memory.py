"""Dict memory module. Caches data in the memory in a dictionary."""
from typing import Optional
from overrides import overrides

from ..cache import Cache, EncodedKeyType, ValueType

class DictMemory(Cache):
    """DictMemory implementation"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cache = {}

    @overrides
    def _set_value(self, encoded_key: EncodedKeyType, value: ValueType):
        self.cache[encoded_key] = value

    @overrides
    def _get(self, encoded_key: EncodedKeyType) -> Optional[ValueType]:
        return self.cache[encoded_key]

    @overrides
    def _check(self, encoded_key: EncodedKeyType) -> bool:
        return encoded_key in self.cache

    def __str__(self) -> str:
        f_str = "[DictMemory]"
        f_str += f" - Num top level keys: {len(self.cache.keys())}"
        return f_str

    def __repr__(self) -> str:
        return self.__str__()
