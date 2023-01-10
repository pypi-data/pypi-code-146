from numbers import Number
import logging
from billiard.pool import Pool as _Pool
from billiard.pool import ApplyResult as Future
from billiard import get_context
from typing import Callable, Optional
from . import base
from .interrupt import process as interrupt


logger = logging.getLogger(__name__)


class RemoteTraceback(Exception):
    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb


class BProcessPool(base.BasePool):
    """Pool of non-daemonic processes (but they CAN have sub-processes)."""

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
        self._pool = _Pool(initializer=interrupt.worker_initializer, **kwargs)
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

        if error_callback is not None:
            org_error_callback = error_callback

            def error_callback(info):
                info.exception.__cause__ = RemoteTraceback(info.traceback)
                return org_error_callback(info.exception)

        return self._pool.apply_async(
            interrupt.task_main,
            args=args,
            kwds=kwargs,
            callback=callback,
            error_callback=error_callback,
        )
