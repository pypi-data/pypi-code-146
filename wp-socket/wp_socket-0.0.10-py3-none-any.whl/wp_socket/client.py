"""Wall Pad Socket Client"""
import asyncio

import logging
from typing import Any

_CONNECTION_TIMEOUT = 5.0
_READ_TIMEOUT = 5.0
_QUEUE_WAIT_TIMEOUT = 1.0
_DEFAULT_READ_BUFFER = 512  # 512 bytes

_LOGGER = logging.getLogger(__name__)


class WpSocketClient:
    """Wall Pad Socket Client"""
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    def __init__(self, host: str, port: int, async_packets_handler):
        self._host = host
        self._port = port
        self._wait_tasks: Any = None
        self._async_receive_handler = async_packets_handler

        self._loop = asyncio.get_event_loop()
        self._receive_packet_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._send_packet_queue: asyncio.Queue[bytes] = asyncio.Queue()

        self._retry_cnt = 0
        self.connected = False

    async def async_on_connected(self):
        """Socket connected notifications"""

    async def async_on_disconnected(self):
        """Socket disconnected notifications"""

    async def async_on_reconnect(self):
        """Socket reconnect notifications"""

    async def async_connect(self) -> bool:
        """Socket connect"""
        await self._async_wait_for_disconnect()

        _LOGGER.debug('connecting to server %s', self._host)
        try:
            asyncio.set_event_loop(self._loop)
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port),
                timeout=_CONNECTION_TIMEOUT)
            self.connected = True
            self._retry_cnt = 0

            self._loop.create_task(self.async_on_connected())

            tasks = [self._loop.create_task(self._async_reader_handler()),
                     self._loop.create_task(self._async_reader()),
                     self._loop.create_task(self._async_writer())]
            self._wait_tasks = asyncio.wait(tasks)
            return True
        except Exception as ex:
            _LOGGER.error("connection error, %s, %s", self._host, ex)
            self.disconnect()
        return False

    async def _async_reconnect(self):
        """Socket reconnect"""
        self._loop.create_task(self.async_on_reconnect())
        wait_time = self._retry_cnt * 5 if self._retry_cnt < 12 else 60
        _LOGGER.debug('reconnect connect, wait %d s', wait_time)
        await asyncio.sleep(wait_time)
        self._retry_cnt += 1
        if not await self.async_connect():
            await self._async_reconnect()

    async def async_send_packet(self, packet: bytes):
        """Send packet"""
        await self._send_packet_queue.put(packet)

    async def _async_reader_handler(self):
        """Queue read handler"""
        _LOGGER.debug('message handler start')
        while self.connected:
            try:
                packets = await asyncio.wait_for(self._receive_packet_queue.get(),
                                                 timeout=_QUEUE_WAIT_TIMEOUT)
                await self._async_receive_handler(packets)
                self._receive_packet_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as ex:
                _LOGGER.error('message handler error, %s', ex)

        _LOGGER.debug('message handler end')

    async def _async_reader(self):
        """Socket read packet"""
        _LOGGER.debug('reader start')
        while self.connected:
            try:
                data = await asyncio.wait_for(self._reader.read(_DEFAULT_READ_BUFFER),
                                              timeout=_READ_TIMEOUT)
                if not data:
                    self._loop.create_task(self._async_reconnect())
                    break

                _LOGGER.debug('Received [%d]: %s', len(data), data.hex())
                await self._receive_packet_queue.put(data)
            except Exception as ex:
                _LOGGER.error('reader error, %s', ex)
                self._loop.create_task(self._async_reconnect())
                break
        _LOGGER.debug('reader end')

    async def _async_writer(self):
        """Socket write packet"""
        _LOGGER.debug('writer start')
        while self.connected:
            try:
                packet = await asyncio.wait_for(self._send_packet_queue.get(),
                                                timeout=_QUEUE_WAIT_TIMEOUT)
                self._writer.write(packet)
                await self._writer.drain()
                _LOGGER.debug('Send [%d]: %s', len(packet), packet.hex())
                self._send_packet_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as ex:
                _LOGGER.error('writer error, %s', ex)
                self._loop.create_task(self._async_reconnect())
                break
        _LOGGER.debug('writer end')

    async def _async_wait_for_disconnect(self):
        """disconnect and task exit wait"""
        self.disconnect()
        if self._wait_tasks is None:
            return
        await self._wait_tasks
        self._wait_tasks = None

    def disconnect(self):
        """disconnect"""
        if not self.connected:
            return
        self.connected = False
        if not self._loop.is_closed():
            self._writer.close()
        self._loop.create_task(self.async_on_disconnected())

    def __del__(self):
        self.disconnect()
