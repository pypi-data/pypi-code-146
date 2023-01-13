import asyncio
import contextlib
import os
from sortedcontainers import SortedDict
import time
from typing import Optional

from .environment import BoxEnvironment


__all__ = ("Box", "BoxContextManager")


N_PERMITTED_PARALLEL_BOXES_WITH_UNLIMITED_RUNTIME = 5


unused_boxes = SortedDict()
box_cleanup_task = None  # keep a strong reference to prevent the task from dying


class BoxContextManager:
    def __init__(self, box: "Box"):
        self._box = box

    def __enter__(self) -> "BoxContextManager":
        if self._box._use_count == 0:
            del unused_boxes[self._box._cleanup_at, id(self._box)]
        self._box._use_count += 1
        return self

    def __exit__(self, *exc):
        self._box._cleanup_at = time.time() + self._box.cleanup_timeout
        self._box._use_count -= 1
        assert self._box._use_count >= 0
        if self._box._use_count == 0:
            add_unused_box(self._box)


def add_unused_box(box: "Box"):
    global box_cleanup_task

    unused_boxes[box._cleanup_at, id(box)] = box
    if len(unused_boxes) == N_PERMITTED_PARALLEL_BOXES_WITH_UNLIMITED_RUNTIME + 1:
        box_cleanup_task = asyncio.create_task(cleanup_old_boxes())


async def cleanup_old_boxes():
    while len(unused_boxes) > N_PERMITTED_PARALLEL_BOXES_WITH_UNLIMITED_RUNTIME:
        (cleanup_at, _), _ = unused_boxes.peekitem(0)
        if cleanup_at < time.time():
            _, box = unused_boxes.popitem(0)
            assert box._use_count == 0
            await box.stop()
        else:
            await asyncio.sleep(5)


class Box:
    def __init__(self, token: str, scope: str, process: asyncio.subprocess.Process, env: BoxEnvironment, cleanup_timeout: float):
        self.token = token
        self.scope = scope
        self.process = process
        self.env = env
        self.cleanup_timeout = cleanup_timeout

        self._use_count: int = 0
        self._cleanup_at: float = time.time() + cleanup_timeout
        self._stopping: bool = False

        add_unused_box(self)


    def is_stopping(self) -> bool:
        return self._stopping


    def is_alive(self) -> bool:
        # asyncio subprocesses don't have poll()
        return not self._stopping and os.path.exists(f"/proc/{self.process.pid}")


    async def stop(self):
        if self._stopping:
            await self.process.wait()
            return
        self._stopping = True
        self.process.terminate()
        try:
            await asyncio.wait_for(self.process.wait(), timeout=5)
        except TimeoutError:
            self.process.kill()
            # XXX: this might hang due to a kernel/driver bug or whatever. Do we want to handle this
            # case gracefully?
            await self.process.wait()


    def get_external_file_path(self, path: str) -> str:
        return f"/proc/{self.process.pid}/root/{path}"


    def get_external_socket_address(self, address: str) -> str:
        if address.startswith("unix:"):
            return "unix:" + self.get_external_file_path(address[5:])
        else:
            return f"netns:/proc/{self.process.pid}/ns/net:{address}"


    def open(self, path: str, *args, **kwargs):
        return open(self.get_external_file_path(path), *args, **kwargs)


    def get_socket_address(self) -> Optional[str]:
        if not self.env.socket:
            return None
        return self.get_external_socket_address(self.env.socket)


    def borrow(self) -> BoxContextManager:
        if self._stopping:
            raise ValueError("Cannot borrow a box after it is stopped")
        return BoxContextManager(self)
