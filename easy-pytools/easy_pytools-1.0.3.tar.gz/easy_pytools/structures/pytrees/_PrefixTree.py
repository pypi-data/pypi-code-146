from typing import Union, Iterable
from .._internal import EqType


class PrefixTreeNode:
    def __init__(self, value: EqType = None):
        self._value = value
        self._termination = 0
        self._children = dict()
        self._child_values = set()

    def add_child(self, value: EqType) -> 'PrefixTreeNode':
        if value not in self._child_values:
            self._children[value] = (node := PrefixTreeNode(value))
            self._child_values.add(value)
        else:
            node = self.get_child(value)

        return node

    def get_child(self, value: EqType) -> 'PrefixTreeNode':
        if value in self._child_values:
            return self._children[value]
        else:
            return None

    def terminate(self):
        self._termination += 1

    @property
    def value(self) -> str:
        return self._value

    @property
    def termination(self):
        return self._termination

    def __contains__(self, item: 'PrefixTreeNode') -> bool:
        return item in self._child_values

    def __bool__(self) -> bool:
        return self.value is not None

    def __str__(self) -> str:
        return f"PrefixTreeNode[{self.value}]"

    def __eq__(self, other: 'PrefixTreeNode') -> bool:
        return self.value == other.value


class PrefixTree:
    def __init__(self):
        self._root = PrefixTreeNode()

    def add(self, sequence: Union[EqType, Iterable[EqType]]):
        if hasattr(sequence, '__iter__'):
            current_node = self._root
            for v in sequence:
                current_node = current_node.add_child(v)
            current_node.terminate()
        else:
            self._root.add_child(sequence)

    def count(self, sequence: Iterable[EqType]) -> int:
        current_node = self._root
        for v in sequence:
            if (current_node := current_node.get_child(v)) is None:
                return False
        return current_node.termination

    def contains(self, sequence: Iterable[EqType]) -> bool:
        return sequence in self

    def __contains__(self, sequence: Iterable[EqType]) -> bool:
        return self.count(sequence) > 0
