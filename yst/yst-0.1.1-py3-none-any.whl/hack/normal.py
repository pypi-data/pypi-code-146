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


def to_list(self):
    return list(self)


def to_dict(self):
    return dict(self)


def to_set(self):
    return set(self)


for t in [map, filter, list, set, dict]:
    for (n, f) in [('to_list', to_list), ('to_dict', to_dict), ('to_set', to_set)]:
        curse(t, n, f)

for t in [list, set]:
    curse(t, 'map', _map)
    curse(t, 'filter', _filter)
curse(dict, 'map', dict_map)
curse(dict, 'filter', dict_filter)

for t in [str, list, map, set]:
    curse(t, "size", size)
    curse(t, "empty", empty)
