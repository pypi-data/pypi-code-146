"""
Class for Directed Acyclic Graphs (DAGs).
"""
import logging
from .admg import ADMG
from .cg import CG
from .ug import UG
import itertools

logger = logging.getLogger(__name__)


class UndefinedDAGOperation(Exception):
    pass


class DAG(ADMG, CG):

    def __init__(self, vertices=[], di_edges=set(), **kwargs):
        """
        Constructor.

        :param vertices: iterable of names of vertices.
        :param di_edges: iterable of tuples of directed edges i.e. (X, Y) = X -> Y.
        """

        super().__init__(vertices=vertices, di_edges=di_edges, **kwargs)
        logger.debug("DAG")

    def d_separated(self, X, Y, separating_set=list()):
        """
        Computes d-separation for set `X` and set `Y` given `separating_set`

        :param X: first vertex set
        :param Y: second vertex set
        :param separating_set: separating set, default list()
        :return: boolean result of d-separation
        """
        if type(X) is str:
            X = [X]
        if type(Y) is str:
            Y = [Y]
        if type(separating_set) is str:
            separating_set = [separating_set]
        for x, y in itertools.product(X, Y):
            if not self._d_separated(x, y, separating_set):
                return False
        return True

    def _d_separated(self, X, Y, separating_set):
        """
        Determine whether two vertices are d-separated given other vertices. Also handles conditional DAGs
        
        :param X: first vertex
        :param Y: second vertex
        :param separating_set: list of given vertices
        
        :return: boolean result of d-separation
        """
        ancestral_vars = [X, Y] + list(separating_set)

        # create a new subgraph of the ancestors of X, Y, and separating vertices
        ancestral_subgraph = self.subgraph(self.ancestors(ancestral_vars))
        ancestral_vertices = list(ancestral_subgraph.vertices)
        ancestral_edges = list(ancestral_subgraph.di_edges)

        # add fixed variables which are not in X or Y to sepset
        for V in ancestral_subgraph.vertices.values():
            if V.fixed and V.name not in X and V.name not in Y:
                separating_set.append(V.name)

        # if both vertices are fixed, result is undefined
        if ancestral_subgraph.vertices[X].fixed and ancestral_subgraph.vertices[Y].fixed:
            raise UndefinedDAGOperation("{0} and {1} are fixed, so d-separation is undefined.".format(X, Y))

        for Vi, Vj in itertools.combinations(ancestral_vertices, 2):
            # fixed vertices are connected
            if ancestral_subgraph.vertices[Vi].fixed and ancestral_subgraph.vertices[Vj].fixed:
                ancestral_edges.append((Vi, Vj))

            ancestral_subgraph.vertices[Vi].fixed = False
            ancestral_subgraph.vertices[Vj].fixed = False

        # retrieves all combinations of the graph's vertices
        pairs_of_vertices = [list(pair) for pair in itertools.combinations(ancestral_vertices, 2)]

        # checks for common children between any pairs of vertices
        # if a pair of vertices has common children, an undirected edge connects the vertices
        for Vi, Vj in pairs_of_vertices:
            children_i = set(ancestral_subgraph.children(Vi))
            children_j = set(ancestral_subgraph.children(Vj))
            common_children = children_i.intersection(children_j)
            if len(common_children) > 0:
                ancestral_edges.append((Vi, Vj))

        # removes given vertices from the graph
        for vertex in separating_set:
            ancestral_vertices.remove(vertex)

        # removes any edges from the graph that include any of the given vertices
        for edge in ancestral_edges[:]:
            if edge[0] in separating_set or edge[1] in separating_set:
                ancestral_edges.remove(edge)

        # creates a new undirected graph from the updated vertices and edges
        augmented_graph = UG(ancestral_vertices, ancestral_edges)

        # checks if vertex Y is in the block of vertex X
        Y_block = augmented_graph.block(X)

        return Y not in Y_block
