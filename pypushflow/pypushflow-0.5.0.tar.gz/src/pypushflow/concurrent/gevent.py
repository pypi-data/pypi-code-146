from numbers import Number
from gevent.pool import Group
from gevent import Greenlet
from typing import Callable, Optional
from . import base
from .interrupt import gevent as terminate


class GreenletPool(base.BasePool):
    """Pool of greenlets."""

    def __init__(self, **kw) -> None:
        self._closed = False
        self._pool = Group()
        super().__init__(**kw)

    def shutdown(
        self,
        block: bool = False,
        timeout: Optional[Number] = None,
        interrupt: bool = False,
    ) -> None:
        super().shutdown(block=block, timeout=timeout, interrupt=interrupt)
        self._pool.kill(block=block, timeout=timeout)

    def close(self):
        self._closed = True

    def join(self, timeout: Optional[Number] = None) -> bool:
        return self._pool.join(timeout=timeout, raise_error=False)

    def interrupt(self) -> None:
        for glts in list(self._pool.greenlets):
            terminate.interrupt_task(glts)

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ) -> Greenlet:
        if self._closed:
            raise RuntimeError("the pool is closed")
        if self._pool is None:
            raise RuntimeError("enter the pool context first")
        if kwargs is None:
            kwargs = dict()

        def cb(glt):
            try:
                result = glt.get()
            except Exception as e:
                if error_callback is not None:
                    error_callback(e)
            else:
                if callback is not None:
                    callback(result)

        glt = Greenlet(terminate.task_main, fn, *args, **kwargs)
        glt.link(cb)
        self._pool.start(glt)
        return glt
