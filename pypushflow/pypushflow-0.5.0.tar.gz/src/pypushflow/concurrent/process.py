import sys
import logging
from numbers import Number
from typing import Callable, Optional
from concurrent.futures import ProcessPoolExecutor, Future
from multiprocessing import get_context
from multiprocessing import set_start_method

from . import base
from .interrupt import process as interrupt

logger = logging.getLogger(__name__)


class ProcessPool(base.BasePool):
    """Pool of non-daemonic processes (they can have sub-processes)."""

    def __init__(
        self, context: str = None, max_workers: Optional[int] = None, **kw
    ) -> None:
        kwargs = dict()

        if sys.version_info >= (3, 7):
            if isinstance(context, str) or None:
                context = get_context(context)
            logger.info(f"pypushflow process pool context: '{type(context).__name__}'")
            kwargs["mp_context"] = context
        else:
            logger.info(f"pypushflow process pool context: '{context}'")
            assert isinstance(context, str) or context is None
            set_start_method(context, force=True)
        if max_workers is not None:
            kwargs["max_workers"] = max_workers
        self._pool = _initialize_pool(kwargs)
        self._closed = False
        super().__init__(**kw)

    def __enter__(self):
        self._pool.__enter__()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self._pool.__exit__(exc_type, exc_val, exc_tb)

    def shutdown(
        self,
        block: bool = False,
        timeout: Optional[Number] = None,
        interrupt: bool = False,
    ) -> None:
        super().shutdown(block=block, timeout=timeout, interrupt=interrupt)
        self._pool.shutdown(wait=block)

    def close(self):
        self._closed = True

    def join(self, timeout: Optional[Number] = None) -> bool:
        return False

    def interrupt(self) -> None:
        for pid in list(self._pool._processes):
            interrupt.interrupt_task(pid)

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
        future = self._pool.submit(interrupt.task_main, fn, *args, **kwargs)
        future.add_done_callback(cb)
        return future


def _initialize_pool(kwargs) -> ProcessPoolExecutor:
    if sys.version_info >= (3, 7):
        return ProcessPoolExecutor(initializer=interrupt.worker_initializer, **kwargs)

    pool = ProcessPoolExecutor(**kwargs)
    pool.submit(_worker_initializer, 0).result()
    pool.map(_worker_initializer, [1] * len(pool._processes))
    return pool


def _worker_initializer(seconds):
    from time import sleep

    interrupt.worker_initializer()
    sleep(seconds)
