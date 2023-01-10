
from .sortedset import SortedSet
from datetime import datetime


class IntBoundSet:
    def __init__(self, *args, **kwargs):
        self.items = SortedSet()
        self.numbers = set()
        self.length = kwargs.pop('length', 0)
        if self.length < 0:
            self.length = 0

    def append(self, x):
        if self.length != 0 and len(self.items) > self.length - 1:
            oldest_value = self.items[len(self.items) - 1]
            self.items.discard(oldest_value)
            self.numbers.remove(oldest_value.get_value())

        hash_value = IntSetValue(x, datetime.now())
        self.items.add(hash_value)
        self.numbers.add(x)

    def contains(self, x):
        if x in self.numbers:
            return True

        return False

    def __len__(self):
        return len(self.items)

    def __str__(self):
        text = ""

        for x in self.items:
            text += "," + str(x.get_value())

        text += '=='

        for x in self.numbers:
            text += "," + str(x)

        return text


class IntSetValue:
    def __init__(self, value, dt):
        self.value = value
        self.dt = dt

    def __str__(self):
        return str(self.value) + ", " + str(self.dt)

    def __lt__(self, other):
        return self.dt > other.dt

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def get_value(self):
        return self.value
