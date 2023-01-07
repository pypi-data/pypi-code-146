import os
import abc
import enum
import asyncio
import platform
from ctypes import *
from functools import cached_property
import msgpack
from multiaddr import protocols
from multiaddr.exceptions import ProtocolExistsError

__LIB = None


def patch_multiaddr():
    try:
        protocols.add_protocol(protocols.Protocol(0x01CD, 'quic-v1', None))
    except ProtocolExistsError:
        return


patch_multiaddr()


def load_library():
    global __LIB
    if __LIB is not None:
        return __LIB
    current_path = __file__
    current_dir = os.path.dirname(current_path)
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    extend = "dll" if os_name == "windows" else "so"
    dl_name = f"libp2p-{os_name}_{arch}.{extend}"
    library_path = os.path.join(current_dir, "bin", dl_name)
    __LIB = cdll.LoadLibrary(library_path)
    return __LIB


class MsgpackList(list):
    def first(self):
        if len(self) < 1:
            raise ValueError(f'cannot take first elements, list is empty')
        return self[0]

    def take(self, n: int):
        if len(self) < n:
            raise ValueError(f'cannot take {n} elements, list length is {len(self)}')
        return self[:n]


class LibP2PError(ValueError):
    pass


class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

    @classmethod
    def new(cls, s: str | bytes):
        if isinstance(s, str):
            s = s.encode('utf8')
        return cls(s, len(s))


class MsgpackArg(GoString):
    @staticmethod
    def from_dict(d: dict):
        return MsgpackArg.new(msgpack.dumps(d))


class MsgpackBody(Structure):
    _fields_ = [("l", c_longlong), ("p", POINTER(c_char)), ]
    load_library().freePointer.argtypes = [c_char_p, ]
    FREE = load_library().freePointer

    def __del__(self):
        if self.p is not None:
            self.FREE(self.p)

    @cached_property
    def result(self) -> None | dict:
        if self.l and self.p:
            s = string_at(self.p, self.l)
            return msgpack.loads(s)
        else:
            return None

    @cached_property
    def handles(self) -> MsgpackList[int]:
        return MsgpackList(self.result.get('Handles', list()))

    @cached_property
    def strings(self) -> MsgpackList[str]:
        return MsgpackList(self.result.get('Strings', list()))

    @cached_property
    def bytes(self) -> MsgpackList[bytes]:
        return MsgpackList(self.result.get('Bytes', list()))

    @cached_property
    def integers(self) -> MsgpackList[int]:
        return MsgpackList(self.result.get('Integers', list()))

    def raise_error(self):
        result = self.result
        if error := result.get('Error'):
            raise LibP2PError(error)


class SimpleFreeMixin:
    def __del__(self):
        del_handle = getattr(self, 'del_handle', None)
        handle = getattr(self, 'handle', None)
        free = getattr(self, '_FREE')
        if del_handle:
            free(del_handle)
        elif handle:
            free(handle)


class Option(abc.ABC, SimpleFreeMixin):
    load_library().option_delete.argtypes = [c_size_t, ]
    _FREE = load_library().option_delete

    def __init__(self, handle: int) -> None:
        self.handle = handle


def c_wrap(loop: asyncio.AbstractEventLoop, fp, *a):
    return loop.run_in_executor(None, fp, *a)


class AutoInt(enum.IntEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return count


__all__ = [
    'load_library',
    'MsgpackList',
    'LibP2PError',
    'GoString',
    'MsgpackArg',
    'MsgpackBody',
    'SimpleFreeMixin',
    'Option',
    'c_wrap',
    'AutoInt',
]
