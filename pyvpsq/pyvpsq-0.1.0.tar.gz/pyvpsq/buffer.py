import struct

from .exceptions import Error


class Buffer:
    data: bytes
    length: int
    index: int

    def __init__(self, data: bytes = b''):
        self.data = data
        self.length = len(data)
        self.index = 0

    def get_buffer(self) -> bytes:
        return self.data[self.index:]

    def read(self, length: int = 1) -> bytes:
        if self.index + length > self.length:
            raise Error('Attempt to read beyond buffer length')

        data = self.data[self.index:self.index + length]
        self.index += length

        return data

    def skip(self, length: int = 1) -> None:
        self.index += length

    def has(self, length: int = 1) -> bool:
        return self.index + length <= self.length

    def read_c_bytestring(self) -> bytes:
        v = bytes()
        while (b := self.read(1)) != b'\x00':
            v += b
        return v

    def read_c_string(self, encoding: str = 'utf-8') -> str:
        return self.read_c_bytestring().decode(encoding, errors='replace')

    def read_uchar(self) -> int:
        v, *_ = struct.unpack('>B', self.read(1))
        return v

    def read_ushort(self) -> int:
        v, *_ = struct.unpack('>H', self.read(2))
        return v

    def read_uint(self) -> int:
        v, *_ = struct.unpack('>I', self.read(4))
        return v

    def read_ip(self) -> str:
        v = self.read(4)
        return "%d.%d.%d.%d" % struct.unpack(">BBBB", v)

    def write(self, v: bytes) -> None:
        self.data += v
        self.length += len(v)

    def write_c_bytestring(self, v: bytes) -> None:
        self.write(v + b'\x00')

    def write_c_string(self, v: str, encoding: str = 'utf-8') -> None:
        self.write_c_bytestring(v.encode(encoding))

    def write_uchar(self, v: int) -> None:
        self.write(struct.pack('>B', v))

    def write_ushort(self, v: int) -> None:
        self.write(struct.pack('>H', v))

    def write_uint(self, v: int) -> None:
        self.write(struct.pack('>I', v))
