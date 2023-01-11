#!/usr/local/bin/python3

from mjcgraph.digraph import digraph
from mjcgraph.digraph import digraphdfs
from mjcgraph import draw

import unittest

class TestDigraphDFSearch(unittest.TestCase):

    def test_medium(self):
        DG = digraph.Digraph('data/mediumG.txt')
        assert DG.V == 250

        dfsearch = digraphdfs.DirectedDFSearch(DG, 0)
        assert dfsearch.has_path_to(197)
        assert len(dfsearch.path_to(0)) == 1
        assert len(dfsearch.path_to(197)) == 8


    def test_tiny(self):
        DG = digraph.Digraph('data/tinyG.txt')
        assert DG.V == 13
        assert DG.E == 13

        dfsearch = digraphdfs.DirectedDFSearch(DG, 0)



if __name__ == '__main__':
    unittest.main()
