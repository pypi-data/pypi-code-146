#!/usr/local/bin/python3

from mjcgraph.digraph import symboldigraph
from mjcgraph.digraph import topological
from mjcgraph import draw

SG = symboldigraph.SymbolDigraph('../data/jobs.txt', '/')
TS = topological.Topological(SG.G)
names = SG.node_names()

print("Order of courses")
for i, v in enumerate(TS.get_order()):
    print(f'{i} {names[v]}')
