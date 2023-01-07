import statistics
from dataclasses import dataclass, field

from .utils import disk_in_nexus

@dataclass
class Nexus:
    nexusid: str
    level: int = 0
    refs: int = 0
    totalsize: int = 0
    saturated_size: int = 0
    disks: str = ''

@dataclass
class NexusLevel:
    level: int
    members: list[Nexus] = field(default_factory=list)
    totalsize: int = 0
    saturated_size: int = 0
    imbalance: float = 0.0
    imbalance_change_cache: dict = field(default_factory=dict)

    def add_member(self, m):
        self.totalsize += m.totalsize
        self.saturated_size += m.saturated_size
        self.members.append(m)

    def change_size(self, nexus, diff, saturated:bool=False):
        self.totalsize += diff
        nexus.totalsize += diff
        if saturated:
            self.saturated_size += diff
            nexus.saturated_size += diff

        self.imbalance_change_cache.clear()
        self.update_imbalance()

    def calc_imbalance(self, modified_nexus=None, size_diff_order=0, sign=1):
        '''Calculate how "balanced" the member nexuses would be with the given change'''
        res = self.imbalance_change_cache.get(sign * size_diff_order)
        if res is not None:
            return res

        size_diff = sign * (1 << size_diff_order)
        res = 0.0
        if len(self.members) > 1:
            mean = (self.totalsize + size_diff) / len(self.members)
            res = statistics.stdev([(nexus.totalsize + size_diff) if nexus is modified_nexus else nexus.totalsize for nexus in self.members], mean)

        self.imbalance_change_cache[sign * size_diff_order] = res

        return res

    def update_imbalance(self):
        if len(self.members) > 1:
            mean = self.totalsize / len(self.members)
            self.imbalance = statistics.stdev([nexus.totalsize for nexus in self.members], mean)
        else:
            self.imbalance = 0.0

class NexusLevelDict(dict):
    def __init__(self, nexus_seq):
        super().__init__()
        if isinstance(nexus_seq, dict):
            nexus_seq = nexus_seq.values()

        for nexus in nexus_seq:
            self[nexus.level].add_member(nexus)

    def __missing__(self, key):
        r = self[key] = NexusLevel(key)
        return r

    def move_object(self, old_nexus, new_nexus, size, maxcopies=None):
        self[old_nexus.level].change_size(old_nexus, -size, maxcopies is not None and old_nexus.level >= maxcopies)
        self[new_nexus.level].change_size(new_nexus, size, maxcopies is not None and new_nexus.level >= maxcopies)

    def calc_imbalance_change(self, from_nexus, to_nexus, size_diff_order):
        from_level = self[from_nexus.level]
        to_level = self[to_nexus.level]

        imbalance_change_from = from_level.calc_imbalance(from_nexus, size_diff_order, -1) - from_level.imbalance
        imbalance_change_to = to_level.calc_imbalance(to_nexus, size_diff_order, 1) - to_level.imbalance

        # Weight the imbalance change to higher-level nexus more.
        if from_nexus.level > to_nexus.level:
            imbalance_change_from *= 2
        else:
            imbalance_change_to *= 2

        return imbalance_change_to + imbalance_change_from

    def get_copy_data(self, nexus_index=None):
        copy_data = [(0, 0)] * (max(self) + 1)

        if nexus_index is not None:
            for index, level in self.items():
                all_nexus = [nexus for nexus in level.members if disk_in_nexus(nexus.nexusid, nexus_index)]
                copy_data[index] = (
                    sum(nexus.totalsize for nexus in all_nexus),
                    sum(nexus.saturated_size for nexus in all_nexus)
                )
        else:
            for index, level in self.items():
                copy_data[index] = (level.totalsize, level.saturated_size)

        return copy_data
