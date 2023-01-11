#!/usr/local/bin/python3

import sys
from mjcgraph.graph import graph
from mjcgraph.graph import bfs
from mjcgraph import draw

infile = "../data/mediumG.txt"

G = graph.Graph(infile)

bfs = bfs.BFSearch(G, 0)
bfpath = bfs.path_to(200)

fig = draw.Draw()
fig.node_attr(label='')
fig.draw(G, bfpath)
