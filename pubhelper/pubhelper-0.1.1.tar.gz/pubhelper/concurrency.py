import functools
from threading import Lock
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor


class LockData(object):
    def __init__(self, data: Any):
        self.data = data
        self.data_lock = Lock()

    def __call__(self, f: Callable, *args, **kwargs):
        with self.data_lock:
            return f(*args, lock_data=self.data, **kwargs)


class ThreadFunc(object):
    def __init__(self, fn, *, concurrency: int = 1):
        if 0 < concurrency <= 10:
            self.f: Callable = fn
            self.thds = concurrency
        else:
            raise Exception('concurrency in [1, 10]')

    def __call__(self, *args, block=True, **kwargs):
        workers = ThreadPoolExecutor(self.thds)
        tasks = [workers.submit(self.f, *args, **kwargs)
                 for _ in range(self.thds)]
        return block and [t.result() for t in tasks] or tasks


def concur_wraps(fn=None, *, concurrency=1):
    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            return ThreadFunc(
                f, concurrency=concurrency
            )(*args, **kwargs)

        return inner

    return fn and wrap(fn) or wrap


__all__ = ('LockData', 'ThreadFunc', 'concur_wraps')
