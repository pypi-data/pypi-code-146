#!/usr/local/bin/python3

import sys
from mjcgraph import digraph
from mjcgraph import nfa
from mjcgraph import draw

nfa = nfa.NFA('((A*B|AC)D)')

print(nfa.G.G)

# fig = draw.Draw(digraph=True)
# fig.set_names(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
# fig.draw(nfa.G)
