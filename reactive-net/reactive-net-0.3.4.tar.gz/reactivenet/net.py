import struct
import ipaddress
import asyncio
import contextlib

from .enums import ReactiveCommand, ReactiveResult


class Error(Exception):
    pass


class Message():
    """
    Message: format <size u16><payload>
    """

    def __init__(self, payload=bytearray()):
        self.payload = payload

    def pack(self):
        """
        form the byte array according to the format
        """
        size = struct.pack('!H', len(self.payload))

        return size + self.payload

    @staticmethod
    async def read(reader):
        """
        read from an asyncio StreamReader
        """

        # read len
        size = await reader.readexactly(2)
        size = struct.unpack('!H', size)[0]

        # payload
        payload = bytearray()
        if size > 0:
            payload = await reader.readexactly(size)

        return Message(payload)


class ResultMessage():
    """
    ResultMessage: format <code u8><size u16><payload>
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def pack(self):
        """
        form the byte array according to the format
        """
        code = struct.pack('!B', self.code)

        return code + self.message.pack()

    def ok(self):
        """
        check if the command succeeded
        """
        return self.code == ReactiveResult.Ok

    @staticmethod
    async def read(reader):
        """
        read from an asyncio StreamReader
        """

        # read result code
        code = await reader.readexactly(1)
        code = struct.unpack('!B', code)[0]

        try:
            code = ReactiveResult(code)
        except ValueError:
            raise Error("Result code not valid")

        message = await Message.read(reader)

        return ResultMessage(code, message)


class CommandMessage():
    """
    CommandMessage: format <code u8><size u16><payload>
    """

    def __init__(self, code, message, ip=None, port=None):
        self.code = code
        self.message = message
        self.__ip = ip
        self.__port = port

    @property
    def ip(self):
        """
        get destination IP
        raises exception if the IP is not specified
        """
        if self.__ip is None:
            raise Error("IP address not specified")

        return self.__ip

    @property
    def port(self):
        """
        get destination port
        raises exception if the port is not specified
        """

        if self.__port is None:
            raise Error("TCP port not specified")

        return self.__port

    def pack(self):
        """
        form the byte array according to the format
        """

        code = struct.pack('!B', self.code)

        return code + self.message.pack()

    def set_dest(self, ip, port):
        """
        set destination ip and port
        """

        self.__ip = ip
        self.__port = port

    def has_response(self):
        """
        check if the command will have a response
        """
        return self.code.has_response()

    async def send(self):
        """
        send the command to the destination IP and port
        """
        _, writer = await asyncio.open_connection(str(self.ip), self.port)

        with contextlib.closing(writer):
            writer.write(self.pack())
            await writer.drain()

    async def send_wait(self):
        """
        send the command to the destination IP and port
        also wait for the response
        raises exception if the command does not have a response
        """

        if not self.has_response():
            raise Error("This command has not response: call send() instead")

        reader, writer = await asyncio.open_connection(str(self.ip), self.port)

        with contextlib.closing(writer):
            writer.write(self.pack())
            await writer.drain()
            return await ResultMessage.read(reader)

    @staticmethod
    async def read(reader):
        """
        read from an asyncio StreamReader
        """

        # read command code
        code = await reader.readexactly(1)
        code = struct.unpack('!B', code)[0]

        try:
            code = ReactiveCommand(code)
        except ValueError:
            raise Error("Command code not valid")

        message = await Message.read(reader)

        return CommandMessage(code, message)

    @staticmethod
    async def read_with_ip(reader):
        """
        read from an asyncio StreamReader
        also read ip and port from reader, that are sent before the command
        """
        ip = await reader.readexactly(4)
        ip = struct.unpack('!I', ip)[0]
        ip = ipaddress.ip_address(ip)

        port = await reader.readexactly(2)
        port = struct.unpack('!H', port)[0]

        cmd = await CommandMessage.read(reader)
        cmd.set_dest(ip, port)

        return cmd


class CommandMessageLoad(CommandMessage):
    """
    CommandMessageLoad: since the loading process is different for each
                        architecture, this class receives the payload already
                        formed by the caller. The code is fixed: ReactiveCommand.Load
    Inherited: has_response(), send() and send_wait() from CommandMessage
    """

    def __init__(self, payload, ip, port):
        super().__init__(ReactiveCommand.Load, None, ip, port)
        self.payload = payload

    def pack(self):
        """
        form the byte array according to the format
        """
        code = struct.pack('!B', self.code)

        return code + self.payload
