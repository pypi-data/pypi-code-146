#!/usr/local/bin/python3

from mjcgraph.graph import graph
from mjcgraph.graph import dfs
from mjcgraph import draw

import unittest

class TestDFSearch(unittest.TestCase):

    def test_test(self):
        G = graph.Graph('data/mediumG.txt')

        dfsearch = dfs.DFSearch(G, 0)
        self.assertTrue(dfsearch.has_path_to(200))

        self.assertTrue(len(dfsearch.path_to(0)) == 1)
        self.assertEqual(len(dfsearch.path_to(200)), 71)


    def test_nopath(self):
        G = graph.Graph('data/tinyG.txt')

        dfsearch = dfs.DFSearch(G, 0)
        self.assertFalse(dfsearch.has_path_to(8))
        self.assertEqual(len(dfsearch.path_to(8)), 0)


    def test_count(self):
        G = graph.Graph('data/tinyG.txt')

        dfsearch = dfs.DFSearch(G, 8)
        self.assertEqual(dfsearch.count(), 1)


if __name__ == '__main__':
    unittest.main()
