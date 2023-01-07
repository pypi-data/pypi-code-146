import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

import dendropy

from gtdblib.tree.polytomy import collapse_polytomy


def _create_test_tree():
    """
    #
    #          (seed)
    #       /        \
    #      /          \
    #    ch1 [80]     ch2 [50]
    #   /  \          /  \
    #  ch3 ch4       ch5 ch6
    """
    taxon_namespace = dendropy.TaxonNamespace(["A", "B", "C", "D", ])
    tree = dendropy.Tree(taxon_namespace=taxon_namespace)

    # Left branch
    ch1 = tree.seed_node.new_child(edge_length=1)
    ch1.label = '80'

    ch3 = ch1.new_child(edge_length=1.5)
    ch4 = ch1.new_child(edge_length=2.3)

    # Right branch
    ch2 = tree.seed_node.new_child(edge_length=1.26)
    ch2.label = '50'

    ch5 = ch2.new_child(edge_length=3.1)
    ch6 = ch2.new_child(edge_length=2.9)

    # Assign taxa
    ch3.taxon = taxon_namespace.get_taxon("A")
    ch4.taxon = taxon_namespace.get_taxon("B")
    ch5.taxon = taxon_namespace.get_taxon("C")
    ch6.taxon = taxon_namespace.get_taxon("D")

    return tree


class TestTreePolytomy(unittest.TestCase):

    def test_collapse_polytomy(self):

        tree = _create_test_tree()

        with tempfile.TemporaryDirectory() as tmp_dir:
            path_tmp = Path(tmp_dir) / 'test.tree'
            with open(path_tmp, 'w') as f:
                f.write(tree.as_string(schema='newick', suppress_rooting=True, unquoted_underscores=True))

            path_out = Path(tmp_dir) / 'out.tree'
            collapse_polytomy(path_tmp, path_out, 70)

            tree_collapsed = dendropy.Tree.get_from_path(str(path_out), schema='newick', rooting='force-rooted',
                                                         preserve_underscores=True)

        self.assertEqual(str(tree_collapsed), '((A:1.5,B:2.3)80:1.0,C:4.36,D:4.16)')

        pdm_a = tree.phylogenetic_distance_matrix()
        pdm_b = tree_collapsed.phylogenetic_distance_matrix()

        pdm_a_values = defaultdict(dict)
        for t1 in tree.taxon_namespace:
            for t2 in tree.taxon_namespace:
                pdm_a_values[t1.label][t2.label] = (pdm_a.patristic_distance(t1, t2))

        pdm_b_values = defaultdict(dict)
        for t1 in tree_collapsed.taxon_namespace:
            for t2 in tree_collapsed.taxon_namespace:
                pdm_b_values[t1.label][t2.label] = (pdm_b.patristic_distance(t1, t2))

        self.assertAlmostEqual(pdm_a_values['A']['B'], pdm_b_values['A']['B'])
        self.assertAlmostEqual(pdm_b_values['A']['C'], 6.86)
        self.assertAlmostEqual(pdm_b_values['A']['D'], 6.66)
        self.assertAlmostEqual(pdm_b_values['B']['C'], 7.66)
        self.assertAlmostEqual(pdm_b_values['B']['D'], 7.46)
