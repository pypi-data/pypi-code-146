"""NGC HyperEdges module"""
from typing import Dict, List
import torch as tr
from nwgraph import Message
from nwgraph.edge import Edge, IdentityEdge
from nwgraph.node import Node, CatNode
from .ngc import NGC, NGCEdgeFn, ConfigEdges
from .edges import SingleLink, EnsembleEdge, HyperEdge
from .ngc_ensemble import NGCEnsemble
from datetime import datetime

class NGCHyperEdges(NGC):
    """NGC HyperEdges module"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate_edges()

    def aggregate(self, messages: Dict[Node, List[Message]], t: int):
        res = {}
        for node, node_messages in messages.items():
            if len(node_messages) == 0:
                continue
            if isinstance(node, CatNode):
                cat_node = tr.cat([x.content for x in node_messages], dim=-1)
                if cat_node.shape[-1] == node.num_dims:
                    res[node] = cat_node
            else:
                mean_messages = tr.stack([message.content for message in messages[node]], dim=0).mean(dim=0)
                res[node] = mean_messages
        return res

    def update(self, aggregation: Dict[Node, tr.Tensor], t: int) -> Dict[Node, tr.Tensor]:
        return aggregation

    @property
    def num_iterations(self) -> int:
        return 4

    def subgraph(self, edges):
        this_edges = [self.name_to_edge[edge.name] for edge in edges]
        subgraph_input_nodes = set()
        for edge in edges:
            for node in edge.nodes:
                if node in self.input_nodes:
                    subgraph_input_nodes.add(node.name)
        new_graph = type(self)(this_edges, self.vote_fn, subgraph_input_nodes)
        return new_graph

    def _validate_edges(self):
        for edge in self.edges:
            assert isinstance(edge, (SingleLink, EnsembleEdge, HyperEdge, IdentityEdge)), f"{edge} => {type(edge)}"
            if isinstance(edge, SingleLink):
                assert edge.input_node in self.input_nodes and edge.output_node in self.output_nodes, edge

            if isinstance(edge, EnsembleEdge):
                assert edge.input_node in self.output_nodes and edge.output_node in self.output_nodes, edge

            if isinstance(edge, HyperEdge):
                assert isinstance(edge.input_node, CatNode)
                assert edge.output_node in self.output_nodes, edge
                if edge.name.startswith("H1"):
                    for node in edge.input_node.nodes:
                        assert node in self.input_nodes, edge
                elif edge.name.startswith("H2"):
                    assert False, "TODO H2"
                else:
                    assert False, "TODO"

    @staticmethod
    def edge_name_from_cfg_str(edge_type: str, cfg_edge_name: List[str], node_names: List[str],
                               input_node_names: List[str]) -> str:
        assert edge_type in ("SL", "ENS", "H1", "H2"), edge_type
        if edge_type in ("SL", "ENS"):
            return NGCEnsemble.edge_name_from_cfg_str(edge_type, cfg_edge_name, node_names, input_node_names)

        if edge_type == "H1":
            first_part = input_node_names if cfg_edge_name[0] == "*" else cfg_edge_name[0]
            assert isinstance(first_part, list), first_part
            for node_name in first_part:
                assert node_name in input_node_names, cfg_edge_name
            assert cfg_edge_name[1] not in input_node_names and cfg_edge_name[1] in node_names, cfg_edge_name
            name = ",".join(first_part)
            return f"H1 [{name}] -> {cfg_edge_name[1]}"

        if edge_type == "H2":
            assert False, "TODO"

        return None

    def nodes_from_cfg_edges(cfg_edges: ConfigEdges, node_names: List[str], input_node_names: List[str]) -> List[str]:
        nodes = NGCEnsemble.nodes_from_cfg_edges(cfg_edges, node_names, input_node_names)
        assert "H2" not in cfg_edges, "TODO"
        cfg_edges["H1"] = cfg_edges["H1"] if "H1" in cfg_edges else []
        for edge in cfg_edges["H1"]:
            first_part = input_node_names if edge[0] == "*" else edge[0]
            nodes.extend(first_part)
            nodes.append(edge[1])
        return list(set(nodes))

    @staticmethod
    def build_edges(nodes: List[Node], cfg_edges: ConfigEdges, input_node_names: List[str],
                    ngc_edge_fn: NGCEdgeFn) -> List[Edge]:
        assert len(cfg_edges) > 0
        ens_edges = NGCEnsemble.build_edges(nodes, cfg_edges, input_node_names, ngc_edge_fn)
        name_to_node = {node.name: node for node in nodes}
        h1s = cfg_edges["H1"] if "H1" in cfg_edges else []
        h2s = cfg_edges["H2"] if "H2" in cfg_edges else []
        cat_nodes: Dict[tuple, CatNode] = {}
        res: List[Edge] = []

        for str_edge in h1s:
            edge_name = NGCHyperEdges.edge_name_from_cfg_str("H1", str_edge, nodes, input_node_names)
            first_part = input_node_names if str_edge[0] == "*" else str_edge[0]
            input_nodes = tuple(name_to_node[n] for n in first_part)
            output_node = name_to_node[str_edge[1]]
            for input_node in input_nodes:
                assert input_node in input_node_names
            assert output_node not in input_nodes

            if input_nodes not in cat_nodes:
                cat_nodes[input_nodes] = CatNode(input_nodes)
            cat_node = cat_nodes[input_nodes]
            id_edges = [IdentityEdge(i, cat_node, name=f"Copy {i} -> {cat_node}") for i in input_nodes]
            out_edge = HyperEdge(cat_node, output_node, edge_name, ngc_edge_fn(output_node))
            res = [*res, *id_edges, out_edge]

        for str_edge in h2s:
            assert False, "TODO"

        return [*ens_edges, *res]
