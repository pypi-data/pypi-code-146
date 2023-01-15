"""個人的によく使う関数、クラス、型ヒントを纏めたライブラリです。
"""

__all__ = (
    "FLOAT_INT",
    "ObjectSaver",
    "OtsuNone",
    "T",
    "Timer",
    "deduplicate",
    "hmsValue",
    "load_json",
    "pathLike",
    "read_lines",
    "save_json",
    "setup_path",
    "str_to_path",
    "write_lines",
)

from .classes import ObjectSaver, OtsuNone, Timer
from .funcs import (
    deduplicate,
    load_json,
    read_lines,
    save_json,
    setup_path,
    str_to_path,
    write_lines,
)
from .types import FLOAT_INT, T, hmsValue, pathLike
