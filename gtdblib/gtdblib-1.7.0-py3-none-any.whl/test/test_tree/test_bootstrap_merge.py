import tempfile
import unittest
from pathlib import Path

import dendropy

from gtdblib.tree.bootstrap_merge import bootstrap_merge_replicates


def _create_test_tree(a: str, b: str, c: str, d: str, path: Path):
    """
    #
    #         (seed)
    #      /          \
    #    ch1          ch2
    #   /  \          /  \
    #  ch3  ch4     ch5  ch6
    """
    taxon_namespace = dendropy.TaxonNamespace(["A", "B", "C", "D", ])
    tree = dendropy.Tree(taxon_namespace=taxon_namespace)

    # Left branch
    ch1 = tree.seed_node.new_child(edge_length=1)
    ch3 = ch1.new_child(edge_length=1)
    ch4 = ch1.new_child(edge_length=1)

    # Right branch
    ch2 = tree.seed_node.new_child(edge_length=1)
    ch5 = ch2.new_child(edge_length=2)
    ch6 = ch2.new_child(edge_length=3)

    # Assign taxa
    ch3.taxon = taxon_namespace.get_taxon(a)
    ch4.taxon = taxon_namespace.get_taxon(b)
    ch5.taxon = taxon_namespace.get_taxon(c)
    ch6.taxon = taxon_namespace.get_taxon(d)

    tree.write_to_path(str(path),
                       schema='newick',
                       suppress_rooting=True,
                       unquoted_underscores=True)

    return tree


def _create_test_tree_2(a: str, b: str, c: str, d: str, path: Path):
    """
    #
    #         (seed)
    #      /          \
    #    ch1          ch2
    #             /         \
    #           ch3         ch4
                          /      \
                        ch5      ch6
    """
    taxon_namespace = dendropy.TaxonNamespace(["A", "B", "C", "D", ])
    tree = dendropy.Tree(taxon_namespace=taxon_namespace)

    # Left branch
    ch1 = tree.seed_node.new_child(edge_length=1)

    # Right branch
    ch2 = tree.seed_node.new_child(edge_length=1)

    ch3 = ch2.new_child(edge_length=1)
    ch4 = ch2.new_child(edge_length=1)

    ch5 = ch4.new_child(edge_length=2)
    ch6 = ch4.new_child(edge_length=3)

    # Assign taxa
    ch1.taxon = taxon_namespace.get_taxon(a)
    ch3.taxon = taxon_namespace.get_taxon(b)
    ch5.taxon = taxon_namespace.get_taxon(c)
    ch6.taxon = taxon_namespace.get_taxon(d)

    tree.write_to_path(str(path),
                       schema='newick',
                       suppress_rooting=True,
                       unquoted_underscores=True)

    return tree


class TestTreeBootstrapMerge(unittest.TestCase):

    # def test_bootstrap_merge_replicates(self):
    #     with tempfile.TemporaryDirectory() as tmp_dir:
    #         tmp_dir = Path(tmp_dir)
    #
    #         path_ref = tmp_dir / 'ref.tree'
    #         path_1 = tmp_dir / '1.tree'
    #         path_2 = tmp_dir / '2.tree'
    #         path_3 = tmp_dir / '3.tree'
    #
    #         _create_test_tree('A', 'B', 'C', 'D', path_ref)
    #
    #         _create_test_tree('A', 'D', 'B', 'C', path_1)
    #         _create_test_tree('B', 'A', 'C', 'D', path_2)
    #         _create_test_tree_2('A', 'B', 'C', 'D', path_3)
    #
    #         path_out = tmp_dir / 'out.tree'
    #         bootstrap_merge_replicates(path_ref, path_out, [path_1, path_2, path_3])
    #
    #         tree = dendropy.Tree.get_from_path(str(path_out), schema='newick')
    #
    #         seed_bs = float(tree.seed_node.label)
    #
    #         self.assertEqual(seed_bs, 100.0)

   def test_bootstrap_merge_replicates_local(self):
        path_out = Path('/tmp/ar/merged.tree')
        path_ref = Path('/tmp/ar/ar53_r207.tree')

        import os
        rep_paths = list()
        for file in os.listdir('/tmp/ar/bootstrap_trees'):
            if file.endswith('.treefile'):
                rep_paths.append(Path('/tmp/ar/bootstrap_trees') / file)

        rep_paths = rep_paths[0:2]
        bootstrap_merge_replicates(path_ref, path_out, rep_paths, cpus=15)
        return



