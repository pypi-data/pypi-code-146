import asyncio
import functools
import inspect
import logging
import time
from typing import Any, Callable


def retry_wraps(
        fn: Callable = None,
        *,
        retry_times: int = 0,
        debug: bool = True,
        retry_interval: int = 1,
        onretry: Callable = None,
        finally_call: Callable = None,
        default: Any = '__no_default__',
):
    logger = logging.getLogger('__retry_wraps__')
    debug and logger.setLevel(logging.DEBUG)

    def sync_retry(f, times, *args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if times > 0:
                if callable(onretry):
                    onretry(exc=e)
                time.sleep(retry_interval)
                return sync_retry(f, times - 1, *args, **kwargs)
            raise e

    async def async_retry(f, times, *args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:
            if times > 0:
                if callable(onretry):
                    onretry(exc=e)
                await asyncio.sleep(retry_interval)
                return await async_retry(f, times - 1, *args, **kwargs)
            raise e

    def sync_inner(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            try:
                if retry_times > 0:
                    return sync_retry(f, retry_times, *args, **kwargs)
                return f(*args, **kwargs)
            except Exception as e:
                logger.debug(f.__name__, exc_info=True)
                return e if default == '__no_default__' else default
            finally:
                callable(finally_call) and finally_call(*args, **kwargs)

        return inner

    def async_inner(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            try:
                if retry_times > 0:
                    return await async_retry(f, retry_times, *args, **kwargs)
                return await f(*args, **kwargs)
            except Exception as e:
                logging.debug(f.__name__, exc_info=True)
                return e if default == '__no_default__' else default
            finally:
                callable(finally_call) and finally_call(*args, **kwargs)

        return inner

    def default_inner(f):
        if inspect.iscoroutinefunction(f):
            return async_inner(f)
        else:
            return sync_inner(f)

    return callable(fn) and default_inner(fn) or default_inner


__all__ = ('retry_wraps',)
