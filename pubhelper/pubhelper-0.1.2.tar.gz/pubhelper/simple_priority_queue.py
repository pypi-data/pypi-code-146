import heapq
from typing import Any, Iterable


class SimplePriorityQueue(list):
    """简单优先队列实现"""

    def __init__(self, *args, **kwargs):
        """禁止从构造函数添加元素"""
        super(SimplePriorityQueue, self).__init__()

    def __getitem__(self, item):
        data = super().__getitem__(item)
        if data and isinstance(data, (tuple, list)):
            return data[-1]
        return data

    def __setitem__(self, key, value):
        super(
            SimplePriorityQueue, self
        ).__setitem__(
            key, (0, key, value)
        )

    def __iter__(self):
        while True:
            yield self.pop_pri()

    def append(self, obj: Any) -> None:
        self.push_pri(obj)

    def extend(self, iterable: Iterable[Any]) -> None:
        [self.append(item) for item in iterable]

    def pop(self, index: int = -1):
        data = super().pop(index)
        if data and isinstance(data, (tuple, list)):
            return data[-1]
        return data

    def pop_pri(self):
        return heapq.heappop(self)[-1] if self else None

    def push_pri(self, item: Any, priority: int = 0):
        heapq.heappush(self, (-priority, len(self), item))


__all__ = ('SimplePriorityQueue',)
