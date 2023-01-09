"""
.. include:: ../extras/consts.md
"""

from typing import Any

__all__ = ["MISSING"]


class _Missing:
    def __eq__(self, _) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _Missing()
