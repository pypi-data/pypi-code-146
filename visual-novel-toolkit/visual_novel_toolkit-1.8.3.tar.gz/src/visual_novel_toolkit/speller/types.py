from typing import TypeAlias
from typing import TypedDict


class YASpeller(TypedDict, total=False):
    dictionary: list[str]


class Item(TypedDict, total=False):
    word: str


class Items(TypedDict, total=False):
    data: list[Item]


Report: TypeAlias = list[tuple[bool, Items]]
