import sys

pyversion = sys.version_info[:2]


if pyversion >= (3, 10):
    from typing import TypeAlias  # type: ignore[attr-defined]
else:
    from typing_extensions import TypeAlias


__all__ = [
    "TypeAlias",
]
