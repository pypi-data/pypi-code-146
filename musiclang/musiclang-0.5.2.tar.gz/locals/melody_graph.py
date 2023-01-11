import networkx as nx
from musiclang import Note, Melody
from musiclang.core.library import *
import networkx as nx
import numpy as np
from itertools import product


SEED = 3
SEED = np.random.randint(0, 2 ** 31)
random = np.random.RandomState(seed=SEED)


def value(n):
    return n.val + 7 * n.octave

def interval(n1, n2):
    return n2.val + 7 * n2.octave - n1.val - 7 * n1.octave

def construct_graph(patterns=None):
    if patterns is None:
        patterns = [Note("s", i, octave, duration) for i in range(7) for octave in [-1, 0, 1] for duration in [E]]
        patterns += [r.e, l.e]
    pairs = product(patterns, patterns)
    G = nx.Graph()
    for n in patterns:
        G.add_node(n)
    for n1, n2 in pairs:
        G.add_edge(n1, n2, proba=random.random())
    return G


def get_neighbor_with_proba(G, node):
    edges = G.edges(node, data=True)
    data = [(m[1], m[2]['proba']) for m in edges]
    probas = np.asarray([m[1] for m in data])
    probas /= np.sum(probas)
    data = [m[0] for m in data]
    next_note = random.choice(data, p=probas)
    return next_note

def sample_with_proba(G, n, start_note=None, rg=None):
    melody = None
    current_note = start_note
    if current_note is None:
        current_note = rg.choice(G.nodes)
    for i in range(n):
        current_note = get_neighbor_with_proba(G, current_note)
        melody += current_note

    return melody



# TRANSFORM FUNCTIONS
def reverse(melody):
    return Melody([n for n in melody.notes[::-1]])

def transpose(melody, n=1):
    return melody & n

# Merging functions



### START ALGORITHM
N_STEPS = 4
N_PATTERNS = 6
PATH_LENGTH = 2

# PHRASE = THEME + 
TRANSFORMS = [reverse,
              lambda x: transpose(x, 1), lambda x: transpose(x, -1),
                #lambda x: transpose(x, 2), lambda x: transpose(x, -2),
                #lambda x: transpose(x, 3), lambda x: transpose(x, -3)
              ]
# Init graph

# Create a graph with transition probability of melodies

# Sample

patterns = None
for i in range(N_STEPS):
    G = construct_graph(patterns=patterns)
    # Pattern generation
    # Sample a 4 note graph
    patterns = [sample_with_proba(G, PATH_LENGTH, start_note=None, rg=random) for p in range(N_PATTERNS)]
    print(patterns)

    # Transformation generation
    patterns = [transform(pattern) for pattern in patterns for transform in TRANSFORMS]
    # Merging steps

melody = patterns[0]
print(melody)
# Melody = sum of patterns
#print(melody)
I(piano__0=melody).to_midi(filepath='locals/test.mid')