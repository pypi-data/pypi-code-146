#!/usr/local/bin/python3

import sys
from mjcgraph import graph
from mjcgraph import draw

node_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

G = graph.Graph('../data/tinyG.txt')

fig = draw.Draw()
fig.set_names(node_names)
fig.node_attr(style='', fontcolor='black', fontsize='10')
fig.draw(G)
