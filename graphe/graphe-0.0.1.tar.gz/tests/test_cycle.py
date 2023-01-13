#!/usr/bin/env python3

from graphe.digraph import digraph
from graphe.digraph import cycle

import unittest

class TestGraph(unittest.TestCase):

    def test_manual(self):
        DG = digraph.Digraph(4)
        DG.add_edge(0, 1)
        DG.add_edge(1, 2)
        DG.add_edge(2, 3)
        cycl = cycle.DirectedCycle(DG)
        assert cycl.has_cycle() == False
        DG.add_edge(3, 1)
        cycl = cycle.DirectedCycle(DG)
        assert cycl.has_cycle() == True

        c = []
        while cycl.cycle:
            c.append(cycl.cycle.pop())

        print(f'cycle: {c}')







if __name__ == '__main__':
    unittest.main()
