"""よく使う型ヒントや定義を纏めたモジュールです。
"""


__all__ = (
    "FLOAT_INT",
    "T",
    "hmsValue",
    "pathLike",
)

from pathlib import Path
from typing import TypeVar

# ジェネリクス
T = TypeVar("T")
FLOAT_INT = TypeVar("FLOAT_INT", float, int)

# タイプエイリアス
hmsValue = tuple[int, int, float]
pathLike = Path | str
