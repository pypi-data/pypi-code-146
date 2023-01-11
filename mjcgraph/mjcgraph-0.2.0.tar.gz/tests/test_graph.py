#!/usr/local/bin/python3

from mjcgraph.graph import graph
from mjcgraph import draw

import unittest

class TestGraph(unittest.TestCase):

    def test_manual(self):
        G = graph.Graph(7)
        assert G.V == 7
        assert G.E == 0

        G.add_edge(0, 1)
        G.add_edge(1, 2)
        assert G.E == 2


if __name__ == '__main__':
    unittest.main()
