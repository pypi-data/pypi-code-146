#!/usr/local/bin/python3

from graphe.digraph import digraph
from graphe import draw

import unittest

class TestGraph(unittest.TestCase):

    def test_manual(self):
        DG = digraph.Digraph(7)
        assert DG.V == 7
        assert DG.E == 0

        DG.add_edge(0, 1)
        DG.add_edge(0, 2)
        assert DG.E == 2
        assert len(DG.G[0]) == 2
        assert len(DG.G[1]) == 0
        assert len(DG.G[2]) == 0


    def test_reverse(self):
        DG = digraph.Digraph(7)
        DG.add_edge(0, 1)
        DG.add_edge(0, 2)
        assert len(DG.G[0]) == 2
        assert len(DG.G[1]) == 0
        assert len(DG.G[2]) == 0

        RDG = DG.reverse()
        print(RDG.G)
        assert len(RDG.G[0]) == 0
        assert len(RDG.G[1]) == 1
        assert len(RDG.G[2]) == 1


    def test_load(self):
        DG = digraph.Digraph('data/tinyDG.txt')
        assert DG.V == 13
        assert DG.E == 22


if __name__ == '__main__':
    unittest.main()
