"""Cache module - Abstract class implementing the generic, non stoarge dependent, functionality"""
from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Optional, Callable, Sequence, Union

from .logger import logger
from .utils import identity_encode_fn, KeyEncodeFnType, ValueFnType, ValueType, EncodedKeyType, KeyType

class Cache(ABC):
    """
    Cache generic implementation

    Parameters:
    name: The name of the cache
    key_encode_fn: A function that encodes the key into a unique identifiable (hashed) key item
    clash_exception: If a key encode fn computes a duplicated key and this is set to true, it'll trigger an exception
    """
    def __init__(self, name: str, key_encode_fn: KeyEncodeFnType = None, clash_exception: bool = False):
        if key_encode_fn is None:
            key_encode_fn = identity_encode_fn
        self.name = name
        self.key_encode_fn = key_encode_fn
        self.clash_exception = clash_exception

    @abstractmethod
    def _set_value(self, encoded_key: EncodedKeyType, value: ValueType):
        """Adds the key to the cache after a value was computed. Stores f(key)=value."""

    @abstractmethod
    def _get(self, encoded_key: EncodedKeyType) -> Optional[ValueType]:
        """Gets this key from the cache"""

    @abstractmethod
    def _check(self, encoded_key: EncodedKeyType) -> bool:
        """Checks if this key is in the cache"""

    def map(self, fn: ValueFnType, seq: Sequence[KeyType]) -> Sequence[ValueType]:
        """Populates this map from a sequence and returns the values"""
        def f(item, self, fn):
            # Add a lambda here. This is such that fn(item) is not evaluated, if key_fn(item) is already in the cache
            self[item] = lambda item: fn(item) # pylint: disable=unnecessary-lambda
            return self[item]
        return [f(item, self, fn) for item in seq]

    def __setitem__(self, key: KeyType, value: Union[ValueType, ValueFnType]):
        encoded_key: EncodedKeyType = self.key_encode_fn(key)
        # Compute key here to avoid computing it twice and call underlying _check function
        if self._check(encoded_key):
            if self.clash_exception:
                raise KeyError(f"Key {key} already exists. Set clash_exists to False if you don't care about clashes.")
            logger.debug2(f"Key {key} clash! Cache will not be updated.")
            return

        # value can be both a lazy call as well as an already resolved value. If not resolved, this is where we do it.
        resolved_value: ValueType = value(key) if isinstance(value, Callable) else value
        self._set_value(encoded_key, resolved_value)

    def __getitem__(self, key: KeyType) -> ValueType:
        encoded_key: EncodedKeyType = self.key_encode_fn(key)
        return self._get(encoded_key)

    def __contains__(self, key: KeyType) -> bool:
        encoded_key: EncodedKeyType = self.key_encode_fn(key)
        return self._check(encoded_key)
