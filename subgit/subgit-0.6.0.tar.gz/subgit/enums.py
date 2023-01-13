from enum import Enum


class OrderAlgorithms(Enum):
    ALPHABETICAL = 10
    TIME = 20
    SEMVER = 30


class SelectionMethods(Enum):
    SEMVER = 10
    EXACT = 20


__all__ = [
    "OrderAlgorithms",
    "SelectionMethods",
]
