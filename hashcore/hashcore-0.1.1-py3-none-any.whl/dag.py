"""
The main DAG module, it contains definitions for nodes, edges and methods to walk the graph
"""

from .utils import check_type
from .errors import GraphError, NodeError, EdgeError
from hash import utils

class Node(object):
    """
    A graph node
    """
    def __init__(self, key, metadata) -> None:
        utils.check_type(key, str, NodeError, False, f"Node key must be a string: found {type(key)}")
        self.__key = key
        self.__metadata = metadata

    def __repr__(self) -> str:
        return f"<Node key: {self.__key}>"
    def __eq__(self, other: object) -> bool:
        if type(other) == str:
            return self.__key == other
        if type(other) == Node:
            return self.__key == other.getKey()
        raise NodeError(f"Cannot compare node with {type(other)}")
    def __hash__(self) -> int:
        return hash(self.__key)
    def getKey(self):
        return self.__key
    def getMetadata(self, key = None):
        if key:
            return self.__metadata.get(key)
        return self.__metadata
    def setMetadata(self, key, value):
        self.__metadata[key] = value
class Edge(object):
    """
    An edge between two nodes
    """
    def __init__(self, node1 : Node, node2 : Node) -> None:
        check_type(node1, Node, GraphError, False, f"Graph nodes should be of class hash.dag.Node : found {type(node1)}")
        check_type(node2, Node, GraphError, False, f"Graph nodes should be of class hash.dag.Node : found {type(node2)}")
        self.node1 = node1
        self.node2 = node2

    def __eq__(self, other: object) -> bool:
        if type(other) == Edge:
            return self.node1 == other.node1 and self.node2 == other.node2
        raise EdgeError(f"Cannot compare edge with {type(other)}")

    def __repr__(self) -> str:
        return f"<Edge node1: {self.node1}, node2: {self.node2}>"

class Graph(object):
    """
    A simple graph
    """
    def __init__(self) -> None:
        self.__nodes = []
        self.__edges = []

    def addEdge(self, edge : Edge):
        edge.node1 = self.addNode(edge.node1)
        edge.node2 = self.addNode(edge.node2)
        for e in self.__edges:
            if e == edge:
                return
        self.__edges.append(edge)
    def removeEdge(self, edge):
        for i in range(len(self.__edges)):
            if self.__edges[i] == edge:
                del self.__edges[i]
                return
    def addNode(self, node : Node):
        for n in self.__nodes:
            if n == node:
                return n
        self.__nodes.append(node)
        return node

    def upToEdges(self, node : Node) -> list:
        result = []
        for e in self.__edges:
            if e.node2 == node:
                result.append(e.node1)
        return result

    def downToEdges(self, node : Node) -> list:
        result = []
        for e in self.__edges:
            if e.node1 == node:
                result.append(e.node2)
        return result


    def check_loop(self, node):
        self.loop = False
        self.dfs_walk(node, self.__check_loop)
        return self.loop

    def __check_loop(self, node, neighbors, visited_nodes):
        for n in neighbors:
            if n in visited_nodes:
                self.loop = True
                return

    def dfs_walk(self, node : Node, callback):
        return self.__dfs_walk(node, callback, {})
    def __dfs_walk(self, node : Node, callback, visisted_nodes):
        if visisted_nodes.get(node.getKey()):
            return
        visisted_nodes[node.getKey()] = 1
        nodes = self.downToEdges(node)
        callback(node, nodes, visisted_nodes)
        for n in nodes:
            self.__dfs_walk(n, callback, visisted_nodes)

    def __walk_number(self, node, distance):
        if len(self.ns) == 0:
            node.label = 0
            self.ns[0] = [node]
        else:
            upToNodes = self.upToEdges(node)
            max_label = 0
            for n in upToNodes:
                try:
                    if n.label > max_label:
                        max_label = n.label
                except AttributeError:
                    return
            node.label = max_label + 1
            nodes = self.ns.get(node.label, [])
            if nodes:
                self.ns[node.label].append(node)
            else:
                self.ns[node.label] = [node]
    def __next_index(self, ns, index, max_num) -> int:
        for i in range(index + 1, max_num+1):
            try:
                ns[i]
                return i
            except KeyError:
                pass
    def walk_number(self):
        # Use kahn's algorithm
        l = [[]]
        s = []
        for n in self.__nodes:
            if len(self.upToEdges(n)) == 0:
                n.setMetadata("_index", 0)
                s.append(n)
        index = 1
        while len(s) != 0:
            node = s.pop(0)
            if node.getMetadata('_index') == index:
                index += 1
                l.append([])
            l[index-1].append(node)
            for n in self.downToEdges(node):
                self.removeEdge(Edge(node, n))
                if len(self.upToEdges(n)) == 0:
                    n.setMetadata("_index", index)
                    s.append(n)

        return l
    def bfs_walk_number(self, node):
        self.ns = {}
        self.bfs_walk(node, self.__walk_number)
        indices = self.ns.keys()
        num = max(indices)
        for i in range(num):
            try:
                self.ns[i]
            except KeyError:
                nextIndex = self.__next_index(self.ns, i, num)
                if nextIndex is None:
                    break
                self.ns[i] = self.ns[nextIndex]
                del self.ns[nextIndex]
        return self.ns

    def bfs_walk(self, node : Node, callback):
        q = [node]
        z = {
            node.getKey(): 1
        }
        e = {
            node.getKey(): 0
        }
        visited_nodes = []
        callback(node, 0)
        while len(q) != 0:
            n = q[0]
            del q[0]
            nodes = self.downToEdges(n)
            for nn in nodes:
                if z.get(nn.getKey()):
                    continue
                callback(nn, e[n.getKey()] + 1)
                try:
                    nn.label
                    z[nn.getKey()] = 1
                    e[nn.getKey()] = e[n.getKey()] + 1
                    q.append(nn)
                    visited_nodes.append(nn)
                except AttributeError:
                    continue

    def getNodes(self):
        return self.__nodes

    def getEdges(self):
        return self.__edges

    def __repr__(self) -> str:
        return f"Graph <edges: {self.__edges}>"
    def __eq__(self, __o: object) -> bool:
        if len(self.__nodes) != len(__o.__nodes):
            return False
        if len(self.__edges) != len(__o.__edges):
            return False
        for node in self.__nodes:
            upToNodes1 = self.upToEdges(node)
            upToNodes2 = __o.upToEdges(node)
            if len(upToNodes1) != len(upToNodes2):
                return False
            return upToNodes1 == upToNodes2
