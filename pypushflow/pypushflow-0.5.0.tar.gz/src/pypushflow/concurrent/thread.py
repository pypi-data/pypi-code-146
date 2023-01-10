from concurrent.futures import ThreadPoolExecutor, Future
from numbers import Number
from typing import Callable, Optional
from . import base


class ThreadPool(base.BasePool):
    def __init__(self, max_workers: Optional[int] = None, **kw) -> None:
        kwargs = dict()
        if max_workers is not None:
            kwargs["max_workers"] = max_workers
        self._pool = ThreadPoolExecutor(**kwargs)
        self._closed = False
        super().__init__(**kw)

    def __enter__(self):
        self._pool.__enter__()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self._pool.__exit__(exc_type, exc_val, exc_tb)

    def close(self):
        self._closed = True

    def join(self, timeout: Optional[Number] = None) -> bool:
        return False

    def interrupt(self) -> None:
        raise RuntimeError("Cannot stop tasks of a thread pool")

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ) -> Future:
        if self._closed:
            raise RuntimeError("the pool is closed")

        def cb(future):
            try:
                result = future.result()
            except Exception as e:
                if error_callback is not None:
                    error_callback(e)
            else:
                if callback is not None:
                    callback(result)

        if kwargs is None:
            kwargs = dict()
        future = self._pool.submit(fn, *args, **kwargs)
        future.add_done_callback(cb)
        return future
