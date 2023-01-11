"""NGC V1 module"""
from __future__ import annotations
from typing import List, Dict
from overrides import overrides
from nwgraph import Node, Message, Edge, Graph
import torch as tr
from .edges import TwoHopLink, SingleLink
from .ngc import NGC
from ..utils import VoteFn, ConfigEdges, NGCEdgeFn

class NGCV1(NGC):
    """NGC V1 architecture. The original one with single links and two hops."""
    def __init__(self, edges: List[Edge], vote_fn: VoteFn, input_nodes: List[str]):
        super().__init__(edges, vote_fn, input_nodes)
        self.single_links = [edge for edge in self.edges if isinstance(edge, SingleLink)]
        self.two_hops = [edge for edge in self.edges if isinstance(edge, TwoHopLink)]
        assert len(self.single_links) + len(self.two_hops) == len(self.edges), "Only SL and TH allowed."
        for th in self.two_hops:
            sl_in, sl_out = th.single_link_input_node, th.input_node
            lookup = [sl.input_node == sl_in and sl.output_node == sl_out for sl in self.single_links]
            assert sum(lookup) == 1, f"Two hop {th} has no single link"

    @property
    def num_iterations(self) -> int:
        return 2

    def message_pass(self, t: int) -> Dict[Node, List[Message]]:
        res = {node: [] for node in self.output_nodes}
        if t == 0:
            # In t = 0, we send only the single links
            for edge in self.single_links:
                assert edge.input_node.state is not None
                res[edge.output_node].append(edge.message_pass(edge.input_node.state, t))
        if t == 1:
            # In t = 1, we send all the two hops, using the single links messages, not state,
            # which could be aggregated. This is true only for NGC-V1.
            for edge in self.two_hops:
                sl_messages = [message for message in edge.input_node.messages \
                    if self.name_to_edge[message.source].input_node == edge.single_link_input_node]
                assert len(sl_messages) == 1
                res[edge.output_node].append(edge.message_pass(sl_messages[0].content, t))
        res = {k: v for k, v in res.items() if len(v) > 0}
        return res

    def aggregate(self, messages: Dict[Node, List[Message]], t: int) -> Dict[Node, tr.Tensor]:
        res = {}
        for node, node_messages in messages.items():
            x = tr.stack([x.content for x in node_messages], dim=1)
            aggregated = self.vote_fn(x, [x.source for x in node_messages])
            res[node] = aggregated
        return res

    @staticmethod
    def edge_name_from_cfg_str(edge_type: str, cfg_edge_name: List[str], node_names: List[str],
                               input_node_names: List[str]) -> str:
        assert len(cfg_edge_name) in (2, 3), f"Got {cfg_edge_name}"
        assert edge_type in ("SL", "TH"), edge_type
        if edge_type == "SL":
            input_node, output_node = cfg_edge_name
            name = f"Single Link {input_node} -> {output_node}"
        else:
            single_link_input_node, input_node, output_node = cfg_edge_name
            name = f"TwoHop Link ({single_link_input_node} ->) {input_node} -> {output_node}"
        return name

    def nodes_from_cfg_edges(cfg_edges: ConfigEdges, node_names: List[str], input_node_names: List[str]) -> List[str]:
        res = []
        sls = cfg_edges["SL"] if "SL" in cfg_edges else []
        ths = cfg_edges["TH"] if "TH" in cfg_edges else []
        for str_edge in sls + ths:
            res.extend([name for name in str_edge])
        return list(set(res))

    @staticmethod
    def build_edges(nodes: List[Node], cfg_edges: ConfigEdges, input_node_names: List[str],
                    ngc_edge_fn: NGCEdgeFn) -> List[Edge]:
        """Builds NGCV1 edges: single links or two hops"""
        name_to_node = {node.name: node for node in nodes}
        assert len(cfg_edges) > 0
        sls = cfg_edges["SL"] if "SL" in cfg_edges else []
        ths = cfg_edges["TH"] if "TH" in cfg_edges else []

        res: List[Edge] = []
        for str_edge in sls:
            edge_name = NGCV1.edge_name_from_cfg_str("SL", str_edge, nodes, input_node_names)
            edge_nodes = [name_to_node[n] for n in str_edge]
            assert len(edge_nodes) == 2, str_edge
            assert edge_nodes[0] in input_node_names and edge_name[1] not in input_node_names
            edge = SingleLink(edge_nodes[0], edge_nodes[1], edge_name, ngc_edge_fn(edge_nodes[1]))
            res.append(edge)

        for str_edge in ths:
            edge_name = NGCV1.edge_name_from_cfg_str("TH", str_edge, nodes, input_node_names)
            edge_nodes = [name_to_node[n] for n in str_edge]
            assert len(edge_nodes) == 3, str_edge
            assert edge_nodes[0] in input_node_names and edge_nodes[1] not in input_node_names and \
                   edge_nodes[2] not in input_node_names, edge_nodes
            edge = TwoHopLink(edge_nodes[0], edge_nodes[1], edge_nodes[2], edge_name, ngc_edge_fn(edge_nodes[2]))
            res.append(edge)
        return res

    @overrides
    def subgraph(self, edges: List[Edge]) -> Graph:
        this_edges = [self.name_to_edge[edge.name] for edge in edges]
        subgraph_input_nodes = set()
        for edge in edges:
            for node in edge.nodes:
                if node in self.input_nodes:
                    subgraph_input_nodes.add(node.name)
        new_graph = type(self)(this_edges, self.vote_fn, subgraph_input_nodes)
        return new_graph
