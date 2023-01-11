"""CacheFunctionCall internal module. Used by cache_fn decorator."""
from __future__ import annotations
from typing import Callable, Any
from ..cache import Cache, KeyType, EncodedKeyType, ValueType

class CacheFunctionCall:
    """CacheFunctionCall implementation"""
    def __init__(self, base_cache: Cache, fn: Callable):
        self.base_cache = base_cache
        self.fn = fn

    def set(self, value: ValueType, *args, **kwargs):
        """Set the value in the base cache"""
        value = (value, ) if not isinstance(value, tuple) else value
        encoded_key: EncodedKeyType = self.encode(value, *args, **kwargs)
        if self.check(encoded_key):
            return
        value: ValueType = self.fn(*value, *args, **kwargs)
        self.base_cache._set_value(encoded_key, value) # pylint: disable=protected-access

    def get(self, encoded_key: EncodedKeyType) -> ValueType:
        """Get the value from the base cache"""
        return self.base_cache._get(encoded_key) # pylint: disable=protected-access

    def check(self, encoded_key: EncodedKeyType) -> bool:
        """Check value in the base cache"""
        return self.base_cache._check(encoded_key) # pylint: disable=protected-access

    def encode(self, key: KeyType, *args, **kwargs) -> EncodedKeyType:
        """encode value in the base cache"""
        key = (key, ) if not isinstance(key, tuple) else key
        return self.base_cache.key_encode_fn(*key, *args, **kwargs)

    def __getitem__(self, key: KeyType):
        return self.base_cache[key]

    def __setattr__(self, key: KeyType, value: Any):
        if key in ("base_cache", "fn", "overwrite"):
            super().__setattr__(key, value)
            return
        raise ValueError("Cannot call setattr on this class. Use cache.set(key).")

    def __contains__(self, key: KeyType):
        return key in self.base_cache
