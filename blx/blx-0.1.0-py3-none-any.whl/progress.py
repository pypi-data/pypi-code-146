from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Queue
from threading import Event, Thread
from types import TracebackType
from typing import Optional, Type

from rich.progress import Progress as RichBar

POLLING = 0.1

__all__ = ["Progress"]


class Progress(Thread):
    def __init__(self, desc: str, transient: bool = False, disable: bool = False):
        self._rich_bar = RichBar(transient=transient, disable=disable)
        self._task = self._rich_bar.add_task(desc, total=None)

        self._shutdown = Event()
        self._display_queue = Queue()

        self._total = -1

    def set_meta(self, total_length: int | None = None, object_name: str | None = None):
        if total_length:
            self._total = total_length
            self._rich_bar.reset(self._task, total=self._total)
            self._rich_bar.start_task(self._task)
        del object_name

    def update(self, size: int):
        self._display_queue.put(size)

    def shutdown(self, force_finish: bool = False):
        self._shutdown.set()
        if force_finish:
            self._force_finish()

    def loop(self):
        while not self._shutdown.is_set():
            try:
                consumed = self._display_queue.get(timeout=POLLING)
            except Empty:
                continue

            self._rich_bar.update(self._task, advance=consumed)
            self._display_queue.task_done()

    def _force_finish(self):
        if self._total == -1:
            return
        self._rich_bar.update(self._task, completed=self._total)
        self._rich_bar.refresh()

    def __enter__(self):
        self._ex = ThreadPoolExecutor(max_workers=1)
        self._rich_bar.__enter__()
        self._future = self._ex.submit(self.loop)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.shutdown()
        self._future.result()
        self._rich_bar.__exit__(exc_type, exc_val, exc_tb)
        self._ex.__exit__(exc_type, exc_val, exc_tb)
