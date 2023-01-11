"""NGCEnsemble module"""
from typing import Dict, List
from nwgraph import Node, Edge, Message, Graph
from overrides import overrides
import torch as tr

from .ngc import NGC, NGCEdgeFn, ConfigEdges
from .edges import EnsembleEdge, SingleLink

class NGCEnsemble(NGC):
    """NGCEnsemble implementation"""
    @property
    def num_iterations(self) -> int:
        return 2

    @staticmethod
    @overrides
    def edge_name_from_cfg_str(edge_type: str, cfg_edge_name: List[str], node_names: List[str],
                               input_node_names: List[str]) -> str:
        assert edge_type in ("SL", "ENS"), edge_type
        edge_type = "Single Link" if edge_type == "SL" else "Ensemble"
        name = f"{edge_type} {cfg_edge_name[0]} -> {cfg_edge_name[1]}"
        return name

    def nodes_from_cfg_edges(cfg_edges: ConfigEdges, node_names: List[str], input_node_names: List[str]) -> List[str]:
        res = []
        sls = cfg_edges["SL"] if "SL" in cfg_edges else []
        enss = cfg_edges["ENS"] if "ENS" in cfg_edges else []

        for str_edge in sls + enss:
            res.extend([name for name in str_edge])
        return list(set(res))

    @staticmethod
    def build_edges(nodes: List[Node], cfg_edges: ConfigEdges, input_node_names: List[str],
                    ngc_edge_fn: NGCEdgeFn) -> List[Edge]:
        """Builds NGC-Ensemble edges: single links and ensemble edges"""
        sls = cfg_edges["SL"] if "SL" in cfg_edges else []
        enss = cfg_edges["ENS"] if "ENS" in cfg_edges else []
        name_to_node = {node.name: node for node in nodes}

        res: List[Edge] = []
        for str_edge in sls:
            edge_name = NGCEnsemble.edge_name_from_cfg_str("SL", str_edge, nodes, input_node_names)
            edge_nodes = [name_to_node[n] for n in str_edge]
            assert len(edge_nodes) == 2, str_edge
            assert edge_nodes[0] in input_node_names and edge_name[1] not in input_node_names, edge_name
            edge = SingleLink(edge_nodes[0], edge_nodes[1], edge_name, ngc_edge_fn(edge_nodes[1]))
            res.append(edge)

        for str_edge in enss:
            edge_name = NGCEnsemble.edge_name_from_cfg_str("ENS", str_edge, nodes, input_node_names)
            edge_nodes = [name_to_node[n] for n in str_edge]
            assert len(edge_nodes) == 2, str_edge
            assert edge_nodes[0] not in input_node_names and edge_nodes[1] not in input_node_names, edge_nodes
            edge = EnsembleEdge(edge_nodes[0], edge_nodes[1], edge_name, ngc_edge_fn(edge_nodes[1]))
            res.append(edge)
        return res

    @overrides
    def aggregate(self, messages: Dict[Node, List[Message]], t: int) -> Dict[Node, tr.Tensor]:
        assert t < 2, t
        res = {}
        for node, node_messages in messages.items():
            x = tr.stack([x.content for x in node_messages], dim=1)
            if t == 0:
                aggregated = x.median(dim=1)[0]
            else:
                aggregated = self.vote_fn(x, [x.source for x in node_messages])
            res[node] = aggregated
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
