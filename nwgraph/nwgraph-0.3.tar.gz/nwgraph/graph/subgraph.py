"""subgraph module"""
from __future__ import annotations
from typing import Dict, List, Union
from copy import copy, deepcopy
import torch as tr
from torch import nn
from ..edge import Edge
from ..logger import logger
from ..utils import compare_two_states

@tr.no_grad()
def subgraph_for_edge(graph: "Graph", edge: Edge, in_nodes: Union[Dict[str, tr.Tensor], List[str]], t: int,
                      check_subgraph_message_pass: bool = False, use_original_graph: bool = False,
                      deepcopy_original_graph: bool = True) -> "Graph":
    """
    Creates a subgraph for a given edge of a graph, a st of input nodes (or input states) and the number of
    iterations (t) in the message passing loop
    """
    if use_original_graph:
        assert isinstance(in_nodes, dict), "When using the original graph, in_nodes must be an input dict"
        return subgraph_for_edge_mp(graph, edge, in_nodes, t, check_subgraph_message_pass)

    if isinstance(in_nodes, dict):
        in_nodes = list(in_nodes.keys())
    return subgraph_for_edge_fake_linear_graph_(graph, edge, in_nodes, t,
                                                check_subgraph_message_pass, deepcopy_original_graph)

def subgraph_for_edge_fake_linear_graph_(graph: "Graph", edge: Edge, in_nodes: List[str], t: int,
                                         check_subgraph_message_pass: bool = False,
                                         deepcopy_original_graph: bool = True):
    """
    A trick to compute the subgraph on a copy of the original graph, altering the edges properly to be linear with
    random data, instead of it being the original edges, which may be big neural networks.

    WARNING: This will alter the original graph. Make a deepcopy before calling this method or use
    deepcopy_original_graph set to True. Defaults to True. It may be much faster do not deepcopy it though, since
    the edges' models may be large. YMMV.
    """
    new_graph = deepcopy(graph) if deepcopy_original_graph else copy(graph)
    new_edge: Edge
    for new_edge in new_graph.edges:
        # We need to maintain identity models for CatEdges and other special edges that do not alter the input, but
        #  they just copy it.
        if isinstance(new_edge.model, nn.Identity):
            new_edge._model = nn.Identity() # pylint: disable=protected-access
        else:
            new_edge._model = nn.Linear(new_edge.in_dims, new_edge.out_dims) # pylint: disable=protected-access
    new_graph.edges = nn.ModuleList(new_graph.edges)
    new_edge = new_graph.name_to_edge[edge.name]
    new_in_nodes = [new_graph.name_to_node[node] for node in in_nodes]
    x = {node.name: tr.randn(node.num_dims) for node in new_in_nodes}

    # Call the original algorithm on the new graph, new edges and generated data
    new_subgraph = subgraph_for_edge_mp(new_graph, new_edge, x, t, check_subgraph_message_pass)

    if new_subgraph is None:
        return None
    # Return the subgraph of the original graph according to the fake subgraph on the fake data/edges
    edges_original_graph = [graph.name_to_edge[edge.name] for edge in new_subgraph.edges]
    subgraph = graph.subgraph(edges_original_graph)
    return subgraph

def subgraph_for_edge_mp(graph: "Graph", edge: Edge, x: Dict[str, tr.Tensor], t: int,
                         check_subgraph_message_pass: bool = False) -> "Graph":
    """
    Given a graph and an edge, run the graph for t timesteps, and based on the messages, obtain the subgraph
    required for that edge only. These are the edges that should exist in the subraph such that that particular edge
    can be trained or inferred (given some steps).

    Parameters:
    graph The original graph
    edge The edge for which we are building the subgraph
    x The message used for message passing when creating the subgraph
    t The number of steps to run the message on the original graph
        check_subgraph_message_pass If true, will send x on the subgraph to see if the edge's output node has a set
        state that is not the original one, when using the given message. If no state is updated, a warning is thrown.
    Returns: The found subgraph required for the edge, or None if the subgraph cannot be resolved. The last edge is
        always the required edge.
    """
    assert isinstance(x, dict), "The inputs must be a dictionary of {node => tensor}"
    for node_name in x.keys():
        assert isinstance(node_name, str)
    graph.forward(x, t)

    current_messages = [message for message in edge.output_node.messages if message.source == edge.name]
    distance = 0
    found_edges = set()

    while len(current_messages) > 0:
        new_messages = []
        distance += 1
        for msg in current_messages:
            if t - distance < msg.timestamp:
                continue
            msg_edge: Edge = graph.name_to_edge[msg.source]
            found_edges.add(msg_edge)
            new_messages.extend(msg_edge.input_node.messages)
        current_messages = new_messages

    if len(found_edges) == 0 or edge not in found_edges:
        logger.debug(f"Found edges: {found_edges}. Edge: {edge}. Have to return None!")
        return None
    # Reorder nicely, so the required edge is the last one.
    found_edges = [_edge for _edge in found_edges if _edge is not edge] + [edge]

    subgraph = graph.subgraph(found_edges)
    if check_subgraph_message_pass:
        subgraph.forward(x, 0)
        orig_state = edge.output_node.state
        subgraph.forward(x, t)
        new_state = edge.output_node.state
        if compare_two_states(orig_state, new_state):
            logger.warning(f"State of the output node of edge {edge} was not updated for the subgraph")
    subgraph._clear_messages() # pylint: disable=protected-access
    return subgraph

def graph_edge_subgraphs(self: "Graph", input_node_names: List[str], num_iterations: int) -> Dict[str, "Graph"]:
    """Builds the subgraphs required for this graph by doing a pass such that messages reach to that edge"""
    res = {}
    edge: Edge
    # deepcopy the subgraph here only once
    _graph = deepcopy(self)
    for edge in self.edges:
        subgraph = subgraph_for_edge(_graph, edge, input_node_names, num_iterations, deepcopy_original_graph=False)
        res[edge.name] = subgraph
    this_res = {}
    edge_graph: "Graph"
    # we know that the deepcopy was altered, but the subgraphs' edges names are okay, so we subgraph based on these
    #  altered edges from the original graph.
    for edge_name, edge_graph in res.items():
        if edge_graph is None:
            this_res[edge_name] = None
            continue
        this_res[edge_name] = self.subgraph(edge_graph.edges)
    return this_res
