#!/usr/local/bin/python3

import sys
from graphe.graph import graph
from graphe.graph import dfs
from graphe import draw

infile = "../data/mediumG.txt"

G = graph.Graph(infile)
print(G.to_string())

dfs = dfs.DFSearch(G, 0)
dfpath = dfs.path_to(200)

fig = draw.Draw()
fig.node_attr(label='')
fig.edge_attr(color='gray', penwidth='0.75')
fig.draw(G, dfpath)
