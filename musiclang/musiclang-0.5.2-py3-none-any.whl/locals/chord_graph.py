import networkx as nx


from musiclang import *
from musiclang.core.library import *
import networkx as nx
from itertools import product

def get_notes(c):
        pitches_scale = set([i % 12 for i in c.scale_pitches])
        pitches = set([i % 12 for i in c.chord_pitches])
        return (c, pitches, pitches_scale)


def get_all_chords_and_pitches():
    modes = ['M', 'm', 'mm']

    tonalities = [Tonality(i, mode=mode) for mode in modes for i in
                  range(12)
                  ]

    chords = [Chord(i, extension=extension, tonality=tonality) for i in range(7) for tonality in tonalities for
              extension in [5, 7]]

    print(chords[0])
    chords = [get_notes(c) for c in chords]
    chords = [c for c in chords if c[1] is not None]
    return chords

# Get a distance graph between chords
def distance_between_chords(c1, c2, weight_notes=1, weight_tonality=0,
                            weight_cadenza=1, weight_proximity=1):
    # Play notes
    distance = 0

    n1, n2 = c1[1], c2[1]
    s1, s2 = c1[2], c2[2]
    notes_distance = (len(set.union(n1, n2)) - max(len(n1), len(n2)))
    #assert 1 >= notes_distance >= 0
    distance += weight_notes * notes_distance

    # Tonality distance (as of circle of fifths)
    tonality_distance = (len(set.union(s1, s2)) - max(len(s1), len(s2))) / max(len(s1), len(s2))
    distance += weight_tonality * tonality_distance ** 2

    # Cadenza bonus
    cadenza_bonus = 0
    # Proximity with 5th of chord bonus
    proximity_with_fifth_bonus = 0

    return distance

chords = get_all_chords_and_pitches()
print(len(chords))
idx1, idx2 = 0, 124


# Create distances matrix$
print('start distances')
distances = {(c1[0], c2[0]): distance_between_chords(c1, c2) for c1, c2 in product(chords, chords)}

from operator import itemgetter

def knn(graph, node, n):
    return list(map(itemgetter(1),
                    sorted([(e[2]['weight'], e[1])
                            for e in graph.edges(node, data=True)], key=lambda x: x[0])[:n]))

def knn_with_distances(graph, node, n):
    return list(sorted([(e[2]['weight'], e[1])
                            for e in graph.edges(node, data=True)], key=lambda x: x[0])[:n])


G = nx.Graph()


for c1, c2 in distances.keys():
    G.add_edge(c1, c2, weight=distances[c1, c2])

# Display 10 nearest neighbors of I.M
#print(knn_with_distances(G, I % I.M, 3))
path = nx.shortest_path(G, I % I.M, I % IV.s.m, weight='weight')
print(path)


distance = 0
for p1, p2 in zip(path[:-1], path[1:]):
    distance += G[p1][p2]['weight']

    print(distance, G[I % I.M][I % IV.s.m]['weight'])
from pdb import set_trace; set_trace()



# Display keys in a planar graph



