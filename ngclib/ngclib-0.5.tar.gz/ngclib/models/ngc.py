"""NGC Graph Module"""
from __future__ import annotations
from typing import List, Dict
from abc import abstractmethod
from pathlib import Path
from nwgraph import Node, Edge
from nwgraph.graph import SimpleGraph

from .edges import NGCEdge
from ..logger import logger
from ..utils import VoteFn, ConfigEdges, NGCEdgeFn

class NGC(SimpleGraph):
    """NGC basic implementation"""
    def __init__(self, edges: List[NGCEdge], vote_fn: VoteFn, input_node_names: List[str]):
        edges = NGC._fix_ngc_edges(edges)
        super().__init__(edges)
        if len(set(input_node_names).intersection(self._nodes)) != len(input_node_names):
            logger.warning(f"{input_node_names} vs {[x.name for x in self._nodes]}. Removing additional input nodes.")
            input_node_names = list(set(input_node_names).intersection(self._nodes))
        self.vote_fn = vote_fn
        self.input_node_names = input_node_names
        self._ngc_subgraphs: Dict[str, NGC] = None

    @staticmethod
    @abstractmethod
    def edge_name_from_cfg_str(edge_type: str, cfg_edge_name: List[str], node_names: List[str],
                               input_node_names: List[str]) -> str:
        """Returns the edge name given a string from the graph cfg"""
        raise ValueError("TODO")

    @staticmethod
    @abstractmethod
    def nodes_from_cfg_edges(cfg_edges: ConfigEdges, node_names: List[str], input_node_names: List[str]) -> List[str]:
        """Simply returns the list of all nodes present in all edges. Useful for shrinking a bigger list of nodes"""
        logger.warning(f"This method must be overridden for filtering irrelevant nodes. Returning all of them.")
        return node_names

    @staticmethod
    @abstractmethod
    def build_edges(nodes: List[Node], cfg_edges: ConfigEdges, input_node_names: List[str],
                    ngc_edge_fn: NGCEdgeFn) -> List[Edge]:
        """Builds the edges for this ngc architecture."""
        raise ValueError("TODO")

    @property
    def input_nodes(self) -> List[Node]:
        """The input nodes of this graph"""
        return [self.name_to_node[node_name] for node_name in self.input_node_names]

    @property
    def output_nodes(self) -> List[Node]:
        """The output nodes of this graph"""
        return list(set(self._nodes).difference(self.input_nodes))

    @property
    def num_iterations(self) -> int:
        """The number of iterations, must be updated by each ngc architecture"""
        assert False, "TODO"

    @property
    def nodes(self) -> List[Node]:
        return [*self.input_nodes, *self.output_nodes]

    @property
    def ngc_subgraphs(self) -> Dict[str, NGC]:
        """Builds the subgraphs required for this graph by doing a pass such that messages reach to that edge"""
        if self._ngc_subgraphs is None:
            self._ngc_subgraphs = super().edge_subgraphs(self.input_node_names, self.num_iterations)
        return self._ngc_subgraphs

    def forward(self, x, num_iterations=None):
        return super().forward(x, self.num_iterations)

    def load_all_weights(self, weights_dir: Path):
        """Loads the weights of each edge from a previously training ngc dir"""
        logger.info(f"Loading all weights ({len(self.edges)} edges) from NGC weights dir: '{weights_dir}'")
        edge: NGCEdge
        for edge in self.edges:
            edge_weights_file = weights_dir / str(edge) / "checkpoints/model_best.ckpt"
            edge.load_weights(edge_weights_file)

    @staticmethod
    def _fix_ngc_edges(edges: List[Edge]) -> List[NGCEdge]:
        """If regular edges are given, convert to ngc edges. For compatibility purposes."""
        new_edges = []
        for edge in edges:
            if len(tuple(edge.parameters())) > 0:
                if not isinstance(edge, NGCEdge):
                    logger.warning(f"Edge '{edge}' is not an instance of NGCEdge. Trying to convert!")
                    edge = NGCEdge.build_from_edge(edge)
            new_edges.append(edge)
        assert len(edges) == len(new_edges), f"Before: {len(edges)}. After: {len(new_edges)}"
        return new_edges
