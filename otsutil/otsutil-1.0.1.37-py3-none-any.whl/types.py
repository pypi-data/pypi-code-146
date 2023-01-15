"""よく使う型ヒントや定義を纏めたモジュールです。
"""


__all__ = (
    "FLOAT_INT",
    "T",
    "hmsValue",
    "pathLike",
)

from pathlib import Path
from typing import Tuple, TypeVar, Union

# ジェネリクス
T = TypeVar("T")
FLOAT_INT = TypeVar("FLOAT_INT", float, int)

# タイプエイリアス
hmsValue = Tuple[int, int, float]
pathLike = Union[Path, str]
