from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Page:
    """
    simple structure to allow paging when requesting list of elements
    """

    index: int | None = 1
    """
    the index of the page
    """
    size: int | None = 100
    """
    the size of the page.
    """
    afterCursor: bool | None = False

    hasNextPage: bool | None = False
