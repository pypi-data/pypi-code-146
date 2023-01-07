import random
from typing import Optional
from dataclasses import dataclass, field
from .nexus import Nexus

@dataclass(order=True)
class ObjectCopyEntry:
    hash: str = field(compare=False)
    size: int = field(compare=False)
    blocksize: int = field(compare=False)
    size_order: int = field(compare=False)
    groupkey: tuple[int, int] = field(default=(0, 0), compare=False)
    maxcopies: Optional[int] = field(default=None, compare=False)
    refs: int = field(default=0, compare=False)
    nexusfrom: Optional[Nexus] = field(compare=False, default=None)
    nexusto: Optional[Nexus] = field(compare=False, default=None)
    path: str = field(default='', compare=False)
    modtime: int = field(default=0, compare=False)
    imbalance_change: float = field(default=0.0, compare=True)

@dataclass(order=True)
class ObjectGroup:
    groupkey: tuple[int, int]
    objects: list[ObjectCopyEntry] = field(default_factory=list, compare=False)
    saved_objects: Optional[list] = field(default=None, compare=False)
    totalsize: int = field(default=0, compare=False)
    sorted: bool = field(default=False, compare=False)

    def commit(self):
        self.saved_objects = None

    def rollback(self):
        if self.saved_objects is not None:
            self.objects = self.saved_objects

    def add_entry(self, obj):
        self.objects.append(obj)
        self.totalsize += obj.blocksize

    def pop_entry(self, max_size=None):
        '''Calculates the imbalance change for all objects in the group, sorts them with
        the best balance improvements at the front, then chooses a random entry from the
        first third of the list, weighted toward earlier entries, removes, and returns
        it.'''

        # Save the previous list of objects in case we have to back out changes
        if self.saved_objects is None:
            self.saved_objects = list(self.objects)

        while True:
            # Generate a uniform random number between 0.0 and 1.0, then cube it to weight it lower.
            rval = random.random()
            pos = int((rval * rval * rval) * len(self.objects) / 3)
            item = self.objects[pos]
            del self.objects[pos]
            self.totalsize -= item.blocksize
            if max_size is None or item.blocksize <= max_size:
                return item

    def sort(self, levels):
        '''Recalculate the imbalance change for all objects in the group'''
        for obj in self.objects:
            obj.imbalance_change = levels.calc_imbalance_change(obj.nexusfrom, obj.nexusto, obj.size_order)
        self.objects.sort()
        self.sorted = True

class ObjectGroupList(list):
    def __init__(self, ondisk):
        super().__init__()
        self.ondisk = ondisk

    def commit(self):
        for grp in self:
            grp.commit()

    def rollback(self):
        for grp in self:
            grp.rollback()
