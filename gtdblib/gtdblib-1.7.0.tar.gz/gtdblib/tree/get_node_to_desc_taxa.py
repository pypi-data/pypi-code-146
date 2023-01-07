from collections import defaultdict
from typing import Dict, FrozenSet

import dendropy

from gtdblib.tree.get_node_depth import get_tree_node_depth


def get_tree_node_to_desc_taxa(tree: dendropy.Tree) -> Dict[dendropy.Node, FrozenSet[str]]:
    """Get each node and the taxa that are descendants of this node.

    :param tree: The dendropy tree object to calculate the depths for.

    :returns: A dictionary of nodes and their descendant taxa.
    """

    # Calculate the nodes at each depth
    node_depth = get_tree_node_depth(tree)

    # Process the deepest nodes first
    out = defaultdict(set)
    for depth, nodes in sorted(node_depth.items(), key=lambda x: x[0], reverse=True):
        for node in nodes:

            # Seed the output dictionary
            if node.is_leaf():
                out[node].add(node.taxon.label)

            # Check bring up the taxa from the descendant nodes
            else:
                for child in node.child_nodes():
                    out[node].update(out[child])

    assert (out[tree.seed_node] == {x.label for x in tree.taxon_namespace})
    return {k: frozenset(v) for k, v in out.items()}
