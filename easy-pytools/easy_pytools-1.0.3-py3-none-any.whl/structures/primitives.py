from typing import Any


class Queue:
    def add(self, value):
        raise NotImplementedError()

    def next(self) -> Any:
        raise NotImplementedError()

    def is_empty(self) -> bool:
        raise NotImplementedError()

    @property
    def size(self) -> int:
        raise NotImplementedError()

    @property
    def first(self) -> Any:
        raise NotImplementedError()

    @property
    def last(self) -> Any:
        raise NotImplementedError()


class Stack:
    def push(self, value):
        raise NotImplementedError()

    def pop(self) -> Any:
        raise NotImplementedError()

    def is_empty(self) -> bool:
        raise NotImplementedError()

    @property
    def top(self) -> Any:
        raise NotImplementedError()

    @property
    def size(self) -> int:
        raise NotImplementedError()


from .cpp_lib.dist.primitives import Stack, Queue