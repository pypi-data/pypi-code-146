import functools
from typing import TypeVar, Callable, Dict, List

KEY = TypeVar("KEY")
VALUE = TypeVar("VALUE")
PARTITION_ID = TypeVar("PARTITION_ID")


def partitioned_cached(
        cache,
        *,
        get_key_partitions: Callable[[KEY], Dict[PARTITION_ID, str]],
        combine_partitions: Callable[[List[VALUE]], VALUE],
        partition_value: Callable[[VALUE], Dict[PARTITION_ID, VALUE]],
        cache_lookup_criterion: Callable[[KEY], bool] = lambda key: True,
        key=lambda x: x,
        lock=None
):
    """
    Decorator to wrap a function with a memoizing callable that saves results in a cache.
    """

    def decorator(func):
        if cache is None:

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            def clear():
                pass

        elif lock is None:

            def wrapper(*args, **kwargs):
                k = key(*args, **kwargs)
                partitions = get_key_partitions(k)
                if cache_lookup_criterion(k):
                    try:
                        partition_values = [cache[cache_key] for cache_key in partitions.values()]
                        return combine_partitions(partition_values)
                    except KeyError:
                        pass  # key not found
                v = func(*args, **kwargs)
                partitioned_value = partition_value(v)
                try:
                    for partition_key_identifier, value in partitioned_value.items():
                        k = partitions[partition_key_identifier]
                        cache[k] = value
                except ValueError:
                    pass  # value too large
                return v

            def clear():
                cache.clear()

        else:

            def wrapper(*args, **kwargs):
                k = key(*args, **kwargs)
                partitions = get_key_partitions(k)
                if cache_lookup_criterion(k):
                    try:
                        with lock:
                            partition_values = [cache[cache_key] for cache_key in partitions.values()]
                            return combine_partitions(partition_values)
                    except KeyError:
                        pass  # key not found
                v = func(*args, **kwargs)
                partitioned_value = partition_value(v)
                # in case of a race, prefer the item already in the cache
                try:
                    with lock:
                        for partition_key_identifier, value in partitioned_value.items():
                            k = partitions[partition_key_identifier]
                            cache[k] = value
                except ValueError:
                    return v  # value too large

            def clear():
                with lock:
                    cache.clear()

        wrapper.cache = cache
        wrapper.cache_key = key
        wrapper.cache_lock = lock
        wrapper.cache_clear = clear

        return functools.update_wrapper(wrapper, func)

    return decorator
