import gzip

from ..interfaces.deserializer import Deserializer
from ..interfaces.serializer import Serializer


class GzipSerializer(Serializer[bytes, bytes]):
    def serialize(self, value: bytes) -> bytes:
        return gzip.compress(value)


class GzipDeserializer(Deserializer[bytes, bytes]):
    def deserialize(self, value: bytes) -> bytes:
        return gzip.decompress(value)
