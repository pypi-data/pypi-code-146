# General-purpose queue of items
# Method calls on queue use indices that start at 1

import random
from pathlib import Path

from .selector import Selector
from .item import Item
from busy import do_import


class BusyQueue:

    itemclass = Item
    default_key = 'default'

    def __init__(self, manager=None, items=[]):
        self.manager = manager
        self.changed = False
        self._items = [self.itemclass.create(i) for i in items if i]

    def all(self):
        return self._items

    def count(self):
        return len(self._items)

    # Add new items. Always makes them the right class. Also does inserts.

    def add(self, *items, index=None):
        newitems = [self.itemclass.create(i) for i in items if i]
        index = len(self._items) if index is None else index
        self._items[index:index] = newitems
        self.changed = True

    # Replace existing items at the indices provided. Also inserts if the
    # indices run out. Does not create items. Would be good to combine this
    # with the add method.

    def replace(self, indices, newvalues):
        while newvalues and indices:
            self._items[indices.pop(0)] = newvalues.pop(0)
        while indices:
            del self._items[indices.pop()]
        self._items.extend(newvalues)
        self.changed = True

    def get(self, index=1):
        return self._items[index-1] if self._items else None

    def select(self, *criteria):
        selector = Selector(criteria)
        return selector.indices(self._items)

    def _split(self, *criteria):
        return self._split_by_indices(*self.select(*criteria))

    def _split_by_indices(self, *indices):
        inlist = [t for i, t in enumerate(self._items) if i in indices]
        outlist = [t for i, t in enumerate(self._items) if i not in indices]
        return (inlist, outlist)

    def criteria_string(self, *criteria):
        return " ".join([str(i) for i in self.select(*criteria)])

    def pop(self, *criteria):
        if not criteria:
            criteria = [len(self._items)]
        hilist, lolist = self._split(*criteria)
        self._items = hilist + lolist
        self.changed = True
        return "Popped " + self.criteria_string(*criteria)

    def drop(self, *criteria):
        if not criteria:
            criteria = [1]
        lolist, hilist = self._split(*criteria or [1])
        self._items = hilist + lolist
        self.changed = True
        return "Dropped " + self.criteria_string(*criteria)

    def delete(self, *criteria):
        self._items = self._split(*criteria)[1]
        self.changed = True

    def delete_by_indices(self, *indices):
        self._items = self._split_by_indices(*indices)[1]
        self.changed = True

    def list(self, *criteria):
        return [(i+1, self._items[i]) for i in self.select(*criteria)]

    @property
    def strings(self):
        return [str(i) for i in self._items]

    def manage(self, *criteria, editor):
        itemlist = self.list(*criteria)
        indices = [i[0]-1 for i in itemlist]
        items = [i[1] for i in itemlist]
        new_items = editor(self.itemclass, *items)
        self.replace(indices, new_items)

    def shuffle(self, *criteria):
        itemlist = self.list(*criteria)
        indices = [i[0]-1 for i in itemlist]
        items = [i[1] for i in itemlist]

        random.shuffle(items)

        self.replace(indices, items)

    @classmethod
    def register(self, queueclass, default=False):
        if not hasattr(self, '_classes'):
            self._classes = {}
        self._classes[queueclass.key] = queueclass
        if default:
            self.default_key = queueclass.key

    @classmethod
    def subclass(self, key):
        return self._classes.get(key) or self

    # Get all the tags for the queue, as a set

    def tags(self):
        master = [i.tags for i in self._items]
        return {item for sublist in master for item in sublist}


do_import(Path(__file__).parent / 'queues', 'busy.queues')
