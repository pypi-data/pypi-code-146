import sys
from pathlib import Path
from threading import Thread
import base64
import os
import platform

argv = sys.argv[1:]


def get_cuurent_platform() -> str:
    return platform.uname().system


IS_WINDOWS = get_cuurent_platform() == "Windows"

tool = ("C:\\" if IS_WINDOWS else "/mnt/c/") + os.path.join(
    "Windows", ".upakaraNAni", "bin"
)


def from_base64(v: str) -> str:
    """Convert Text from ``base64`` to ``utf-8``"""
    return base64.b64decode(v).decode("utf-8")


def to_base64(v: str) -> str:
    """Convert Text from ``utf-8`` to ``base64``"""
    return base64.b64encode(bytes(v, "utf-8")).decode("utf-8")


def args(i: int) -> str:
    if i > len(argv) - 1:
        return ""
    else:
        return argv[i]


def get_type(val) -> str:
    return str(type(val))[8:-2]


def home() -> str:
    """Get ``home`` path for windows"""
    return str(Path.home())


def start_thread(f: str, daemon=False, join=False):
    th = Thread(target=f)
    th.daemon = daemon
    th.start()
    if join:
        th.join()
    return th
