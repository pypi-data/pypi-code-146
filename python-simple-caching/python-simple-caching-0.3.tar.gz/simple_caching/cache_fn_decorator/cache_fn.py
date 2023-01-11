"""cache_fn decorator. Used to cache an entire function with just a decorator and a key_encode_fn"""
from typing import Union, Type, Callable
from functools import partial
from pathlib import Path
import inspect

from .cache_function_call import CacheFunctionCall
from ..cache import Cache, ValueType
from ..logger import logger

class cache_fn:
    """
    For each python file, adds a directory called .simple_cache if used with NpyFS.
    Usage

    @cache_fn(NpyFS, key_encode_fn) or @cache_fn(NpyFS(name, key_encode_fn))
    def f(x):
        ...

    """
    def __init__(self, base_cache: Union[Cache, Type[Cache]], key_encode_fn: Callable = None):
        self.base_cache = base_cache
        self.key_encode_fn = key_encode_fn

    def _lazy_instantiate(self, func: Callable) -> Cache:
        """
        We get the file of the calling function and cache in that particular directory adding a dot as a prefix
        to the fn name.

        i.e.: /path/to/script.py -- function fn => cache dir is /path/to/.script.py/fn/

        """
        func_name = str(func).split(" ")[1]
        func_filename = Path(inspect.getfile(func))
        name = func_filename.parent / f".{func_filename.name}" / func_name
        logger.debug(f"Caching function '{func_filename}/{func_name}' at '{name}'")
        return self.base_cache(name=name, key_encode_fn=self.key_encode_fn)

    @staticmethod
    def inner_fn(items, *args, cache: CacheFunctionCall, **kwargs) -> ValueType:
        """The decorator code"""
        assert isinstance(cache, CacheFunctionCall), f"Got {cache}"
        encoded_key = cache.encode(items, *args, **kwargs)
        if not cache.check(encoded_key):
            logger.debug2("Adding new value to cache")
            cache.set(items, *args, **kwargs)
        returned = cache.get(encoded_key)
        return returned

    def __call__(self, func: Callable):
        self.base_cache = self.base_cache if isinstance(self.base_cache, Cache) else self._lazy_instantiate(func)
        fn_cache = CacheFunctionCall(self.base_cache, fn=func)
        return partial(cache_fn.inner_fn, cache=fn_cache)
