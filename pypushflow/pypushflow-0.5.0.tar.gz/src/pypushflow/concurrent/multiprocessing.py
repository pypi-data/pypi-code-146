import sys
import logging
from multiprocessing.pool import Pool as _Pool
from multiprocessing.pool import AsyncResult as Future
from multiprocessing import get_context
from numbers import Number
from typing import Callable, Optional
from . import base
from .interrupt import process as interrupt


logger = logging.getLogger(__name__)


class MProcessPool(base.BasePool):
    """Pool of daemonic processes (they cannot have sub-processes)."""

    def __init__(
        self, context: str = None, max_workers: Optional[int] = None, **kw
    ) -> None:
        kwargs = dict()
        if isinstance(context, str) or None:
            context = get_context(context)
        logger.info(f"pypushflow process pool context: '{type(context).__name__}'")
        kwargs["context"] = context
        if max_workers is not None:
            kwargs["processes"] = max_workers

        self._pool = _initialize_pool(kwargs)
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
        self._pool.terminate()

    def close(self):
        self._pool.close()

    def join(self, timeout: Optional[Number] = None) -> bool:
        self._pool.join()
        return True

    def interrupt(self) -> None:
        for p in list(self._pool._pool):
            interrupt.interrupt_task(p.pid)

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ) -> Future:
        if kwargs is None:
            kwargs = dict()
        if args is None:
            args = (fn,)
        else:
            args = (fn,) + args
        return self._pool.apply_async(
            interrupt.task_main,
            args=args,
            kwds=kwargs,
            callback=callback,
            error_callback=error_callback,
        )


def _initialize_pool(kwargs) -> _Pool:
    if sys.version_info >= (3, 7):
        return _Pool(initializer=interrupt.worker_initializer, **kwargs)

    pool = _Pool(**kwargs)
    pool.apply(_worker_initializer, args=(0,))
    pool.map(_worker_initializer, [1] * len(pool._pool))
    return pool


def _worker_initializer(seconds):
    from time import sleep

    interrupt.worker_initializer()
    sleep(seconds)
