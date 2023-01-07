#!/usr/local/bin/python3

import sys

from mjcgraph import graph

class SymbolGraph():
    def __init__(self, infile):
        self.keys = [] # vertice index to name
        self.ST = {} # vertice name to index

        lines = open(infile).read().splitlines()
        for line in lines:
            res = line.split()
            assert len(res) == 2
            for i in res:
                if not i in self.ST:
                    self.ST[i] = len(self.ST)
                    self.keys.append(i)

        self.G = graph.Graph(len(self.ST))

        lines = open(infile).read().splitlines()
        for line in lines:
            res = line.split()
            assert len(res) == 2
            self.G.add_edge(self.ST[res[0]], self.ST[res[1]])


    def graph(self):
        return self.G


    def node_names(self):
        return self.keys

if __name__ == '__main__':
    sg = SymbolGraph('../../data/routes.txt')
    assert sg.G.V == 10
    assert sg.G.E == 18
    assert sg.keys[0] == 'JFK'
