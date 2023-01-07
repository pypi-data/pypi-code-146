#!/usr/local/bin/python3

import sys
from mjcgraph import symbolgraph
from mjcgraph import bfs
from mjcgraph import draw

SG = symbolgraph.SymbolGraph('../data/routes.txt')

b = bfs.BFSearch(SG.graph(), SG.ST['LAX'])
path = b.path_to(SG.ST['HOU'])

fig = draw.Draw()
fig.set_names(SG.node_names())
fig.node_attr(width='0.3', height='0.3', shape='circle', style='filled',
              color='gray', fontcolor='black', fontsize='8')
fig.draw(SG.graph(), path)
