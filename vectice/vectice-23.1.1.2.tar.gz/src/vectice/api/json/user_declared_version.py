from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserDeclaredVersion:
    name: str | None = None
    """"""
    uri: str | None = None
    """"""
    description: str | None = None
    """"""
    isStarred: bool | None = False
    """"""
