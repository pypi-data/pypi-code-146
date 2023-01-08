import math
from typing import Union, Optional, Iterable, List


class ThresholdFind:
    def __init__(self, reverse: bool = False):
        self.known_false = -math.inf if not reverse else math.inf
        self.known_true = math.inf if not reverse else -math.inf
        self.reverse: bool = reverse

    def get(self, value: Union[int, float]) -> Optional[bool]:
        if not self.reverse and value <= self.known_false or self.reverse and value >= self.known_false:
            return False
        if not self.reverse and value >= self.known_true or self.reverse and value <= self.known_true:
            return True
        return None

    def register(self, value: Union[float, int], result: bool):
        if result:
            if not self.reverse and value < self.known_true or self.reverse and value > self.known_true:
                self.known_true = value
        else:
            if not self.reverse and value > self.known_false or self.reverse and value < self.known_false:
                self.known_false = value

    def clear(self):
        self.known_false = -math.inf if not self.reverse else math.inf
        self.known_true = math.inf if not self.reverse else -math.inf


def first(iterable: Iterable):
    return next(iter(iterable))


def last(l: List):
    return l[-1]
