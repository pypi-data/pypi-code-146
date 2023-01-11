"""Graph abstract class module"""
from __future__ import annotations
from abc import abstractmethod
from typing import Dict, List, Set, Optional
from torch import nn
import torch as tr

from ..utils import GraphDrawer
from ..node import Node
from ..edge import Edge
from ..logger import logger
from ..message import Message
from .subgraph import graph_edge_subgraphs
from .collect import graph_collect_states_and_messages

# A Graph is a list of Edges. Each edge is a FeedForward network between two nodes.
class Graph(nn.Module):
    """Graph class implementation"""
    def __init__(self, edges: List[Edge]):
        super().__init__()
        if len(list(set(edges))) != len(edges):
            len_before = len(edges)
            edges = list(set(edges))
            logger.warning(f"You have identical edges. Removing duplicates {len_before} => {len(edges)}")
        assert isinstance(edges, list), type(edges)
        assert len(edges) > 0, "No edges provided"
        self._nodes: List[Node] = Graph._get_nodes_from_edges(edges)
        assert len(self._nodes) > 0, f"Could not extract nodes from {edges}"
        self.edges = nn.ModuleList(edges)

    @property
    def name_to_node(self) -> Dict[str, Node]:
        """A dictionary between node names and the nodes"""
        return {node.name: node for node in self._nodes}

    @property
    def name_to_edge(self) -> Dict[str, Edge]:
        """A dictionary between edge names and the edges"""
        return {edge.name: edge for edge in self.edges}

    @property
    def nodes(self) -> List[Node]:
        """The nodes of the graph"""
        return sorted(self._nodes, key=lambda node: node.name)

    @abstractmethod
    def message_pass(self, t: int) -> Dict[Node, List[Message]]:
        """Method that defines how messages are sent in one iteration."""

    @abstractmethod
    def aggregate(self, messages: Dict[Node, List[Message]], t: int) -> Dict[Node, tr.Tensor]:
        """
        Aggregation function that must transform all the received messages of a node to one message after each
        iteration has finished. Basically f(node, [message]) = (node, message). Doing nothing will preserve the
        messages (old behaviour), however, you need to aggregate at the last step manually in your algorithm.
        """

    @abstractmethod
    def update(self, aggregation: Dict[Node, tr.Tensor], t: int) -> Dict[Node, tr.Tensor]:
        """Update function that updates the nodes' representation at the end of each iteration"""

    # Public methods
    def forward(self, x: Dict[str, tr.Tensor], num_iterations: int = 1):
        """
        The forward pass/message passing of a graph. The algorithm is as follows:
        - x represents the "external" data of this passing, which is the initial state of all input nodes
        - for n steps, do a message passing call, which will send the state of each node to all possible neighbours
        - after the messages are sent, we aggregate them and update the internal state
        - after all iterations are done, we return the current state of each node (copying it, so we don't alter)
        """
        self._clear_messages()
        self._add_gt_to_nodes(x)
        for i in range(num_iterations):
            messages = self.message_pass(i)
            aggregation = self.aggregate(messages, i)
            new_states = self.update(aggregation, i)
            for node, new_state in new_states.items():
                node.set_state(new_state, i)
        node_states = {node.name: node.state for node in self.nodes}
        return node_states

    def print_nodes_state(self):
        """Prints all the nodes states"""
        for node in self.nodes:
            print(repr(node))

    def draw(self, file_name: str, cleanup: bool = True, view: bool = False):
        """Draws graph using graphviz"""
        GraphDrawer(self.nodes, self.edges)(file_name, cleanup, view)

    def subgraph(self, edges: List[Edge]) -> Graph:
        """Given a subset of edges, build the subgraph of this graph"""
        this_edges = [self.name_to_edge[edge.name] for edge in edges]
        new_graph = type(self)(this_edges)
        return new_graph

    def edge_subgraphs(self, input_node_names: List[str], num_iterations: int) -> Dict[str, Graph]:
        """
        Given a list of input nodes and a number of iterations, return the subgraphs for each edge that would
        reach to each edge, one by one, or None, if no graph is possible.
        """
        return graph_edge_subgraphs(self, input_node_names, num_iterations)

    def find_edges_by_nodes(self, nodes: List[Node]) -> Optional[List[Edge]]:
        """Finds all the edges that math the required list of nodes in that order. Returns None if none exist."""
        res = []
        for edge in self.edges:
            if edge.nodes == nodes:
                res.append(edge)
        return res if len(res) > 0 else None

    def collect_states_and_messages(self, x: Dict[str, tr.Tensor], t: int) -> Dict[Node, Dict[str, tr.Tensor]]:
        """Given an input item (x), collect all the states and messages after traversing the graph t iterations"""
        return graph_collect_states_and_messages(self, x, t)

    # Private methods
    def _add_gt_to_nodes(self, x: Dict[str, tr.Tensor]):
        for node_name, gt_data in x.items():
            assert node_name in self.name_to_node, f"Node {node_name} is not in graph, but in GT data."
            self.name_to_node[node_name].set_state(gt_data, -1)

    def _clear_messages(self):
        """Clears all nodes' messages"""
        logger.debug2("Clearing node messages.")
        for node in self.nodes:
            node.reset()

    @staticmethod
    def _get_nodes_from_edges(edges: List[Edge]) -> Set[Node]:
        """Method to extract all nodes from the edges directly"""
        nodes = set()
        name_to_node = {}
        for edge in edges:
            A, B = edge.nodes
            nodes.add(A)
            nodes.add(B)
            if A.name in name_to_node:
                existing = name_to_node[A.name]
                assert id(existing) == id(A), f"Two node instances have the same name: {existing} vs {A}"
            if B.name in name_to_node:
                existing = name_to_node[B.name]
                assert id(existing) == id(B), f"Two node instances have the same name: {existing} vs {B}"
            name_to_node[A.name] = A
            name_to_node[B.name] = B
        logger.debug2(f"Extracted nodes {nodes} from the edges ({len(edges)})")
        return nodes

    def __str__(self) -> str:
        f_str = "Graph:"
        pre = "  "
        for edge in self.edges:
            edge_str = str(edge)
            f_str += f"\n{pre}-{edge_str}"
        return f_str
