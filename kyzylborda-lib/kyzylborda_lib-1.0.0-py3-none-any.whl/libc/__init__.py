import ctypes
import os


__all__ = ("libc", "SPLICE_F_NONBLOCK", "get_errno", "strerror")


libc = ctypes.CDLL("libc.so.6", use_errno=True)
SPLICE_F_NONBLOCK = 0x2

get_errno = ctypes.get_errno
strerror = os.strerror
