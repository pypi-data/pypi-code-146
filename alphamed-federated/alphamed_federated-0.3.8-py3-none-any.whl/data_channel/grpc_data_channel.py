"""通过 GRPC 连接传输数据的数据通道."""

import random
import socket
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime
from tempfile import TemporaryFile
from threading import Event
from time import sleep
from typing import IO, Tuple

import grpc
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from .. import logger
from ..contractor import (AcceptGRPCSendingDataEvent, ApplyGRPCSendingDataEvent,
                          DenySendingDataEvent, TaskMessageContractor)
from ..utils import retry
from . import data_channel_pb2, data_channel_pb2_grpc
from .data_channel import DataChannel, SendingError

__all__ = ['InvalidPortNumber', 'GRPCDataChannel']


class InvalidPortNumber(Exception):
    ...


class GRPCDataChannel(DataChannel):
    """GRPC 数据传输通道."""

    BLOCK_SIZE = 2 ** 20

    INT_BYTES_ORDER = 'big'
    LEN_BYTES = 4

    def __init__(self, contractor: TaskMessageContractor) -> None:
        super().__init__()
        self.contractor = contractor
        self._ports = [i for i in range(21010, 21020)]  # TODO configure port range

    def send_stream(self,
                    source: str,
                    target: str,
                    data_stream: bytes,
                    connection_timeout: int = 30,
                    timeout: int = 60) -> None:
        assert source and isinstance(source, str), f'invalid source ID: {source}'
        assert target and isinstance(target, str), f'GRPC only support single target: {target}'
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
                return
            elif future.done() and future.exception() is not None:
                raise future.exception()
            else:
                sleep(0.1)
                current = datetime.utcnow().timestamp()
        raise SendingError(f'timeout to sending data stream to {target}')

    def _do_send_stream(self,
                        source: str,
                        target: str,
                        data_stream: bytes,
                        connection_timeout: int = 30) -> None:
        """Perform sending data stream to a receiver.

        Args:
            source:
                the ID of the data sender.
            target:
                the ID of the receiver.
            data_stream:
                data_stream content.
            connection_timeout:
                the timeout seconds to establish the connection.
        """
        assert source and isinstance(source, str), f'invalid source ID: {source}'
        assert target and isinstance(target, str), f'invalid target ID: {target}'
        assert data_stream, 'must specify some data to send'
        assert isinstance(data_stream, bytes), 'data_stream must be a bytes object'
        assert isinstance(connection_timeout, int), 'connection_timeout must be an int value'

        private_key, public_key = self._new_asymmetric_key_pair()

        session_id = self.contractor.apply_sending_data(source=source,
                                                        target=target,
                                                        public_key=public_key)

        # 监听 L1 返回的处理结果
        receiver_key, port = None, None
        for _event in self.contractor.contract_events(timeout=connection_timeout):
            if isinstance(_event, DenySendingDataEvent) and _event.session_id == session_id:
                raise SendingError('sending application refused.')
            elif isinstance(_event, AcceptGRPCSendingDataEvent) and _event.session_id == session_id:
                receiver_key = _event.public_key
                cipher_port = _event.port
                port = self._decrypt_port(private_key=private_key, cipher_port=cipher_port)
                break
            else:
                continue
        if not receiver_key or not port:
            err_msg = f'Failed to handshake in session {session_id}: {receiver_key=}; {port=}'
            logger.error(err_msg)
            raise SendingError(err_msg)

        target_addr = self.contractor.query_address(target=target)
        if not target_addr:
            err_msg = f'Failed to get target address for {target}.'
            logger.error(err_msg)
            raise SendingError(err_msg)

        logger.debug(f'trying to establish a connection to {target_addr}:{port}')
        self._send_stream_by_grpc_channel(target_addr=target_addr,
                                          port=port,
                                          session_id=session_id,
                                          receiver_key=receiver_key,
                                          data_stream=data_stream)
        logger.debug('sending data stream complete')

    @retry(times=7)
    def _send_stream_by_grpc_channel(self,
                                     target_addr: str,
                                     port: int,
                                     session_id: str,
                                     receiver_key: bytes,
                                     data_stream: bytes):
        """Do send data stream by a grpc channel."""
        with grpc.insecure_channel(f'{target_addr}:{port}',
                                   options=(('grpc.enable_http_proxy', 0),)) as ch:
            stub = data_channel_pb2_grpc.GRPCDataChannelStub(channel=ch)
            stub.SendStream(self._data_frames(session_id=session_id,
                                              receiver_key=receiver_key,
                                              data=data_stream))

    def _new_asymmetric_key_pair(self) -> Tuple[bytes, bytes]:
        """Generate a pair of asymmetric key.

        :return (private_key, public_key)
        """
        key_bits = 1024
        key = RSA.generate(key_bits)
        private_key = key.export_key()
        public_key = key.public_key().export_key()
        return private_key, public_key

    def _decrypt_port(self, private_key: bytes, cipher_port: bytes) -> int:
        """Decrypt the port number for connecting."""
        rsa_key = RSA.import_key(private_key)
        cipher_ras = PKCS1_OAEP.new(rsa_key)
        port_byte = cipher_ras.decrypt(cipher_port)
        port = int.from_bytes(port_byte, self.INT_BYTES_ORDER)
        if port <= 1024 or port > 65535:
            err_msg = f'invalid port number: {port}'
            logger.error(err_msg)
            raise InvalidPortNumber(err_msg)
        return port

    def _data_frames(self, session_id: str, receiver_key: bytes, data: bytes) -> bytes:
        """生成实际传输的数据流，并拆分成大小合适的块，以方便传输.

        :args
            :receiver_key
                the public key of the receiver
            :data
                the raw data stream to be send
        """
        try:
            rsa_key = RSA.import_key(receiver_key)
            cipher_ras = PKCS1_OAEP.new(rsa_key)
            session_key = get_random_bytes(16)
            cipher_key = cipher_ras.encrypt(session_key)

            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            nonce = cipher_aes.nonce
            cipher_data, digest = cipher_aes.encrypt_and_digest(data)

            data_stream = b''
            key_len = len(cipher_key)
            data_stream += key_len.to_bytes(self.LEN_BYTES, self.INT_BYTES_ORDER) + cipher_key
            nonce_len = len(nonce)
            data_stream += nonce_len.to_bytes(self.LEN_BYTES, self.INT_BYTES_ORDER) + nonce
            digest_len = len(digest)
            data_stream += digest_len.to_bytes(self.LEN_BYTES, self.INT_BYTES_ORDER) + digest
            data_stream += cipher_data
            num_frames = len(data_stream) // self.BLOCK_SIZE + 1
            for i in range(num_frames):
                start = i * self.BLOCK_SIZE
                end = start + self.BLOCK_SIZE
                _frame = data_stream[start:end]
                logger.debug(f'return a stream request with data length {len(_frame)}')
                yield data_channel_pb2.SendStreamRequest(session_id=session_id,
                                                         len=len(_frame),
                                                         data=_frame)
            logger.debug('the whole data stream is popped up')
        except Exception as err:
            logger.exception(err)
            raise err

    def receive_stream(self,
                       apply_event: ApplyGRPCSendingDataEvent,
                       receiver: str = None) -> bytes:
        class GRPCDataChannelService:
            """GRPC Service Implementation."""

            def __init__(self, session_id: str, fp: IO, stop_event: Event) -> None:
                self.session_id = session_id
                self.fp = fp
                self._stop_event = stop_event

            def SendStream(self, request_iter, context):
                """Send data stream API."""
                data_slices = []
                for _slice in request_iter:
                    if self.session_id != _slice.session_id:
                        continue
                    if _slice.len and _slice.len > 0:  # 数据分片
                        logger.debug(f'received a data slice of length {len(_slice.data)}')
                        assert _slice.len == len(_slice.data), 'data is broken'
                        data_slices.append(_slice.data)

                data = b''.join(data_slices)
                self.fp.write(data)
                logger.debug(f'received data stream of length {len(data)}')
                self._stop_event.set()
                return data_channel_pb2.SendStreamResponse(received_len=len(data))

        assert apply_event, 'must specify the apply event to exact infomation.'

        # prepare and hand-shake
        port, private_key = self._prepare_for_connecting(
            session_id=apply_event.session_id,
            source=apply_event.source,
            sender_key=apply_event.public_key
        )
        logger.debug(f'port {port} is picked up')

        # setup listening server
        stop_event = Event()
        with TemporaryFile() as fp:
            server = grpc.server(ThreadPoolExecutor(max_workers=1))
            data_channel_pb2_grpc.add_GRPCDataChannelServicer_to_server(
                servicer=GRPCDataChannelService(session_id=apply_event.session_id,
                                                fp=fp,
                                                stop_event=stop_event),
                server=server
            )
            server.add_insecure_port(f'0.0.0.0:{port}')
            server.start()
            logger.debug(f'waiting for receiving data on port {port}')

            stop_event.wait()
            server.stop(grace=2)
            fp.seek(0)
            data = fp.read()

        # decrypt and verify the data received
        data = self._decrypt_and_verify_data(encrypted_data=data, private_key=private_key)
        logger.debug('receiving data stream complete')
        return data

    def _prepare_for_connecting(self,
                                session_id: str,
                                source: str,
                                sender_key: bytes) -> Tuple[int, bytes]:
        """Prepare and return parameters which will be used for connecting later.

        :args
            :session_id
                the session id of current data transmission
            :source
                the source id of current data transmission
            :sender_key
                the public key of the data sender
        :return
            :port
                the port number used for connecting later
            :private_key
                self private key for a data sending session
        """
        rsa_kay = RSA.import_key(sender_key)
        cipher_rsa = PKCS1_OAEP.new(rsa_kay)
        port = self._select_free_port()
        port_bytes = port.to_bytes(self.LEN_BYTES, self.INT_BYTES_ORDER)
        cipher_port = cipher_rsa.encrypt(port_bytes)
        private_key, public_key = self._new_asymmetric_key_pair()
        self.contractor.accept_sending_data(target=source,
                                            session_id=session_id,
                                            public_key=public_key,
                                            cipher_port=cipher_port)
        return port, private_key

    def _select_free_port(self) -> int:
        """Select a free port for connection."""
        random.shuffle(self._ports)
        for _port in self._ports:
            try:
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                    s.bind(('', _port))
                    return _port
            except Exception:
                logger.exception(f'failed to bind port {_port}')
                pass
        err_msg = 'there is no free port available.'
        logger.error(err_msg)
        raise SendingError(err_msg)

    def _decrypt_and_verify_data(self, encrypted_data: bytes, private_key: bytes) -> bytes:
        """Decrypt and verify the data received.

        :args
            :encrypted_data
                the encrypted data received
            :session_key
                the session key used for decrypting
        :return
            the raw data decrypted
        """
        archor = 0
        key_len = int.from_bytes(encrypted_data[archor:(archor + self.LEN_BYTES)],
                                 self.INT_BYTES_ORDER)
        archor += self.LEN_BYTES
        cipher_key = encrypted_data[archor:(archor + key_len)]
        archor += key_len
        nonce_len = int.from_bytes(encrypted_data[archor:(archor + self.LEN_BYTES)],
                                   self.INT_BYTES_ORDER)
        archor += self.LEN_BYTES
        nonce = encrypted_data[archor:(archor + nonce_len)]
        archor += nonce_len
        digest_len = int.from_bytes(encrypted_data[archor:(archor + self.LEN_BYTES)],
                                    self.INT_BYTES_ORDER)
        archor += self.LEN_BYTES
        digest = encrypted_data[archor:(archor + digest_len)]
        archor += digest_len
        data = encrypted_data[archor:]

        rsa_key = RSA.import_key(private_key)
        cipher_ras = PKCS1_OAEP.new(rsa_key)
        session_key = cipher_ras.decrypt(cipher_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(data, digest)
        return data
