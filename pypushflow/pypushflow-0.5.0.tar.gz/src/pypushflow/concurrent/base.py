from numbers import Number
from typing import Callable, Optional


class BasePool:
    def __init__(
        self,
        wait_on_exit: bool = True,
        wait_on_exit_timeout: Optional[Number] = None,
        interrupt_on_exit: bool = False,
        **_
    ) -> None:
        self._wait_on_exit = wait_on_exit
        self._wait_on_exit_timeout = wait_on_exit_timeout
        self._interrupt_on_exit = interrupt_on_exit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(
            block=self._wait_on_exit,
            timeout=self._wait_on_exit_timeout,
            interrupt=self._interrupt_on_exit,
        )

    def close(self):
        """Prevents any more tasks from being submitted to the pool."""
        raise NotImplementedError

    def join(self, timeout: Optional[Number] = None):
        """Wait for the workers to exit."""
        raise NotImplementedError

    def shutdown(
        self,
        block: bool = False,
        timeout: Optional[Number] = None,
        interrupt: bool = False,
    ) -> None:
        """Cleanup all resources. Waits for tasks to finish unless `interrupt=True`."""
        self.close()
        if interrupt:
            self.interrupt()
        if block:
            self.join(timeout=timeout)

    def interrupt(self) -> None:
        """Stop all running tasks"""
        raise NotImplementedError

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ):
        raise NotImplementedError
