from collections import defaultdict
import bisect
from sidecar.skip_list import Skiplist


class SplitTree:
    MAX_DEPTH = 15
    USE_SKIP_LIST = False
    INIT_KEY = (0, 2 ** 32, 1)

    def find(self, hash_integer: int):
        hash_integer = hash_integer % 2 ** 32
        if SplitTree.USE_SKIP_LIST:
            def _cmp(node_key, key):
                return node_key and node_key <= key
            return self.sl.scan_by_compare((hash_integer, 0, 0), _cmp)
        index = bisect.bisect_left(self.nodes, (hash_integer,))
        index = max(index - 1, 0)
        return index

    def __init__(self):
        nodes = [SplitTree.INIT_KEY, ].copy()
        self.sl = Skiplist()
        self.sl[SplitTree.INIT_KEY] = dict()
        self.nodes = nodes
        self.node_values = dict()
        self.node_values[SplitTree.INIT_KEY] = dict()
        self.split_level = 1
        self.merge_level = 1
        self.level_set = defaultdict(set)
        self.merge_pairs = defaultdict(set)
        self.level_set[1].add(SplitTree.INIT_KEY)
        self.set_level()

    def clear(self):
        self.nodes.clear()
        self.sl = Skiplist()
        self.merge_pairs.clear()
        self.level_set.clear()
        nodes = [SplitTree.INIT_KEY, ]
        self.nodes = nodes
        self.node_values.clear()
        self.sl[SplitTree.INIT_KEY] = dict()
        self.node_values[SplitTree.INIT_KEY] = dict()
        self.level_set[1].add(SplitTree.INIT_KEY)
        self.set_level()

    def set_level(self):
        self.split_level = min([key for key in self.level_set.keys() if self.level_set[key]])
        self.merge_level = max([key for key in self.level_set.keys() if self.level_set[key]])

    def __repr__(self):
        length = len(self.sl) if SplitTree.USE_SKIP_LIST else len(self.nodes)
        return f"<SplitTree {self.split_level}:{self.merge_level}, {length}>"

    def split(self):
        if self.split_level >= self.MAX_DEPTH:
            return None
        level = self.split_level
        if not self.level_set[level]:
            return None
        node = self.level_set[level].pop()
        b, e, level = node
        new_level = level + 1
        middle = b + ((e - b) // 2)
        left_node = (b, middle, new_level,)
        right_node = (middle, e, new_level,)
        if SplitTree.USE_SKIP_LIST:
            self.sl.pop(node)
            self.sl[right_node] = dict()
            self.sl[left_node] = dict()
        else:
            split_index = self.nodes.index(node)
            self.nodes.pop(split_index)
            del self.node_values[node]
            self.nodes.insert(split_index, right_node)
            self.node_values[right_node] = dict()
            self.nodes.insert(split_index, left_node)
            self.node_values[left_node] = dict()

        self.merge_pairs[new_level].add((left_node, right_node,))
        self.level_set[new_level].add(left_node)
        self.level_set[new_level].add(right_node)
        self.set_level()
        return node

    def merge(self):
        if self.merge_level <= 1:
            return None
        level = self.merge_level
        if not self.merge_pairs[level]:
            return None
        pair = self.merge_pairs[level].pop()
        left_node, right_node = pair
        node = (left_node[0], right_node[1], self.merge_level - 1)
        if SplitTree.USE_SKIP_LIST:
            self.sl.pop(left_node)
            self.sl.pop(right_node)
            self.sl[node] = dict()
        else:
            merge_index = self.nodes.index(left_node)
            self.nodes.pop(merge_index)
            del self.node_values[left_node]
            self.nodes.pop(merge_index)
            del self.node_values[right_node]
            self.nodes.insert(merge_index, node)
            self.node_values[node] = dict()

        self.level_set[node[2]].add(node)
        self.level_set[left_node[2]].remove(left_node)
        self.level_set[right_node[2]].remove(right_node)
        self.set_level()
        return node


__all__ = ['SplitTree', ]



from datetime import datetime
SplitTree.USE_SKIP_LIST = False
tree = SplitTree()
print("begin", datetime.now())
for _ in range(10000):
    tree.split()
    # print(tree)
print("done", datetime.now())
for _ in range(10000):
    tree.merge()
print("merged", datetime.now())
print(tree)
