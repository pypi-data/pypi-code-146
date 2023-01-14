from typing import Union, Iterable

from .._internal import CompType


class BinarySubtree:
    def __init__(self, value: CompType = None, parent: 'BinarySubtree' = None):
        self._value = value
        self._depth = 0
        self._parent = parent
        self._left_child: 'BinarySubtree' = None
        self._right_child: 'BinarySubtree' = None

        if value is not None:
            self._left_child = BinarySubtree(parent=self)
            self._right_child = BinarySubtree(parent=self)
            self._depth = 1

    def goes_left(self, value: CompType) -> bool:
        if self and (value is not None):
            return self > value
        else:
            return False

    def goes_right(self, value: CompType) -> bool:
        if self and (value is not None):
            return self < value
        else:
            return False

    def set_child(self, other: 'BinarySubtree') -> 'BinarySubtree':
        was_child = None
        if self.goes_left(other):
            was_child = self._left_child
            self._left_child = other
            other.set_parent(self)
        elif self.goes_right(other):
            was_child = self._right_child
            self._right_child = other
            other.set_parent(self)

        return was_child

    def set_parent(self, other: 'BinarySubtree') -> 'BinarySubtree':
        was_parent = self._parent
        self._parent = other
        return was_parent

    def add(self, value: CompType) -> 'BinarySubtree':
        result = None
        if self:
            if self.goes_left(value):
                if self.left:
                    result = self.left.add(value)
                else:
                    result = BinarySubtree(value)
                    self.set_child(result)
            elif self.goes_right(value):
                if self.right:
                    result = self.right.add(value)
                else:
                    result = BinarySubtree(value)
                    self.set_child(result)
        else:
            self.__init__(value, self._parent)
            result = self

        if result:
            self._depth = max(self.left_subtree_depth, self.right_subtree_depth)+1

        if abs(self.left_subtree_depth - self.right_subtree_depth) > 1:
            self.balance()

        return result

    def balance(self):
        if not self:
            return
        dleft = self.left_subtree_depth
        dright = self.right_subtree_depth
        dleft_left = self.left.left_subtree_depth
        dleft_right = self.left.right_subtree_depth
        dright_left = self.right.left_subtree_depth
        dright_right = self.right.right_subtree_depth

        z = self
        p = self._parent

        if (dleft > dright) and (dleft_left >= dleft_right):
            y = self.left
            t3 = self.left.right

            p.set_child(y)
            y._right_child = z
            z._parent = y
            z._left_child = t3
            t3._parent = z

        elif (dleft > dright) and (dleft_left <= dleft_right):
            y = self.left
            x = y.right
            t2 = x.left

            z._left_child = x
            x._parent = z
            x._left_child = y
            y._parent = x
            y._right_child = t2
            t2._parent = y

        elif (dleft < dright) and (dright_left <= dright_right):
            y = self.right
            t2 = y.left

            p.set_child(y)
            y._left_child = z
            z._parent = y
            z._right_child = t2
            t2._parent = z

        elif (dleft < dright) and (dright_left >= dright_right):
            y = self.right
            x = y.left
            t3 = x.right

            z._right_child = x
            x._parent = z
            x._right_child = y
            y._parent = x
            y._left_child = t3
            t3._parent = y

            t2 = x.left
            p.set_child(x)
            x._left_child = z
            z._parent = x
            z._right_child = t2
            t2._parent = z

    def travel(self) -> Iterable['BinarySubtree']:
        if self:
            yield self
            if self.right:
                yield from self.right.travel()
            if self.left:
                yield from self.left.travel()

    @property
    def left_subtree_depth(self) -> int:
        if self.left:
            return self.left.depth
        else:
            return 0

    @property
    def right_subtree_depth(self) -> int:
        if self.right:
            return self.right.depth
        else:
            return 0

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def value(self):
        return self._value

    @property
    def left(self) -> 'BinarySubtree':
        return self._left_child

    @property
    def right(self) -> 'BinarySubtree':
        return self._right_child

    @property
    def graph_string(self):
        if self:
            return f"{self}:\nl:{self.left.graph_string}\nr:{self.right.graph_string}"
        else:
            return ""

    def __contains__(self, item: CompType) -> bool:
        if self == item:
            result = True
        elif self.goes_right(item) and self.right:
            result = item in self.right
        elif self.goes_left(item) and self.left:
            result = item in self.left
        else:
            result = False

        return result

    def __iter__(self) -> Iterable['BinarySubtree']:
        return self.travel()

    def __bool__(self):
        return self.value is not None

    def __eq__(self, other: CompType | 'BinarySubtree'):
        item = other.value if isinstance(other, BinarySubtree) else other
        return self.value == item

    def __gt__(self, other: CompType | 'BinarySubtree'):
        item = other.value if isinstance(other, BinarySubtree) else other
        return self.value > item

    def __lt__(self, other: CompType | 'BinarySubtree'):
        item = other.value if isinstance(other, BinarySubtree) else other
        return self.value < item

    def __str__(self):
        return f"BinarySubtree[{self.value}]"


class BinaryTree:
    def __init__(self, value: CompType = None):
        self._child: 'BinarySubtree' = BinarySubtree(value, parent=self) if value else BinarySubtree(parent=self)
        self._count = 1 if value else 0

    def set_child(self, child: 'BinarySubtree') -> 'BinarySubtree':
        was_child = self._child
        self._child = child
        child.set_parent(self)

        return was_child

    def set_parent(self, other: 'BinarySubtree') -> 'BinarySubtree':
        raise NotImplementedError("BinaryTree can not have parent")

    def add(self, value: CompType) -> 'BinarySubtree':
        result = self._child.add(value)
        if result:
            self._count += 1
        return result

    def balance(self):
        self._child.balance()

    def travel(self) -> Iterable['BinarySubtree']:
        yield from self._child.travel()

    @property
    def depth(self):
        return self._child.depth

    @property
    def _left_child(self):
        return self._child

    @property
    def _right_child(self):
        return self._child

    @property
    def count(self):
        return self._count

    def contains(self, item: CompType) -> bool:
        return item in self

    def __contains__(self, item: CompType):
        return item in self._child

    def __iter__(self) -> Iterable['BinarySubtree']:
        return self.travel()

    def __str__(self):
        return f"BinaryTree[depth: {self.depth}, count: {self.count}]"
