"""定数を纏めたモジュールです。
"""


__all__ = (
    "REGEX_NF_VALUE",
    "T",
)


import re

from typing import TypeVar

REGEX_NF_VALUE = re.compile("^([1-9][0-9]*)(%)?$")
T = TypeVar("T")
