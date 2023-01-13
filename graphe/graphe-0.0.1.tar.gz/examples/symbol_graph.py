#!/usr/local/bin/python3

import sys
from graphe.digraph import symbolgraph
from graphe import draw

G = symbolgraph.SymbolGraph('../data/jobs.txt', '/')

fig = draw.Draw(digraph=True)
fig.set_names(G.keys)
fig.node_attr(width='0.3', height='0.3', shape='', style='',
              color='gray', fontcolor='black', fontsize='4')
fig.draw(G.graph())
