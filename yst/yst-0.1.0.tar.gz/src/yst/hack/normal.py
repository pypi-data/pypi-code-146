from forbiddenfruit import curse


def size(self):
    return len(self)


def empty(self):
    return len(self) == 0


def _map(self, f):
    return map(f, self)


def _filter(self, f):
    return filter(f, self)


def dict_filter(self, f: dict):
    return filter(f, self.items())


def dict_map(self: dict, f):
    return map(f, self.items())


for t in [list, set]:
    curse(t, 'map', _map)
    curse(t, 'filter', _filter)
curse(dict, 'map', dict_map)
curse(dict, 'filter', dict_filter)

for t in [str, list, map, set]:
    curse(t, "size", size)
    curse(t, "empty", empty)
