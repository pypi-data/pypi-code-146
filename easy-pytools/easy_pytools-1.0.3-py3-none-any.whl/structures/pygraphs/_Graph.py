from typing import Hashable, Iterable
from math import inf as INF

from ..primitives import Queue


class PyGraph:
    def __init__(self):
        self._graph_vertex: set[Hashable] = set()
        self._graph_adj: dict[Hashable, set] = dict()
        self._adj_weights: dict[tuple[Hashable, Hashable], float] = dict()
        self._vertex_attr: dict[Hashable, set] = dict()

    def add_vertex(self, value: Hashable):
        if value not in self:
            self._graph_adj[value] = set()
            self._vertex_attr[value] = set()
            self._graph_vertex.add(value)

    def add_edge(self, value1: Hashable, value2: Hashable, weight: float = 1):
        self.add_vertex(value1)
        self.add_vertex(value2)

        self._graph_adj[value1].add(value2)
        self._graph_adj[value2].add(value1)
        self._adj_weights[(value1, value2)] = weight
        self._adj_weights[(value2, value1)] = weight

    def edge_weight(self, value1: Hashable, value2: Hashable) -> float:
        if (value1, value2) in self._adj_weights:
            return self._adj_weights[(value1, value2)]
        else:
            return INF

    def are_adjacent(self, value1: Hashable, value2: Hashable) -> bool:
        if value1 in self and value2 in self:
            return (value2 in self._graph_adj[value1]) and (value1 in self._graph_adj[value2])
        else:
            raise ValueError(f"`{value1}` or `{value2}` not in graph")

    def adjacents(self, value: Hashable) -> set:
        if value in self:
            return self._graph_adj[value]
        else:
            return None

    def travel(self, start_value: Hashable) -> Iterable[Hashable]:
        if start_value not in self:
            raise ValueError(f"`{start_value}` not in graph")

        visited = set()
        queue = Queue()
        queue.add(start_value)
        while not queue.is_empty():
            value = queue.next()
            visited.add(value)
            yield value
            for next_value in self._graph_adj[value]:
                if next_value not in visited:
                    queue.add(next_value)

    def travel_levels(self, start_value: Hashable) -> Iterable[tuple[Hashable, set[Hashable]]]:
        if start_value not in self:
            raise ValueError(f"`{start_value}` not in graph")

        visited = set()
        queue = [start_value]
        while queue:
            value = queue.pop(0)
            visited.add(value)
            yield value, self._graph_adj[value]
            for next_value in self._graph_adj[value]:
                if next_value not in visited:
                    queue.append(next_value)

    def minimal_path_deikstra(self, value_from: Hashable, value_to: Hashable) -> dict[str, list | float]:
        if not (value_from in self and value_to in self):
            raise ValueError(f"`{value_from}` or `{value_to}` not in graph")

        paths = dict()
        for v in self._graph_vertex:
            weight = self.edge_weight(value_from, v)
            path = [value_from, value_to] if weight < INF else []
            paths.update({v: {'path': path, 'weight': weight}})
        paths[value_from] = {'path': [value_from], 'weight': 0}
        unvisited = self._graph_vertex.copy()

        while unvisited:
            min_path = INF
            min_vertex = None
            for u in unvisited:
                if paths[u]['weight'] <= min_path:
                    min_path = paths[u]['weight']
                    min_vertex = u

            if min_path == INF:
                break

            unvisited.remove(min_vertex)
            for v, data in paths.items():
                if data['weight'] > (p := paths[min_vertex]['weight'] + self.edge_weight(min_vertex, v)):
                    paths[v]['weight'] = p
                    paths[v]['path'] = paths[min_vertex]['path'] + [min_vertex, v]
        return paths[value_to]

    def set_attr(self, vertex: Hashable, attr: Hashable):
        if vertex in self:
            self._vertex_attr[vertex].add(attr)
        else:
            raise ValueError(f"`{vertex}` not in graph")

    def del_attr(self, vertex: Hashable, attr: Hashable):
        if vertex in self:
            self._vertex_attr[vertex].remove(attr)
        else:
            raise ValueError(f"`{vertex}` not in graph")

    def get_attr(self, vertex: Hashable) -> set:
        if vertex in self:
            return self._vertex_attr[vertex]
        else:
            raise ValueError(f"`{vertex}` not in graph")

    def has_attr(self, vertex: Hashable, attr: Hashable) -> bool:
        if vertex in self:
            return attr in self._vertex_attr[vertex]
        else:
            raise ValueError(f"`{vertex}` not in graph")

    @property
    def vertexes(self) -> set:
        return self._graph_vertex.copy()

    def __contains__(self, value: Hashable) -> bool:
        return value in self._graph_vertex
