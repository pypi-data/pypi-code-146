#!/usr/local/bin/python3

import sys
from mjcgraph import symbolgraph
from mjcgraph import draw

infile = "../data/routes.txt"

G = symbolgraph.SymbolGraph(infile)

fig = draw.Draw()
fig.set_names(G.keys)
fig.node_attr(width='0.3', height='0.3', shape='circle', style='filled',
              color='gray', fontcolor='black', fontsize='8')
fig.draw(G.graph())
