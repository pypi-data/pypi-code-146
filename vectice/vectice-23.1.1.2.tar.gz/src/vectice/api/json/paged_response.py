from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import Generic, Sequence, Type, TypeVar

from vectice.api.json.page import Page

ItemType = TypeVar("ItemType")


@dataclass
class PagedResponse(Generic[ItemType]):
    """
    Generic structure describing a result of a paged request.
    The structure contains page information and the list of items for this page.

    """

    total: int
    """
    total number of available pages
    """
    list: list[ItemType] = field(init=False)
    """
    current list of elements for this page
    """
    current_page: Page = field(init=False)
    """
    information on the current page.
    """
    page: InitVar[dict]
    item_cls: InitVar[Type[ItemType]]
    items: InitVar[Sequence[dict]]

    def __post_init__(self, page: dict, cls: Type[ItemType], items: Sequence[dict]):
        self.current_page = Page(**page)
        self.list = []
        if items is not None:
            for item in items:
                type_item = cls(**item)
                self.list.append(type_item)
