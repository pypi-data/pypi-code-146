#!/usr/bin/env python
import os
import sys
import signal
import gevent
import multiprocessing
from contextlib import contextmanager
from dataclasses import dataclass
from queue import Empty

from blissdata.client import configure_with_beacon_address
from blissdata.data.events import Event, EventType
from blissdata.data.node import get_node, get_session_node, DataNodeContainer
from blissdata.redis.manager import RedisAddress


@contextmanager
def run_process(process):
    try:
        process.start()
        yield
    finally:
        process.terminate()
        process.join()


@dataclass
class NodeContent:
    """A pickle-able class to embed a node's data attributes (no implementation related stuff)"""

    type: EventType
    name: str
    db_name: str
    info: dict
    redis_url: str


class RemoteNodeWalker:
    """Node-like object implementing walking functions through a subprocess, thus monkey-patching
    can be avoided locally.
    RemoteNodeWalker and NodeContent objects represent the node's implementation and data, this way
    interprocess communication only sees the data part.

         USER-PROCESS                 SUB-PROCESS
    ┌─────────────────────────────┐       ┌───────────────┐
    │       ┌──────────────────┐  │       │   BLISSDATA   │
    │USER   │ RemoteNodeWalker │  │       │  ┌─────────┐  │
    │CODE:  │                  │  │       │  │real Node│  │
    │walk()<┼───── queue <─────┼──┼───────┼──┤  walk() │  │
    │       └──────────────────┘  │       │  └─────────┘  │
    │        (GEVENT-FREE)        │       │    (GEVENT)   │
    └─────────────────────────────┘       └───────────────┘
    """

    def __init__(self, beacon_host: str, beacon_port: int, node_db_name: str):
        self._queue = multiprocessing.Queue()
        self._beacon_host = beacon_host
        self._beacon_port = beacon_port
        self._node_db_name = node_db_name
        self._keep_running = True

    def stop(self):
        self._keep_running = False

    def walk(self, *args, **kwargs):
        yield from self._run_remote_walk("walk", *args, **kwargs)

    def walk_from_last(self, *args, **kwargs):
        yield from self._run_remote_walk("walk_from_last", *args, **kwargs)

    def walk_events(self, *args, **kwargs):
        yield from self._run_remote_walk("walk_events", *args, **kwargs)

    def walk_on_new_events(self, *args, **kwargs):
        yield from self._run_remote_walk("walk_on_new_events", *args, **kwargs)

    def _run_remote_walk(
        self,
        walk_func_name,
        *walk_func_args,
        started_event=None,
        stop_handler=None,
        **walk_func_kwargs,
    ):
        if stop_handler is not None:
            raise RuntimeError("RemoteNodeWalker doesn't support `stop_handler`")

        user_started_event = None
        if started_event is not None:
            user_started_event = started_event
            started_event = multiprocessing.Event()
        walk_func_kwargs["started_event"] = started_event

        process = multiprocessing.Process(
            target=RemoteNodeWalker._remote_task,
            daemon=True,
            args=(
                self._beacon_host,
                self._beacon_port,
                self._node_db_name,
                self._queue,
                walk_func_name,
                walk_func_args,
                walk_func_kwargs,
            ),
        )

        with run_process(process):
            if started_event is not None:
                while process.is_alive() and self._keep_running:
                    if started_event.wait(timeout=0.2):
                        user_started_event.set()
                        break
            while process.is_alive() and self._keep_running:
                try:
                    yield self._queue.get(timeout=0.2)
                except Empty:
                    pass
            if not process.is_alive():
                raise RuntimeError("RemoteNodeWalker subprocess failed.")

    @staticmethod
    def _remote_task(
        beacon_host,
        beacon_port,
        node_db_name,
        queue,
        walk_func_name,
        walk_func_args,
        walk_func_kwargs,
    ):
        """Suprocess main function, don't use it on user side to prevent gevent patching"""
        gevent.monkey.patch_all(thread=False)

        # A watchdog looking at parent's PID to exit if parent dies. If the parent encounters an
        # exception below python level, context managers or "try" statements won't exit properly.
        # Thus, the child has to keep an eye on its parent.
        def watchdog():
            parent_pid = os.getppid()
            while True:
                try:
                    # send null signal to test pid
                    os.kill(parent_pid, 0)
                except OSError:
                    sys.exit(0)
                gevent.sleep(1)

        # Inhibit SIGINT handler before running watchdog, so it is protected from Ctrl-C
        def dummy_handler(signum, frame):
            pass

        signal.signal(signal.SIGINT, dummy_handler)

        gevent.spawn(watchdog)

        configure_with_beacon_address(beacon_host, beacon_port)

        # if a node_db_name contains no ":", it is a session, therefore it should be
        # accessed with get_session_node(), which allows to start walking on it before
        # it even exists in Redis.
        if ":" in node_db_name:
            target_node = get_node(node_db_name)
            if target_node is None:
                raise RuntimeError(f'Node "{node_db_name}" doesn\'t exist.')
        else:
            target_node = get_session_node(node_db_name)

        walk_function = getattr(target_node, walk_func_name)

        for result in walk_function(*walk_func_args, **walk_func_kwargs):
            if isinstance(result, Event):
                ev_type, node, data = result
                packed_event = Event(ev_type, RemoteNodeWalker.pack_node(node), data)
                queue.put(packed_event)
            elif isinstance(result, DataNodeContainer):
                packed_node = RemoteNodeWalker.pack_node(result)
                queue.put(packed_node)
            else:
                RuntimeError(
                    f"Oops, unexpected walk function return type: {type(result)}"
                )

    @staticmethod
    def pack_node(node):
        """Pack revelant node's information to be pickled, without embedding Gevent or Redis related stuff."""
        redis_kw = node.db_connection.connection_pool.connection_kwargs
        if "path" in redis_kw:
            redis_url = (
                RedisAddress.factory(f"localhost:{redis_kw['path']}").url
                + f"?db={redis_kw['db']}"
            )
        else:
            redis_url = (
                RedisAddress.factory(f"{redis_kw['host']}:{redis_kw['port']}").url
                + f"/{redis_kw['db']}"
            )

        return NodeContent(
            node.node_type,
            node.name,
            node.db_name,
            RemoteNodeWalker.pack_info(node.info),
            redis_url,
        )

    @staticmethod
    def pack_info(info):
        info_dict = info.get_all()
        try:
            # ScanState objects brings Bliss dependencies with them, replace with name
            info_dict["state"] = info["state"].name
        except KeyError:
            pass
        return info_dict
