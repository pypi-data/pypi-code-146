"""Custon cache module."""
import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar, cast

from aiocache import Cache, cached

T = TypeVar("T")
P = ParamSpec("P")


class CCached(cached):
    """Custom cache class based on aiocache."""

    def __init__(self, ttl: int) -> None:
        """Initialize custom cache decorator."""
        cached.__init__(self, ttl=ttl, cache=Cache.MEMORY)  # type: ignore[no-untyped-call]

    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        """Call custom cache decorator."""
        self.cache = self._cache()

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            value = await self.decorator(func, *args, **kwargs)  # type: ignore[no-untyped-call]
            return cast(T, value)

        wrapper.cache = self.cache  # type: ignore[attr-defined]
        return cast(Callable[P, T], wrapper)
