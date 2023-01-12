from .buffer import Buffer


class Packet:
    header: bytes
    body: bytes

    HEADER_LENGTH: int

    def __init__(self, header: bytes = b'', body: bytes = b''):
        self.header = header
        self.body = body

    def __bytes__(self):
        return self.header + self.body

    @classmethod
    def from_buffer(cls, buffer: Buffer):
        header, body = buffer.read(cls.HEADER_LENGTH), buffer.get_buffer()
        return cls(header, body)

    def is_valid(self) -> bool:
        pass

    def buffer(self, skip_header: bool = True) -> Buffer:
        buffer = Buffer(self.header + self.body)

        if skip_header:
            buffer.skip(self.HEADER_LENGTH)

        return buffer


class PrincipalPacket(Packet):
    HEADER_LENGTH = 6

    def is_valid(self) -> bool:
        return self.header == b'\xff\xff\xff\xff\x66\x0a' and len(self.body) % 6 == 0
