import unittest
from pathlib import Path

from gtdblib.tree.convert_accession import convert_tree_accessions_to_canonical


class TestTreeBootstrapMerge(unittest.TestCase):

    def test_bootstrap_merge_replicates_local(self):
        path_out = Path('/tmp/bac120_r2072.tree')
        path_ref = Path('/tmp/bac120_r207.tree')

        convert_tree_accessions_to_canonical(path_ref, path_out)
