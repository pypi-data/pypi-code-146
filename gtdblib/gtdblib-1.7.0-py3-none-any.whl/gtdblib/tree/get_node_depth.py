from collections import deque, defaultdict
from typing import Dict, Set

import dendropy


def get_tree_node_depth(tree: dendropy.Tree) -> Dict[int, Set[dendropy.Node]]:
    """Calculate the depth of all nodes in the tree.

    :param tree: The dendropy tree object to calculate the depths for.

    :returns: A dictionary of depths to nodes at that depth.
    """
    # Validate arguments
    if not isinstance(tree, dendropy.Tree):
        raise ValueError(f'Tree is not a dendropy.Tree object.')

    # Create a queue starting from the seed node (depth=0)
    out = defaultdict(set)
    queue = deque([(tree.seed_node, 0)])

    # Progressively add children to the queue
    while len(queue) > 0:
        cur_node, cur_depth = queue.popleft()
        out[cur_depth].add(cur_node)

        for child in cur_node.child_nodes():
            queue.append((child, cur_depth + 1))

    # Make this a dictionary (not defaultdict)
    return dict(out)
