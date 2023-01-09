import msglink
from typing import Dict, Set
from dataclasses import dataclass
import asyncio
import ssl
import logging
import socket
from contextlib import suppress

log = logging.getLogger()


class Router(msglink.Callbacks):
    def __init__(self, server, port, role, password, info=""):
        self._protocol = msglink.Protocol(self)
        self._connected_peers: Dict[int, Router.Peer] = dict()
        self._server = server
        self._port = port
        self._role = role
        self._password = password
        self._info = info
        self._reconnect_interval = 10
        self._running = False
        self._peer_discoveries: Set[Router.PeerDiscovery] = set()
        self._disconnect_waits: Set[Router.DisconnectWait] = set()
        self._client_readers: Set[Router.ClientReader] = set()
        self._channel_readers: Set[Router.ChannelReader] = set()
        self._topic_readers: Set[Router.TopicReader] = set()
        self._established = False
        self._reconnect_task: asyncio.Task | None = None
        self._auth_future: asyncio.Future | None = None

    def start(self):
        if self._running:
            return

        self._running = True
        self._reconnect_task = asyncio.create_task(self._reconnect_loop())

    async def stop(self):
        self._running = False
        self._reconnect_task.cancel()
        with suppress(asyncio.CancelledError):
            await self._reconnect_task
        await self._protocol.async_close()

    def set_reconnect_interval(self, reconnect_interval: int):
        self._reconnect_interval = reconnect_interval

    async def discover_one(self, role: str):
        for pid, peer in self._connected_peers.items():
            if peer.role == role:
                return pid

        disc = Router.PeerDiscovery(role=role)
        self._peer_discoveries.add(disc)
        if self._established:
            self._protocol.send_watch_role(role)
        pid = await disc.queue.get()
        disc.queue.task_done()
        self._peer_discoveries.remove(disc)
        return pid

    async def discover_all(self, role: str):
        disc = Router.PeerDiscovery(role=role)
        self._peer_discoveries.add(disc)

        if self._established:
            self._protocol.send_watch_role(role)

        # store known and matching in list before yielding to avoid race conditions
        # otherwise _known_peers could change mid-iteration during the yield
        matching_known = list()
        for pid, peer in self._connected_peers.items():
            if peer.role == role:
                matching_known.append(pid)

        try:
            for pid in matching_known:
                yield pid

            while self._running:
                yield await disc.queue.get()
                disc.queue.task_done()

        finally:  # handles GeneratorExit
            self._peer_discoveries.remove(disc)

    async def wait_peer_disconnected(self, peer: int):
        if peer not in self._connected_peers:
            return

        wait = Router.DisconnectWait(peer)
        self._disconnect_waits.add(wait)
        await wait.future
        self._disconnect_waits.remove(wait)

    async def read_peer_messages(self, peer: int):
        if peer not in self._connected_peers:
            return

        cr = Router.ClientReader(peer)
        self._client_readers.add(cr)

        try:
            while self._running:
                msg = await cr.queue.get()
                if msg is not None:
                    yield msg
                else:
                    return
        finally:
            self._client_readers.remove(cr)

    async def read_peer_channel(self, peer: int, channel: int):
        if peer not in self._connected_peers:
            return

        cr = Router.ChannelReader(peer, channel)
        self._channel_readers.add(cr)

        try:
            while self._running:
                msg = await cr.queue.get()
                if msg is not None:
                    yield msg
                else:
                    return
        finally:
            self._channel_readers.remove(cr)

    def get_peer_role(self, peer: int) -> str | None:
        if peer not in self._connected_peers:
            return None
        else:
            return self._connected_peers[peer].role

    def get_peer_info(self, peer: int) -> str | None:
        if peer not in self._connected_peers:
            return None
        else:
            return self._connected_peers[peer].info

    async def subscribe_topic(self, topic: str):
        sub = Router.TopicReader(topic=topic)
        self._topic_readers.add(sub)
        self._protocol.send_subscribe(topic)

        try:
            while self._running:
                msg = await sub.queue.get()
                if msg is not None:
                    yield msg
                else:
                    return
        finally:
            self._topic_readers.remove(sub)

    async def send_message(self, receiver: int, channel: int, msg: bytes):
        await self._protocol.send_message(receiver, channel, msg)

    async def make_post(self, topic: str, msg: bytes):
        await self._protocol.send_post(topic, msg)

    # ==================================================================================================================
    # end of public interface
    # ==================================================================================================================

    @dataclass
    class Peer:
        role: str
        info: str

    class PeerDiscovery:
        def __init__(self, role):
            self.role = role
            self.queue = asyncio.Queue()

    class DisconnectWait:
        def __init__(self, peer):
            self.pid = peer
            self.future = asyncio.Future()

    class ClientReader:
        def __init__(self, peer: int):
            self.pid = peer
            self.queue = asyncio.Queue()

    class ChannelReader:
        def __init__(self, peer: int, channel: int):
            self.pid = peer
            self.channel = channel
            self.queue = asyncio.Queue()

    class TopicReader:
        def __init__(self, topic: str):
            self.topic = topic
            self.queue = asyncio.Queue()

    async def _try_connect_msglink(self):
        if self._protocol.is_connected():
            # tcp connection already established
            return

        log.info(f"[msglink] connecting to {self._server}:{self._port}")
        loop = asyncio.get_running_loop()
        await loop.create_connection(lambda: self._protocol, self._server, self._port, ssl=ssl.SSLContext())
        log.info(f"[msglink] connected to {self._server}:{self._port}")

    async def _try_authenticate(self):
        if self._auth_future is not None and self._auth_future.result():
            # authentication already established
            return

        # need to make new authentication attempt
        # (_auth_result either None or failed)
        log.info(f"[msglink] authenticating to {self._server}")
        self._auth_future = asyncio.Future()
        self._protocol.send_auth_request(self._role, self._password, self._info)
        await self._auth_future

    async def _reconnect_loop(self):
        while self._running:
            try:
                await self._try_connect_msglink()
                await self._try_authenticate()

            except socket.error as e:
                log.warning(f"[msglink] error connecting to {self._server}: {e}")
            await asyncio.sleep(self._reconnect_interval)

    def _all_disconnected(self):
        for d in self._disconnect_waits:
            d.future.set_result(None)

        for cr in self._channel_readers:
            cr.queue.put_nowait(None)

    # msglink callbacks =================================================================
    def on_connect_close(self):
        log.info(f"[msglink] connection to {self._server}:{self._port} was closed")
        self._established = False
        self._connected_peers.clear()
        self._all_disconnected()
        self._auth_future = None

    def on_auth_fail(self):
        log.warning(f"[msglink] authentication failed for role '{self._role}' at server {self._server}")
        self._auth_future.set_result(False)

    def on_auth_success(self):
        log.info(f"[msglink] authentication successful")
        self._established = True
        self._auth_future.set_result(True)
        for pd in self._peer_discoveries:
            self._protocol.send_watch_role(pd.role)

    def on_peer_online(self, peer, role, info):
        self._connected_peers[peer] = Router.Peer(role=role, info=info)
        for pd in self._peer_discoveries:
            if pd.role == role:
                pd.queue.put_nowait(peer)

    def on_peer_offline(self, peer, role):
        del self._connected_peers[peer]
        for d in self._disconnect_waits:
            if d.pid == peer:
                d.future.set_result(None)

        for cr in self._channel_readers:
            if cr.pid == peer:
                cr.queue.put_nowait(None)

    def on_message(self, sender, role, channel, payload):
        for cr in self._client_readers:
            if cr.pid == sender:
                cr.queue.put_nowait(payload)

        for cr in self._channel_readers:
            if cr.pid == sender and cr.channel == channel:
                cr.queue.put_nowait(payload)

    def on_post(self, sender, role, topic, payload):
        for sub in self._topic_readers:
            if sub.topic == topic:
                sub.queue.put_nowait(payload)
