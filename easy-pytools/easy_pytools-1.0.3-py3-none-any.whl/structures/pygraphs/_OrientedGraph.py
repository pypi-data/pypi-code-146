from . import _Graph
from typing import Hashable
from math import inf as INF


class PyOrientedGraph(_Graph.PyGraph):
    def add_edge(self, value_from: Hashable, value_to: Hashable, weight: float = 1):
        self.add_vertex(value_from)
        self.add_vertex(value_to)

        self._graph_adj[value_from].add(value_to)
        self._adj_weights[(value_from, value_to)] = weight

    def edge_weight(self, value_from: Hashable, value_to: Hashable) -> float:
        if self.are_adjacent(value_from, value_to):
            return self._adj_weights[(value_from, value_to)]
        else:
            return INF

    def are_adjacent(self, value1: Hashable, value2: Hashable) -> bool:
        if value1 in self and value2 in self:
            return value2 in self._graph_adj[value1]
        else:
            raise ValueError(f"`{value1}` or `{value2}` not in graph")