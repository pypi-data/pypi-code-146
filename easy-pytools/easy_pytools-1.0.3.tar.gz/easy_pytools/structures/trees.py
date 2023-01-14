from typing import Iterable

from .pytrees._BinaryTree import BinaryTree as PyBinaryTree
from .pytrees._PrefixTree import PrefixTree as PyPrefixTree
from ._internal import CompType, HashType


class BinaryTree:
    def add(self, item: CompType):
        raise NotImplementedError()

    def is_empty(self) -> bool:
        raise NotImplementedError()

    def contains(self, item: CompType):
        raise NotImplementedError()

    @property
    def depth(self) -> int:
        raise NotImplementedError()


class PrefixTree:
    def add(self, sequence: Iterable[HashType]):
        raise NotImplementedError()

    def contains(self, sequence: Iterable[HashType]) -> bool:
        raise NotImplementedError()

    def count(self, sequence: Iterable[HashType]) -> int:
        raise NotImplementedError()


from .cpp_lib.dist.trees import BinaryTree, PrefixTree