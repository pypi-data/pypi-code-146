import time

from typing import Union, Optional
from robertcommonio.system.io.socket import SocketType, SocketConfig, SocketAccessor, SocketHandler, IOTNetwork, IOTNetMessage, IOTNetResult, format_bytes


def call_back(data):
    print(data)


def test_tcp_client():
    config = SocketConfig(MODE=SocketType.TCP_CLIENT, HOST='0.0.0.0', PORT=1000, CALL_BACK={})
    accessor = SocketAccessor(config)
    accessor.start()


def test_tcp_server():
    config = SocketConfig(MODE=SocketType.TCP_SERVER, HOST='0.0.0.0', PORT=9500)
    accessor = SocketAccessor(config)
    accessor.start(False)
    while True:
        time.sleep(1)


def test_s7_client():
    config = SocketConfig(MODE=SocketType.TCP_CLIENT, HOST='0.0.0.0', PORT=1000, CALL_BACK={})
    accessor = SocketAccessor(config)
    accessor.start()


class IOTClientMessage(IOTNetMessage):

    def get_head_length(self) -> int:
        '''协议头数据长度，也即是第一次接收的数据长度'''
        return 2

    def get_content_length(self) -> int:
        '''二次接收的数据长度'''
        if self.heads is not None:
            return self.heads[1]
        else:
            return 0

    def check_head(self) -> bool:
        '''回复报文校验'''
        if self.heads is not None:
            if self.heads[0] == 0xA0:
                return True
            else:
                return False
        else:
            return False

    def check_response(self) -> bool:
        '''回复报文校验'''
        if self.heads is not None:
            if self.heads[0] == 0xA0 and self.create_sum((self.heads + self.contents)[0:-1]) == self.contents[-1]:
                return True
            else:
                return False
        else:
            return False

    def create_sum(self, datas: bytes):
        data = sum(datas) & 0xFF
        data = 255 - data if data > 0 else 255 + data
        return data + 1


class IOTServerMessage(IOTNetMessage):

    def get_head_length(self) -> int:
        '''协议头数据长度，也即是第一次接收的数据长度'''
        return 1024


class IOTClient(IOTNetwork):

    '''timeout为None 不超时'''
    def __init__(self, host: str, port: int, timeout: Optional[int] = 5):
        super().__init__(host, port, timeout)

    def get_net_msg(self):
        return IOTClientMessage()

    def extra_on_connect(self, socket):
        '''连接上服务器后需要进行的二次握手操作'''
        # 返回成功的信号
        return IOTNetResult.create_success()

    def extra_on_disconnect(self, socket):
        return IOTNetResult.create_success()

    def ping(self):
        return self.get_socket().is_success

    def read(self):
        read = self.read_server(None)
        return read


class IOTServer(IOTNetwork):
    '''timeout为None 不超时'''

    def __init__(self, host: str, port: int, timeout: Optional[int] = 5, size: int = 500):
        super().__init__(host, port, timeout, size)

    def get_net_msg(self):
        return IOTServerMessage()

    def extra_on_connect(self, socket):
        '''连接上服务器后需要进行的二次握手操作'''
        # 返回成功的信号
        print(f"connect({socket})")
        return IOTNetResult.create_success()

    def extra_on_close(self, socket):
        print(f"close({socket})")
        return IOTNetResult.create_success()

    def extra_on_disconnect(self, socket):
        print(f"disconnect({socket})")
        return IOTNetResult.create_success()

    def extra_on_receive(self, socket, datas: bytes):
        print(f"recv({format_bytes(datas)})")

    def read(self):
        read = self.read_server(None)
        return read


def test_iot_client():
    client = IOTClient('127.0.0.1', 4001, None)
    while True:
        rt = client.read()
        if rt.is_success is True:
            print(format_bytes(rt.contents[0]))
        else:
            print(rt.msg)


def test_iot_server():
    server = IOTServer('0.0.0.0', 4001, None)
    server.start_server()
    while True:
        time.sleep(1)


test_iot_server()