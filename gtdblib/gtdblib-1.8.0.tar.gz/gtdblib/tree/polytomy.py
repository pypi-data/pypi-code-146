from pathlib import Path

import dendropy

from gtdblib import log
from gtdblib.exception import GtdbLibExit
from gtdblib.util.bio.newick import parse_label
from gtdblib.util.types import is_float


def _validate_support(support: float):
    """Validate that the support is a valid object."""
    if support is None or not is_float(support):
        raise GtdbLibExit(f'Support value "{support}" is not a float.')
    if support < 0.0 or support > 100.0:
        raise GtdbLibExit(
            f'Invalid support "{support}", must be between 0.0 and 100.0.')


def _validate_tree_path(path: Path):
    """Validate that the path is a valid tree path."""
    if path is None:
        raise GtdbLibExit(f'Path cannot be None.')
    if not isinstance(path, Path):
        raise GtdbLibExit(f'Path "{path}" is not a Path object.')


def _validate_tree_obj(tree: dendropy.Tree):
    if tree is None:
        raise GtdbLibExit(f'Tree cannot be None.')
    if not isinstance(tree, dendropy.Tree):
        raise GtdbLibExit(f'Tree "{tree}" is not a dendropy.Tree object.')
    if len(tree.taxon_namespace) == 0:
        raise GtdbLibExit(f'Tree "{tree}" has no taxa.')


def collapse_polytomy_tree(tree: dendropy.Tree, support: float):
    """Collapse nodes with low bootstrap support, works on the Tree object.

    :param tree: Tree to collapse.
    :param support: Collapse nodes that have a support less than this value.
    """
    log.info(f"Collapsing nodes with bootstrap support < {support}")

    # Validate arguments
    _validate_tree_obj(tree)
    _validate_support(support)

    n_internal_nodes = 0
    n_collapsed = 0
    for node in tree.internal_nodes():
        if node.label is not None:
            bs, _, _ = parse_label(node.label)
            if bs is not None and bs < support:
                for child_node in node.child_nodes():
                    child_node.edge_length += node.edge_length
                    node.remove_child(child_node)
                    node.parent_node.add_child(child_node)
                node.parent_node.remove_child(node)
                n_collapsed += 1
        n_internal_nodes += 1

    if n_internal_nodes > 0:
        log.info(f'Found {n_collapsed:,}/{n_internal_nodes:,} '
                 f'({n_collapsed / n_internal_nodes:.2%}) internal nodes '
                 f'to collapse.')
    else:
        raise GtdbLibExit(f'Did not find any nodes in the tree.')


def collapse_polytomy(path_in: Path, path_out: Path, support: float):
    """
    Collapse nodes with low bootstrap support.

    :param path_in: Tree to collapse.
    :param path_out: The path to write the tree to.
    :param support: Collapse nodes that have a support less than this value.
    """

    # Validate the arguments
    _validate_tree_path(path_in)
    _validate_tree_path(path_out)
    _validate_support(support)

    # Create the output directory if not exists
    path_out.parent.mkdir(parents=True, exist_ok=True)

    # Load the tree
    tree: dendropy.Tree = dendropy.Tree.get_from_path(
        str(path_in),
        schema='newick',
        rooting="force-unrooted",
        preserve_underscores=True
    )

    # Collapse nodes
    collapse_polytomy_tree(tree, support)

    # Write the output
    with open(path_out, 'w') as f:
        f.write(tree.as_string(schema='newick',
                suppress_rooting=True, unquoted_underscores=True))
    log.info(f'Wrote tree to: {path_out}')

    return
