from asyncinotify import Inotify, Mask
import asyncio
import os
from typing import Optional


__all__ = ("watch_file_creation",)


class ReadinessWatcher:
    def __init__(self):
        self.inotify = Inotify()
        self.info_by_path = {}


    async def loop(self):
        async for event in self.inotify:
            if (event.mask & Mask.CREATE) and event.path in self.info_by_path:
                event, watch = self.info_by_path[event.path]
                self.inotify.rm_watch(watch)
                event.set()
                del self.info_by_path[event.path]


    async def wait_for_path(self, path: str):
        path = os.path.realpath(path)

        if os.path.exists(path):
            return

        if path in self.info_by_path:
            event, _ = self.info_by_path[path]
        else:
            event = asyncio.Event()
            watch = self.inotify.add_watch(os.path.dirname(path), Mask.CREATE)
            self.info_by_path[path] = event, watch
            if os.path.exists(path):  # race
                if not event.is_set():
                    self.inotify.rm_watch(watch)
                    event.set()
                    del self.info_by_path[event.path]

        await event.wait()


readiness_watcher: Optional[ReadinessWatcher] = None
readiness_watcher_task = None  # keep a strong reference to prevent the task from dying


async def watch_file_creation(path: str):
    global readiness_watcher, readiness_watcher_task

    if readiness_watcher is None:
        readiness_watcher = ReadinessWatcher()
        readiness_watcher_task = asyncio.create_task(readiness_watcher.loop())

    await readiness_watcher.wait_for_path(path)
