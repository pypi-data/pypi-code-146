#!/usr/local/bin/python3

from graphe.digraph import symboldigraph
from graphe.digraph import topological
from graphe import draw

SG = symboldigraph.SymbolDigraph('../data/jobs.txt', '/')
TS = topological.Topological(SG.G)
names = SG.node_names()

print("Order of courses")
for i, v in enumerate(TS.get_order()):
    print(f'{i} {names[v]}')
