#!/usr/local/bin/python3

import sys
from graphe.graph import graph
from graphe import draw

infile = "../data/mediumG.txt"

G = graph.Graph(infile)
print(G.to_string())

fig = draw.Draw()
fig.node_attr(label='')
fig.draw(G)
