import asyncio
from typing import List, Dict, Optional
from collections import deque, defaultdict
from msglink import packets
import hashlib
import time
from contextlib import suppress



BUFFER_TIME_MS = 500
MIN_WINDOW = 3000
UINT32_MAX = 2**32 - 1


class Callbacks:
    def on_connect_close(self):
        pass

    def on_auth_fail(self):
        pass

    def on_auth_success(self):
        pass

    def on_peer_online(self, peer, role, info):
        pass

    def on_peer_offline(self, peer, role):
        pass

    def on_message(self, sender, role, channel, payload):
        pass

    def on_post(self, sender, role, topic, payload):
        pass


class Stream:
    def __init__(self, receiver, channel, topic):
        self.queue = deque()
        self.bytes_sent = 0
        self.receiver = receiver
        self.channel = channel
        self.topic = topic


class Protocol(asyncio.Protocol):
    def __init__(self, callbacks: Callbacks):
        self._callbacks = callbacks
        self._send_window = MIN_WINDOW
        self._rec_window = MIN_WINDOW
        self._bytes_since_update = 0
        self._last_update_time = time.perf_counter()
        self._streams: List[Stream] = list()
        self._transport: Optional[asyncio.WriteTransport] = None
        self._input_buffer = bytearray()
        self._is_connected = False
        self._peer_roles = dict()
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._message_buffers: Dict[tuple, bytearray] = defaultdict(bytearray)
        self._post_buffers: Dict[tuple, bytearray] = defaultdict(bytearray)
        self._topics: Dict[bytes, str] = dict()
        self._send_paused = False
        self._debug_flow = False

    def pause_writing(self) -> None:
        self._send_paused = True

    def resume_writing(self) -> None:
        self._send_paused = False
        self._send_queued()

    def _clear(self):
        self._send_window = MIN_WINDOW
        self._rec_window = MIN_WINDOW
        self._bytes_since_update = 0
        self._last_update_time = time.perf_counter()
        self._streams.clear()
        self._input_buffer = bytearray()
        self._is_connected = False
        self._peer_roles.clear()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None

    def connection_made(self, transport: asyncio.WriteTransport):
        self._clear()
        self._transport = transport
        self._is_connected = True
        self._heartbeat_task = asyncio.ensure_future(self._heartbeat_loop())

    def data_received(self, data):
        self._input_buffer.extend(data)
        while len(self._input_buffer) >= 3:
            packet_type = int.from_bytes(self._input_buffer[0:1], 'big')
            payload_size = int.from_bytes(self._input_buffer[1:3], 'big')
            if len(self._input_buffer) < 3 + payload_size:
                return
            payload = self._input_buffer[3:3+payload_size]
            self._input_buffer = self._input_buffer[3+payload_size:]
            self._handle_packet(packet_type, payload)

    def connection_lost(self, exc):
        self._clear()
        self._callbacks.on_connect_close()

    def close(self):
        self._transport.abort()

    async def async_close(self):
        unfinished = self._heartbeat_task
        self.close()
        if unfinished:
            with suppress(asyncio.CancelledError):
                await unfinished

    def is_connected(self):
        return self._is_connected

    def send_auth_request(self, role, password, info):
        self._send_control_packet(packets.encode_auth_request(role, password, info))

    def send_watch_role(self, role):
        self._send_control_packet(packets.encode_watch_role(role))

    async def send_message(self, receiver: int, channel: int, payload: bytes):
        if len(payload) <= packets.MESSAGE_FULL_MAX_PAYLOAD:
            packet = packets.encode_message_full(receiver, channel, payload)
            await self._send_message_packet(receiver, channel, None, packet)
        else:
            pos = 0
            while pos < len(payload) - 1:
                size = min(len(payload) - pos, packets.MESSAGE_PART_MAX_PAYLOAD)
                packet = packets.encode_message_part(receiver, channel, payload[pos:pos+size])
                await self._send_message_packet(receiver, channel, None, packet)
                pos += size
            packet = packets.encode_message_end(receiver, channel)
            await self._send_message_packet(receiver, channel, None, packet)

    async def send_post(self, topic: str, payload: bytes):
        topic_id = hashlib.sha256(topic.encode("utf-8")).digest()
        if len(payload) <= packets.POST_FULL_MAX_PAYLOAD:
            packet = packets.encode_post_full(topic_id, payload)
            await self._send_message_packet(None, None, topic, packet)
        else:
            pos = 0
            while pos < len(payload) - 1:
                size = min(len(payload) - pos, packets.POST_PART_MAX_PAYLOAD)
                packet = packets.encode_post_part(topic_id, payload[pos:pos + size])
                await self._send_message_packet(None, None, topic, packet)
                pos += size
            packet = packets.encode_post_end(topic_id)
            await self._send_message_packet(None, None, topic, packet)

    def send_subscribe(self, topic: str):
        topic_id = hashlib.sha256(topic.encode('utf-8')).digest()
        self._topics[topic_id] = topic
        self._send_control_packet(packets.encode_subscribe(topic_id))

    def send_drop_buffered(self, receiver, channel):
        self._send_control_packet(packets.encode_drop_buffered(receiver, channel))

    def set_debug_flow(self, debug):
        self._debug_flow = debug

    def _send_control_packet(self, packet):
        self._transport.write(packet)

    async def _send_message_packet(self, receiver, channel, topic, packet):
        if self._send_window <= 0 or self._send_paused:
            stream = self._get_stream(receiver, channel, topic)
            future = asyncio.Future()
            stream.queue.append((future, packet))
            await future
        else:
            self._transport.write(packet)
            self._send_window -= len(packet) - 3

    def _get_stream(self, receiver, channel, topic):
        for stream in self._streams:
            if stream.receiver == receiver and stream.channel == channel and stream.topic == topic:
                return stream
        stream = Stream(receiver, channel, topic)
        self._streams.append(stream)
        return stream

    def _handle_packet(self, packet_type, packet_data):
        self._extend_deadline = True
        if packet_type == packets.AUTH_FAIL:
            self._callbacks.on_auth_fail()

        elif packet_type == packets.AUTH_OK:
            self._callbacks.on_auth_success()

        elif packet_type == packets.PEER_ONLINE:
            peer, role, info = packets.decode_peer_online(packet_data)
            self._peer_roles[peer] = role
            self._callbacks.on_peer_online(peer, role, info)

        elif packet_type == packets.PEER_OFFLINE:
            peer = packets.decode_peer_offline(packet_data)
            role = self._peer_roles.pop(peer)
            self._callbacks.on_peer_offline(peer, role)

        elif packet_type == packets.MESSAGE_FULL:
            sender, channel, payload = packets.decode_message_full(packet_data)
            self._update_receive_flow(len(packet_data))
            role = self._peer_roles[sender]
            self._callbacks.on_message(sender, role, channel, payload)

        elif packet_type == packets.MESSAGE_PART:
            sender, channel, payload = packets.decode_message_part(packet_data)
            self._update_receive_flow(len(packet_data))
            self._message_buffers[(sender, channel)].extend(payload)

        elif packet_type == packets.MESSAGE_END:
            sender, channel = packets.decode_message_end(packet_data)
            self._update_receive_flow(len(packet_data))
            payload = self._message_buffers.pop((sender, channel))
            role = self._peer_roles[sender]
            self._callbacks.on_message(sender, role, channel, payload)

        elif packet_type == packets.POST_FULL:
            sender, topic_id, payload = packets.decode_post_full(packet_data)
            self._update_receive_flow(len(packet_data))
            role = self._peer_roles[sender]
            topic = self._topics.get(topic_id, None)
            self._callbacks.on_post(sender, role, topic, payload)

        elif packet_type == packets.POST_PART:
            sender, topic_id, payload = packets.decode_post_part(packet_data)
            self._update_receive_flow(len(packet_data))
            self._post_buffers[(sender, topic_id)].extend(payload)

        elif packet_type == packets.POST_END:
            sender, topic_id = packets.decode_post_end(packet_data)
            self._update_receive_flow(len(packet_data))
            payload = self._post_buffers.pop((sender, topic_id))
            role = self._peer_roles[sender]
            topic = self._topics.get(topic_id, None)
            self._callbacks.on_post(sender, role, topic, payload)

        elif packet_type == packets.WINDOW_UPDATE:
            self._send_window += packets.decode_window_update(packet_data)
            self._send_queued()

        elif packet_type == packets.HEARTBEAT:
            pass

        elif packet_type == packets.DROP_BUFFERED:
            peer, channel = packets.decode_drop_buffered(packet_data)
            self._message_buffers.pop((peer, channel), None)

        else:
            print(f"got packet with invalid type {packet_type}")

    def _send_queued(self):
        if not self._streams or self._send_window <= 0 or self._send_paused:
            return

        # tare bytes_sent
        min_stream = min(self._streams, key=lambda x: x.bytes_sent)
        min_sent = min_stream.bytes_sent
        for stream in self._streams:
            stream.bytes_sent -= min_sent

        # send queued
        while self._send_window > 0 and self._streams and not self._send_paused:
            index, stream = min(enumerate(self._streams), key=lambda x: x[1].bytes_sent)
            future, packet = stream.queue.popleft()
            stream.bytes_sent += len(packet) - 3
            self._transport.write(packet)
            self._send_window -= len(packet) - 3
            future.set_result(None)
            if not stream.queue:
                del self._streams[index]

    def _update_receive_flow(self, received_bytes):
        # (1) update count of received bytes
        self._bytes_since_update += received_bytes

        # (2) Is the number of bytes received smaller than a quarter of the current window?
        if self._bytes_since_update < self._rec_window / 4:
            return

        # (3) Calculate new window size. new_window = buffer_time / measured_time * received_bytes (+ apply bounds)
        now = time.perf_counter()
        ms_since_last_update = max(round((now - self._last_update_time) * 1000), 1)
        new_window = round(BUFFER_TIME_MS / ms_since_last_update * self._bytes_since_update)
        min_new_window = max(MIN_WINDOW, round(self._rec_window / 2))
        max_new_window = min(UINT32_MAX, self._rec_window * 2)
        new_window = max(min_new_window, min(new_window, max_new_window))

        if self._debug_flow:
            old_speed = _fmt_size(self._rec_window * 1000 / BUFFER_TIME_MS)
            new_speed = _fmt_size(new_window * 1000 / BUFFER_TIME_MS)
            print(f"speed {old_speed}/s -> {new_speed}/s  "
                  f"window {_fmt_size(self._rec_window)} -> {_fmt_size(new_window)}  "
                  f"received {_fmt_size(self._bytes_since_update)} in {ms_since_last_update}ms")

        # (4) Calculate window update size
        window_update = new_window + self._bytes_since_update - self._rec_window

        # (5) Is the window update size positive (could be negative when window is shrinking
        if window_update <= 0:
            return

        # (6) Save state and send window update
        self._last_update_time = now
        self._rec_window = new_window
        self._bytes_since_update = 0
        self._send_control_packet(packets.encode_window_update(window_update))

    async def _heartbeat_loop(self):
        try:
            while True:
                # send heartbeat every 30s, check connection every 60s
                await asyncio.sleep(20)
                self._send_control_packet(packets.encode_heartbeat())
                await asyncio.sleep(20)
                self._send_control_packet(packets.encode_heartbeat())
                await asyncio.sleep(20)
                self._send_control_packet(packets.encode_heartbeat())
                if self._extend_deadline:
                    self._extend_deadline = False
                else:
                    self._transport.abort()
                    return
        except asyncio.CancelledError:
            pass


def _fmt_size(size):
    for suffix in ["Byte", "KB", "MB", "GB"]:
        if size < 1024:
            break
        size /= 1024
    return f"{round(size)} {suffix}"
