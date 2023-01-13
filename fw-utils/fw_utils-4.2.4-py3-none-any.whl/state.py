"""Cached application state management."""
import contextlib
import inspect
import os
import threading
import time
import typing as t

__all__ = ["Cached", "TempEnv"]

T = t.TypeVar("T")


class Cached(t.Generic[T]):
    """Descriptor for caching attributes and injecting dependencies."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        func: t.Callable[..., T],
        thread_safe: bool = True,
        fork_safe: bool = False,
        expire_in: int = 0,
    ) -> None:
        """Initialize the cached attribute descriptor.

        Args:
            func: The callable to init the attribute with on access.
            thread_safe: Set to False disable sharing between threads.
            fork_safe: Set to True to enable sharing between processes.
            expire_in: Time in seconds to recreate the object after.
        """
        self.name = ""
        self.func = func
        self.args = list(inspect.signature(func).parameters)
        if self.args and self.args[0] == "self":
            self.args.pop(0)  # pragma: no cover
        self.close = None
        self.thread_safe = thread_safe
        self.fork_safe = fork_safe if thread_safe else False
        # NOTE thread IDs are only unique within the same process
        self.expire_in = expire_in
        self.expire_at = 0

    def __set_name__(self, owner: type, name: str) -> None:
        """Store the descriptor attribute name as defined on the owner class."""
        self.name = name

    def __get__(self, instance, owner: type = None) -> T:
        """Return the initialized attribute (cached)."""
        # accessed as a class attribute - return the descriptor
        if instance is None:
            return self  # type: ignore
        # accessed as an instance attribute - return the attribute
        cache = self.get_cache_dict(instance)
        key = self.get_cache_key()
        # expunge cached instance if it expired
        if key in cache and self.expire_at and time.time() >= self.expire_at:
            self.__delete__(instance)
        # initialize the attribute if it's not cached yet
        if key not in cache:
            # dependency injection - pass other attrs of the instance as args
            value = self.func(*[getattr(instance, arg) for arg in self.args])
            # if func is a generator, next(1) = value and next(2) = teardown
            if inspect.isgeneratorfunction(self.func):
                # NOTE I owe you a beer if you add type-hints here
                cache[key] = next(value)  # type: ignore
                self.close = lambda: next(value, None)  # type: ignore
            # store simple function / class call return values as-is
            else:
                cache[key] = value
            # take note of the expiration time
            if self.expire_in:
                self.expire_at = int(time.time()) + self.expire_in
        return cache[key]

    def __set__(self, instance, value) -> None:
        """Set arbitrary attribute value."""
        cache = self.get_cache_dict(instance)
        key = self.get_cache_key()
        cache[key] = value

    def __delete__(self, instance) -> None:
        """Delete the cached attribute."""
        cache = self.get_cache_dict(instance)
        key = self.get_cache_key()
        # tear down the attribute if it's cached
        if key in cache:
            if self.close:
                self.close()
            # remove from the cache dict and call an explicit del on the attr
            del cache[key]
            del key

    @staticmethod
    def get_cache_dict(instance) -> dict:
        """Return the cache dict of the given instance."""
        return instance.__dict__.setdefault("_cached", {})

    def get_cache_key(self) -> str:
        """Return the cache key based on the name multiprocess/thread safety."""
        pid = "any" if self.fork_safe else os.getpid()
        tid = "any" if self.thread_safe else threading.get_ident()
        return f"/{self.name}/pid:{pid}/tid:{tid}"


@contextlib.contextmanager
def TempEnv(clear: bool = False, **env: str) -> t.Iterator[t.Dict[str, str]]:
    """Set process environment variables temporarily within a context."""
    old_env = dict(os.environ)
    if clear:
        os.environ.clear()
    os.environ.update(env)
    try:
        yield os.environ  # type: ignore
    finally:
        os.environ.clear()
        os.environ.update(old_env)
