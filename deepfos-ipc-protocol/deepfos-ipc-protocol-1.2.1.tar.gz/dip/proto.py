import json
import pickle
import struct
import typing
import uuid
from io import BytesIO

from dip import errors

read_uint32 = struct.Struct('!I').unpack
to_uint32 = struct.Struct('!I').pack
read_uint16 = struct.Struct('!H').unpack
to_uint16 = struct.Struct('!H').pack
read_uint8 = struct.Struct('!B').unpack

U32 = 0xFFFFFFFF


class Protocol:
    registry: typing.Dict[int, typing.Type['Protocol']] = {}

    if typing.TYPE_CHECKING:
        MSG_TYPE = b''

    @classmethod
    def decode(cls, buf: bytes) -> typing.Any:
        return cls._decode(buf[5:])

    @classmethod
    def _decode(cls, buf: bytes) -> typing.Any:
        raise NotImplemented

    @classmethod
    def _encode(cls, data: typing.Any) -> bytes:
        raise NotImplemented

    @classmethod
    def encode(cls, data: typing.Any) -> bytes:
        buf = cls._encode(data)
        if (buf_len := len(buf)) > U32:
            raise errors.ProtoEncodeError(
                f'Message ({buf_len}) exceeds max length ({U32}).')
        return cls.MSG_TYPE + to_uint32(len(buf)) + buf

    def __init_subclass__(cls, mtype: bytes = None, **kwargs):
        if mtype is not None:
            m_ord = read_uint8(mtype)[0]
            if m_ord in cls.registry:
                raise errors.DuplicateProtoError(
                    f'Cannot set mtype {mtype} for {cls} because '
                    f'it has been registered by {cls.registry[m_ord]}.')
            cls.MSG_TYPE = mtype
            cls.registry[m_ord] = cls

    @classmethod
    def unregister(cls, protocol: typing.Type['Protocol']):
        cls.registry.pop(read_uint8(protocol.MSG_TYPE)[0], None)

    @classmethod
    def dispatch(cls, mtype: int) -> typing.Type['Protocol']:
        if mtype in cls.registry:
            return cls.registry[mtype]

        raise errors.UnsupportedProtoError(
            f'No protocol found in registry for message type: {mtype}')


class _StringProtocol(Protocol):
    @classmethod
    def _decode(cls, buf: bytes) -> str:
        return buf.decode('utf8')

    @classmethod
    def _encode(cls, data: str) -> bytes:
        return data.encode('utf8')


class StdoutProtocol(_StringProtocol, mtype=b'O'):
    pass


class StderrProtocol(_StringProtocol, mtype=b'E'):
    pass


class PickleProtocl(Protocol, mtype=b'P'):
    @classmethod
    def _decode(cls, buf: bytes) -> typing.Any:
        return pickle.loads(buf)

    @classmethod
    def _encode(cls, data: typing.Any) -> bytes:
        return pickle.dumps(data, protocol=-1)


class JsonProtocol(Protocol, mtype=b'J'):
    @classmethod
    def _decode(cls, buf: bytes) -> typing.Any:
        return json.load(BytesIO(buf))

    @classmethod
    def _encode(cls, data: typing.Any) -> bytes:
        return json.dumps(data, ensure_ascii=False).encode('utf8')


class DictProtocol(Protocol, mtype=b'D'):
    VALID_KEYS = ()

    @classmethod
    def _decode(cls, buf: bytes) -> typing.Any:
        return dict(cls._iter_record(buf))  # noqa

    @classmethod
    def _iter_record(cls, buf: bytes) -> typing.Tuple[str, str]:
        stream = BytesIO(buf)
        key_len = len(cls.VALID_KEYS)

        while key := stream.read(2):
            idx = read_uint16(key)[0]
            if idx >= key_len:
                raise errors.ProtoDecodeError(
                    f'Field index {idx} exceeds max length ({key_len}).')
            val_len = read_uint32(stream.read(4))[0]
            val_bytes = stream.read(val_len)
            if len(val_bytes) < val_len:
                raise errors.ProtoDecodeError(
                    f'Not enough bytes to read, '
                    f'expect: {val_len}, got: {len(val_bytes)}')

            yield cls.VALID_KEYS[idx], val_bytes.decode('utf8')

    @classmethod
    def _iter_buf(cls, data: typing.Dict[str, str]):
        try:
            for k, v in data.items():
                yield to_uint16(cls.VALID_KEYS.index(k))
                str_encode = v.encode('utf8')
                yield to_uint32(len(str_encode))
                yield str_encode
        except ValueError:
            raise errors.ProtoEncodeError(
                f'Field {k!r} has not been registered, '  # noqa
                f'valid fields are {cls.VALID_KEYS}')

    @classmethod
    def _encode(cls, data: typing.Dict[str, str]) -> bytes:
        return b''.join(cls._iter_buf(data))


class ListProtocol(Protocol):
    element_proto: typing.Type[Protocol]

    @classmethod
    def _decode(cls, buf: bytes) -> typing.List[typing.Any]:
        return list(cls._iter_item(buf))

    @classmethod
    def _iter_item(cls, buf: bytes) -> typing.Any:
        stream = BytesIO(buf)
        ele_mtype = cls.element_proto.MSG_TYPE

        while mtype := stream.read(1):
            if mtype != ele_mtype:
                raise errors.ProtoDecodeError(
                    f'Invalid element for {mtype}, expect {ele_mtype}')

            val_len = read_uint32(stream.read(4))[0]
            val_bytes = stream.read(val_len)
            yield cls.element_proto._decode(val_bytes)

    @classmethod
    def _encode(cls, data: typing.List[typing.Any]) -> bytes:
        return b''.join(
            cls.element_proto.encode(item)
            for item in data
        )


class HeaderProto(DictProtocol, mtype=b'H'):
    VALID_KEYS = ('header', )


class SubtaskOutProto(DictProtocol, mtype=b'o'):
    VALID_KEYS = ('arg', 'subtask_out')


class SubtaskErrorProto(DictProtocol, mtype=b'e'):
    VALID_KEYS = ('arg', 'subtask_err')


class TaskUpdateProto(ListProtocol, mtype=b'U'):
    element_proto = JsonProtocol


class TaskUpdateProtoV2(ListProtocol, mtype=b'I'):
    element_proto = JsonProtocol


class SetConnectionIdProto(Protocol, mtype=b'\x1d'):
    @classmethod
    def _decode(cls, buf: bytes) -> uuid.UUID:
        return uuid.UUID(bytes=buf)

    @classmethod
    def _encode(cls, data: uuid.UUID) -> bytes:
        return data.bytes
