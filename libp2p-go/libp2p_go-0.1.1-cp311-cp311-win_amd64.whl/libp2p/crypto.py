import enum
from typing import Self
from ctypes import *
from libp2p.utils import *


lib = load_library()


class KeyType(AutoInt):
    RSA = enum.auto()
    Ed25519 = enum.auto()
    Secp256k1 = enum.auto()
    ECDSA = enum.auto()


class PrivKey(SimpleFreeMixin):
    lib.privkey_delete.argtypes = [c_size_t, ]
    _FREE = lib.privkey_delete
    lib.crypto_marshalPrivateKey.argtypes = [c_size_t, ]
    lib.crypto_marshalPrivateKey.restype = MsgpackBody
    _MARSHAL = lib.crypto_marshalPrivateKey
    lib.crypto_unmarshalPrivateKey.argtypes = [c_size_t, POINTER(c_ubyte), ]
    lib.crypto_unmarshalPrivateKey.restype = MsgpackBody
    _UNMARSHAL = lib.crypto_unmarshalPrivateKey
    lib.peer_idFromPrivateKey.argtypes = [c_size_t, ]
    lib.peer_idFromPrivateKey.restype = MsgpackBody
    _ID_FROM_PRIVATE_KEY = lib.peer_idFromPrivateKey

    def __init__(self, handle: int):
        self.handle = handle

    def marshal(self) -> bytes:
        result: MsgpackBody = self._MARSHAL(self.handle)
        result.raise_error()
        return result.bytes.first()

    @classmethod
    def unmarshal(cls, data: bytes) -> Self:
        buffer = (c_ubyte * len(data)).from_buffer(bytearray(data))
        result: MsgpackBody = cls._UNMARSHAL(len(data), buffer)
        result.raise_error()
        return PrivKey(result.handles.first())

    def peer_id(self) -> str:
        result: MsgpackBody = self._ID_FROM_PRIVATE_KEY(self.handle)
        result.raise_error()
        return result.strings.first()


class PubKey(SimpleFreeMixin):
    lib.pubkey_delete.argtypes = [c_size_t, ]
    _FREE = lib.pubkey_delete
    lib.crypto_marshalPublicKey.argtypes = [c_size_t, ]
    lib.crypto_marshalPublicKey.restype = MsgpackBody
    _MARSHAL = lib.crypto_marshalPublicKey
    lib.crypto_unmarshalPublicKey.argtypes = [c_size_t, POINTER(c_ubyte), ]
    lib.crypto_unmarshalPublicKey.restype = MsgpackBody
    _UNMARSHAL = lib.crypto_unmarshalPublicKey
    lib.peer_idFromPublicKey.argtypes = [c_size_t, ]
    lib.peer_idFromPublicKey.restype = MsgpackBody
    _ID_FROM_PUBLIC_KEY = lib.peer_idFromPublicKey

    def __init__(self, handle: int):
        self.handle = handle

    def marshal(self) -> bytes:
        result: MsgpackBody = self._MARSHAL(self.handle)
        result.raise_error()
        return result.bytes.first()

    @classmethod
    def unmarshal(cls, data: bytes) -> Self:
        buffer = (c_ubyte * len(data)).from_buffer(bytearray(data))
        result: MsgpackBody = cls._UNMARSHAL(len(data), buffer)
        result.raise_error()
        return PubKey(result.handles.first())

    def peer_id(self) -> str:
        result: MsgpackBody = self._ID_FROM_PUBLIC_KEY(self.handle)
        result.raise_error()
        return result.strings.first()


lib.crypto_generateKeyPairWithReader.argtypes = [c_longlong, c_longlong, c_longlong, ]
lib.crypto_generateKeyPairWithReader.restype = MsgpackBody
_GENERATE_KEYPAIR_WITH_READER = lib.crypto_generateKeyPairWithReader
lib.crypto_generateKeyPair.argtypes = [c_longlong, c_longlong, ]
lib.crypto_generateKeyPair.restype = MsgpackBody
_GENERATE_KEYPAIR = lib.crypto_generateKeyPair


def crypto_generate_keypair_with_reader(typ: KeyType, bits: int, randseed: int) -> tuple[PrivKey, PubKey]:
    result: MsgpackBody = _GENERATE_KEYPAIR_WITH_READER(typ.value, bits, randseed)
    result.raise_error()
    handles = result.handles
    priv, pub = handles.take(2)
    return PrivKey(priv), PubKey(pub)


def crypto_generate_keypair(typ: KeyType, bits: int) -> tuple[PrivKey, PubKey]:
    result: MsgpackBody = _GENERATE_KEYPAIR(typ.value, bits)
    result.raise_error()
    handles = result.handles
    priv, pub = handles.take(2)
    return PrivKey(priv), PubKey(pub)


__all__ = [
    'KeyType',
    'PrivKey',
    'PubKey',
    'crypto_generate_keypair_with_reader',
    'crypto_generate_keypair',
]
