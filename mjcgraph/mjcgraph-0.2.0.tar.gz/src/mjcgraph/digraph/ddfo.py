#!/usr/local/bin/python3

import sys
from mjcgraph.digraph import digraph
from collections import deque


class DepthFirstOrder():
    def __init__(self, DG):
        assert isinstance(DG, digraph.Digraph)
        self.marked = [False for i in range(DG.V)]
        self.pre = [-1 for i in range(DG.V)]
        self.post = [-1 for i in range(DG.V)]
        self.postorder = []
        self.preorder = []
        self.preCounter = 0
        self.postCounter = 0
        for v in range(DG.V):
            if not self.marked[v]:
                self.dfs(DG, v)

        assert self.check() == True


    def dfs(self, DG, v):
        self.marked[v] = True;
        self.pre[v] = self.preCounter
        self.preCounter += 1
        self.preorder.append(v);
        for w in DG.adj(v):
            if not self.marked[w]:
                self.dfs(DG, w)
        self.postorder.append(v)
        self.post[v] = self.postCounter
        self.postCounter += 1


    def check(self):
        # check that post(v) is consistent with post()
        r = 0
        for v in self.get_post():
            if self.get_postv(v) != r:
                print(f'r === {r}: post(v) and post() inconsistent')
                return False
            r += 1
        # check that pre(v) is consistent with pre()
        r = 0
        for v in self.get_pre():
            if self.get_prev(v) != r:
                print('pre(v) and pre() inconsistent')
                return False
            r += 1
        return True


    def get_prev(self, v):
        return self.pre[v]


    def get_postv(self, v):
        return self.post[v]


    def get_pre(self):
        return self.preorder


    def get_post(self):
        return self.postorder


    def get_reverse_post(self):
        new_lst = self.postorder[::-1]
        return new_lst


if __name__ == '__main__':

    DG = digraph.Digraph('../../data/tinyDAG.txt')
    dfo = DepthFirstOrder(DG)
    print(f'pre  : {dfo.get_pre()}')
    print(f'post : {dfo.get_post()}')
    print(f'rpost: {dfo.get_reverse_post()}')
