import time
from numbers import Number
from typing import Callable, Optional
from .base import BasePool


class ScalingPool(BasePool):
    def __init__(
        self,
        wait_on_exit: bool = True,
        wait_on_exit_timeout: Optional[Number] = None,
        interrupt_on_exit: bool = False,
        pool_type: Optional[str] = None,
        **pool_options,
    ):
        if pool_type == "scaling":
            raise ValueError("cannot nest scaling pools")
        self._running_pools = list()
        self._finished_pools = list()
        self._pool_type = pool_type
        pool_options["max_workers"] = 1
        self._pool_options = pool_options
        super().__init__(
            wait_on_exit=wait_on_exit,
            wait_on_exit_timeout=wait_on_exit_timeout,
            interrupt_on_exit=interrupt_on_exit,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)

        for pool in self._running_pools:
            pool.__exit__(exc_type, exc_val, exc_tb)
        self._running_pools = list()

        for pool in self._finished_pools:
            pool.__exit__(exc_type, exc_val, exc_tb)
        self._finished_pools = list()

    def close(self):
        for pool in self._finished_pools:
            pool.close()
        for pool in self._running_pools:
            pool.close()

    def join(self, timeout: Optional[Number] = None):
        if timeout is not None:
            t0 = time.time()

        for pool in self._running_pools:
            if not pool.join(timeout=timeout):
                return False
            if timeout is not None:
                timeout -= time.time() - t0
        self._running_pools = list()

        for pool in self._finished_pools:
            if not pool.join(timeout=timeout):
                return False
            if timeout is not None:
                timeout -= time.time() - t0
        self._finished_pools = list()

    def interrupt(self) -> None:
        for pool in list(self._running_pools):
            pool.interrupt()
        for pool in list(self._finished_pools):
            pool.interrupt()

    def _new_pool(self):
        from .factory import get_pool

        pool = get_pool(self._pool_type)(**self._pool_options)
        self._running_pools.append(pool)
        return pool

    def _release_pool(self, pool):
        try:
            idx = self._running_pools.index(pool)
        except ValueError:
            return
        pool = self._running_pools.pop(idx)
        self._finished_pools.append(pool)

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ):
        pool = self._new_pool()

        if callback is None:

            def _callback(return_value):
                self._release_pool(pool)

        else:

            def _callback(return_value):
                try:
                    return callback(return_value)
                finally:
                    self._release_pool(pool)

        if callback is None:

            def _error_callback(exception):
                self._release_pool(pool)

        else:

            def _error_callback(exception):
                try:
                    return error_callback(exception)
                finally:
                    self._release_pool(pool)

        future = pool.apply_async(
            fn,
            args=args,
            kwargs=kwargs,
            callback=_callback,
            error_callback=_error_callback,
        )
        pool.close()
        return future
