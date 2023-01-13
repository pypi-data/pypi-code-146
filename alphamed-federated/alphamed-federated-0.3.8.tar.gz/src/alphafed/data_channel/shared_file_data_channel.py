"""通过共享文件方式传输数据的数据通道."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tempfile import TemporaryFile
from time import sleep
from typing import List, Optional, Union

import requests

from .. import logger
from ..contractor import (AcceptSharedFileSendingDataEvent,
                          ApplySharedFileSendingDataEvent,
                          DenySendingDataEvent, TaskMessageContractor)
from .data_channel import DataChannel, SendingError

__all__ = ['SharedFileDataChannel']


class SharedFileDataChannel(DataChannel):
    """共享文件数据传输通道."""

    def __init__(self, contractor: TaskMessageContractor) -> None:
        super().__init__()
        self.contractor = contractor

    def send_stream(self,
                    source: str,
                    target: Union[str, List[str]],
                    data_stream: bytes,
                    connection_timeout: int = 30,
                    timeout: int = 180) -> Optional[List[str]]:
        assert source and isinstance(source, str), f'invalid source ID: {source}'
        assert target and isinstance(target, (str, list)), f'invalid target ID: {target}'
        if isinstance(target, list):
            assert all(isinstance(_id, str) for _id in target), f'invalid target ID: {target}'
        else:
            target = [target]
        assert data_stream, 'must specify some data to send'
        assert isinstance(data_stream, bytes), 'data_stream must be a bytes object'
        assert isinstance(connection_timeout, int), 'connection_timeout must be an int value'
        assert timeout is None or isinstance(timeout, int), 'timeout must be None or an int value'
        if not timeout or timeout < 0:
            timeout = 0

        start_at = datetime.utcnow().timestamp()
        current = start_at
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self._do_send_stream,
                                 source=source,
                                 target=target,
                                 data_stream=data_stream,
                                 connection_timeout=connection_timeout)
        while not timeout or current - start_at < timeout:
            if future.done() and future.exception() is None:
                return future.result()
            elif future.done() and future.exception() is not None:
                raise future.exception()
            else:
                sleep(0.1)
                current = datetime.utcnow().timestamp()
        raise SendingError(f'timeout to sending data stream to {target}')

    def _do_send_stream(self,
                        source: str,
                        target: List[str],
                        data_stream: bytes,
                        connection_timeout: int = 30) -> None:
        """Perform sending data stream to a receiver.

        :args
            :source
                the ID of the data sender
            :target
                the ID list of the receiver
            :data_stream
                data_stream content
            :connection_timeout
                the timeout seconds to establish the connection
        """
        assert source and isinstance(source, str), f'invalid source ID: {source}'
        assert (
            target and isinstance(target, list) and all(isinstance(_id, str) for _id in target)
        ), f'invalid target ID: {target}'
        assert data_stream, 'must specify some data to send'
        assert isinstance(data_stream, bytes), 'data_stream must be a bytes object'
        assert isinstance(connection_timeout, int), 'connection_timeout must be an int value'

        with TemporaryFile() as tf:
            tf.write(data_stream)
            tf.seek(0)
            file_url = self.contractor.upload_file(fp=tf)

        session_id = self.contractor.apply_sending_data(source=source,
                                                        target=target,
                                                        file_url=file_url)

        # 监听 L1 返回的处理结果
        accepted = []
        rejected = []
        for _event in self.contractor.contract_events(timeout=connection_timeout):
            if isinstance(_event, DenySendingDataEvent) and _event.session_id == session_id:
                rejected.append(_event.rejecter)
                logger.warn(f'Sending data application refused by {_event.rejecter}.')
            elif (
                isinstance(_event, AcceptSharedFileSendingDataEvent)
                and _event.session_id == session_id
            ):
                accepted.append(_event.receiver)
            else:
                continue

            if len(accepted) + len(rejected) == len(target):
                break

        logger.debug('sending data stream complete')
        return accepted

    def receive_stream(self,
                       apply_event: ApplySharedFileSendingDataEvent,
                       receiver: str = None) -> bytes:
        assert (
            apply_event and isinstance(apply_event, ApplySharedFileSendingDataEvent)
        ), f'Must specify the apply event to exact infomation: {apply_event} .'
        assert (
            receiver and isinstance(receiver, str)
        ), f"Must specify the receiver's ID: {receiver} ."

        self.contractor.accept_sending_data(target=apply_event.source,
                                            session_id=apply_event.session_id,
                                            receiver=receiver)
        resp = requests.get(apply_event.file_url)
        return resp.content
