# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import asyncio
import logging
from typing import Any, Optional, Tuple

import aiohttp

from ..batch_utils import Batch
from ..connection import send_asyncio_batch_requests
from ..exceptions import AsyncioSenderNoConnected
from ..logging_messages import ASYNCIO_SENDER_HARD_SHUTDOWN, BATCH_SENDING_EXCEPTION
from .base import CLOSE_MESSAGE, BaseSender, batch_endpoint_url, model_base_event

LOGGER = logging.getLogger(__name__)


def get_asyncio_sender(
    api_key: str,
    server_address: str,
    model_name: str,
    model_version: str,
    max_batch_size: int,
    max_batch_time: int,
    batch_sending_timeout: int,
) -> "AsyncioSender":
    sender = AsyncioSender(
        api_key,
        server_address,
        model_name,
        model_version,
        max_batch_size,
        max_batch_time,
        batch_sending_timeout,
    )

    return sender


class AsyncioBackgroundSender:
    def __init__(
        self,
        api_key: str,
        server_address: str,
        model_name: str,
        model_version: str,
        queue: "asyncio.Queue[Any]",
        max_batch_size: int,
        max_batch_time: int,
        batch_sending_timeout: int,
    ):
        """A background coroutine that reads from the queue, add the items to the batch and sends
        them whenever the batch is ready to be sent. Can only be created only when an event loop is running.
        """
        self.api_key = api_key
        self.server_address = server_address
        self.base_event = model_base_event(model_name, model_version)
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.queue: "asyncio.Queue[Any]" = queue
        self.max_batch_time = max_batch_time
        self.batch = Batch(max_batch_size, self.max_batch_time)
        self.batch_sending_timeout = batch_sending_timeout

        self.stop_processing = False

        # Pre-compute URLs
        self.batch_endpoint = batch_endpoint_url(self.server_address)

    async def run(self) -> None:
        while True:
            stop = await self._loop()

            if stop is True:
                break

        # We force stop the processing of the queue
        await self._check_batch_sending()
        return

    async def _loop(self) -> bool:
        try:
            data = await asyncio.wait_for(self.queue.get(), timeout=self.max_batch_time)

            if data:
                if data is CLOSE_MESSAGE:
                    self.stop_processing = True
                    return True

                self._process_single_event(data)
        except asyncio.TimeoutError:
            pass

        await self._check_batch_sending()

        return False

    def _process_single_event(self, data: Any) -> None:
        to_send = self.base_event.copy()
        to_send.update(data)
        self.batch.append(to_send)

    async def _send_batch(self, batch: Any) -> None:
        async with aiohttp.ClientSession() as session:
            await send_asyncio_batch_requests(
                session,
                self.batch_endpoint,
                api_key=self.api_key,
                batch_sending_timeout=self.batch_sending_timeout,
                batch=batch,
            )

    async def _check_batch_sending(self) -> None:
        # This should only be called by the background sender coroutine, if not the batch could
        # become corrupted as its access not protected by a lock
        try:
            if self.batch.should_be_uploaded(self.stop_processing):
                batch = self.batch.get_and_clear()

                await send_asyncio_batch_requests(
                    self.session,
                    self.batch_endpoint,
                    api_key=self.api_key,
                    batch_sending_timeout=self.batch_sending_timeout,
                    batch=batch,
                )
        except Exception:
            LOGGER.error(BATCH_SENDING_EXCEPTION, exc_info=True)

    def close(self) -> None:
        """Force the AsyncioBackgroundSender to stop processing messages"""
        #
        self.stop_processing = True

        while True:
            try:
                data = self.queue.get_nowait()
                if data and data is not CLOSE_MESSAGE:
                    self._process_single_event(data)
            except asyncio.QueueEmpty:
                break

        asyncio.run(self._send_batch(self.batch.get_and_clear()))


class AsyncioSender(BaseSender):
    def __init__(
        self,
        api_key: str,
        server_address: str,
        model_name: str,
        model_version: str,
        max_batch_size: int,
        max_batch_time: int,
        batch_sending_timeout: int,
    ) -> None:
        self.sender_queue: Optional["asyncio.Queue[Any]"] = None
        # We need to wait for the asyncio event loop to be created
        self.background_sender: Optional[AsyncioBackgroundSender] = None
        self.background_task: Optional[asyncio.Task[None]] = None
        self.lock: Optional[asyncio.Lock] = None
        self.drain = False

        self.api_key = api_key
        self.server_address = server_address
        self.model_name = model_name
        self.model_version = model_version
        self.max_batch_time = max_batch_time
        self.max_batch_size = max_batch_size
        self.batch_sending_timeout = batch_sending_timeout

    def connect(self) -> None:
        if self.sender_queue is None:
            sender_queue: "asyncio.Queue[Any]" = asyncio.Queue()
            self.sender_queue = sender_queue
            self.background_sender = AsyncioBackgroundSender(
                self.api_key,
                self.server_address,
                self.model_name,
                self.model_version,
                self.sender_queue,
                self.max_batch_size,
                self.max_batch_time,
                self.batch_sending_timeout,
            )
            self.background_sender.queue = self.sender_queue

        if self.background_task is None:
            assert self.background_sender is not None
            self.background_task = asyncio.create_task(self.background_sender.run())

        if self.lock is None:
            self.lock = asyncio.Lock()

    def _check_connected(self) -> Tuple[asyncio.Lock, "asyncio.Queue[Any]"]:
        if self.lock is None or self.sender_queue is None:
            raise AsyncioSenderNoConnected()

        return self.lock, self.sender_queue

    async def put(self, item: Any) -> None:
        lock, queue = self._check_connected()
        async with lock:
            if not self.drain:
                await queue.put(item)

    def close(self) -> None:
        """Called during atexit but users should call join manually. In last resort, synchronously
        dequeu items and send it by recreating an asyncio Event Loop
        """
        if self.drain is True:
            return None
        else:
            self.drain = True

            need_to_clean = False

            if self.sender_queue is not None and self.sender_queue.qsize() > 0:
                need_to_clean = True

            if (
                self.background_sender is not None
                and len(self.background_sender.batch) > 0
            ):
                need_to_clean = True

            if need_to_clean is False:
                return None
            else:
                LOGGER.warning(
                    ASYNCIO_SENDER_HARD_SHUTDOWN
                )  # TODO: Add link to documentation page
                self.drain = True

                # If the sender_queue is not None, the background sender shouldn't be None either
                assert self.background_sender is not None
                self.background_sender.close()

    async def join(self, timeout: int) -> None:
        """Inform the background sender to stops processing after receiving the sentinel object and
        wait for the background sender to stop
        """
        try:
            lock, queue = self._check_connected()
        except AsyncioSenderNoConnected:
            # The AsyncioSender was not properly initialized, ignore
            return

        async with lock:
            if self.drain is False:
                self.drain = True

                queue.put_nowait(CLOSE_MESSAGE)

                # TODO: Handle asyncio cleaning
                if self.background_task is not None:
                    await asyncio.wait_for(self.background_task, timeout)
