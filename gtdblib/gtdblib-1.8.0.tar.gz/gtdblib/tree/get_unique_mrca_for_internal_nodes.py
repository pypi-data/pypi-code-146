from typing import Dict, Tuple

import dendropy


def get_tree_unique_mrca_for_internal_nodes(tree: dendropy.Tree) -> Dict[dendropy.Node, Tuple[str, str]]:
    """Calculate a unique MRCA for each internal node, i.e. using these taxa
    will always yield the same internal node.

    :param tree: The dendropy tree object to calculate the depths for.

    :returns: A dictionary of nodes and a tuple of each taxon that identifies the node.
    """

    out = dict()
    for node in tree.internal_nodes():
        child_nodes = node.child_nodes()
        if len(child_nodes) < 2:
            raise ValueError("Node must have at least 2 children")
        left_child = child_nodes[0]
        right_child = child_nodes[1]

        left_taxon = left_child.leaf_nodes()[0].taxon.label
        right_taxon = right_child.leaf_nodes()[0].taxon.label

        out[node] = (left_taxon, right_taxon)

    return out
