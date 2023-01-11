#!/usr/local/bin/python3

import sys
from mjcgraph.digraph import digraph
from mjcgraph.digraph import ddfo
from collections import deque


class KnSSCC():
    def __init__(self, Digraph):
        self.count = 0
        self.marked = [False for i in range(Digraph.V)]
        self.id = [0 for i in range(Digraph.V)]

        ddfs = ddfo.DepthFirstOrder(Digraph)
        print(ddfs.get_post())

        for v in ddfs.get_reverse_post():
            if not self.marked[v]:
                self.dfs(Digraph, v)
                self.count += 1


    def dfs(self, Digraph, v):
        self.marked[v] = True
        self.id[v] = self.count
        for w in Digraph.adj(v):
            if not self.marked[w]:
                self.dfs(Digraph, w)


    def strongly_connected(self, v, w):
        return self.id[v] == self.id[w]


    def get_id(self, v):
        return self.id[v]


    def get_count(self):
        return self.count



if __name__ == '__main__':

    DG = digraph.Digraph('../../data/tinyDG.txt')

    SCC = KnSSCC(DG)

    print(f'DG has {SCC.get_count()} components')
