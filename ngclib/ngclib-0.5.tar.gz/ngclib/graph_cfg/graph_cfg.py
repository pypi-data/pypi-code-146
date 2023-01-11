"""Graph Cfg module"""
from pathlib import Path
from copy import copy
from typing import Union, Dict, Type, List
import numpy as np
import yaml
from ..logger import logger
from ..models import NGC, build_model_type
from ..utils import ConfigEdges


class GraphCfg:
    """
    Graph Cfg implementation. Nodes and edges are only strings/literals, no instantiations!

    Use NodesImporter() to instantiate nodes.
    """
    def __init__(self, graph_cfg: Union[Dict, Path], ngc_type: Type[NGC] = None):
        self.path = None
        self.cfg = self._read_cfg(graph_cfg)
        self._validate_cfg()
        if ngc_type is None:
            ngc_type = build_model_type(self.cfg["NGC-Architecture"])
            logger.debug(f"Model type was not explictly given. Building from a default architecture: {ngc_type}")
        self.ngc_type = ngc_type
        self.seed = int(self.cfg["seed"]) if "seed" in self.cfg else 42
        self.edges_raw: ConfigEdges = self.cfg["edges"]

        self._node_names: List[str] = None
        self._node_types: List[str] = None
        self._input_nodes: List[str] = None
        self._output_nodes: List[str] = None
        self._edges: List[str] = None
        self.node_args: Dict[str, Dict] = self._get_nodes_args()

    @property
    def node_names(self) -> List[str]:
        if self._node_names is None:
            node_names: List[str] = self.cfg["nodes"]["names"]
            node_types: List[str] = self.cfg["nodes"]["types"]
            filtered_nodes = self.ngc_type.nodes_from_cfg_edges(self.cfg["edges"], node_names,
                                                                self.cfg["nodes"]["inputNodes"])
            filtered_ixs = [node_names.index(n) for n in filtered_nodes]
            filtered_types = [node_types[ix] for ix in filtered_ixs]
            arg_sort = np.argsort(filtered_nodes)
            filtered_nodes = list(np.array(filtered_nodes)[arg_sort])
            filtered_types = list(np.array(filtered_types)[arg_sort])

            self._node_names = filtered_nodes
            self._node_types = filtered_types

        return self._node_names

    @property
    def node_types(self) -> List[str]:
        if self._node_types is None:
            _ = self.node_names
        return self._node_types

    @property
    def input_nodes(self) -> List[str]:
        """List of inputs nodes (names), sorted"""
        if self._input_nodes is None:
            self._input_nodes = sorted(list(set(self.cfg["nodes"]["inputNodes"]).intersection(self.node_names)))
        return self._input_nodes

    @property
    def output_nodes(self) -> List[str]:
        """List of output nodes (names), sorted"""
        if self._output_nodes is None:
            self._output_nodes = sorted(list(set(self.node_names).difference(self.input_nodes)))
        return self._output_nodes

    @property
    def edges(self) -> List[str]:
        """Converts the edges raw strings to the names of the edges w/o instantiating them using the ngc type"""
        if self._edges is None:
            self._edges = []
            for edge_type, edges in self.edges_raw.items():
                for edge in edges:
                    edge_name = self.ngc_type.edge_name_from_cfg_str(edge_type, edge,
                                                                     self.node_names, self.input_nodes)
                    self._edges.append(edge_name)
        return self._edges

    def _validate_cfg(self):
        """Basic consistency validation"""
        if "edges" not in self.cfg:
            logger.warning("No edegs in graph cfg")
            self.cfg["edges"] = []
        assert "nodes" in self.cfg, f"'nodes' key not in the graph cfg: {self.cfg}"
        assert "types" in self.cfg["nodes"], f"No node types in graph cfg. Most likely an error. {self.cfg}"
        assert "names" in self.cfg["nodes"], f"No node names in graph cfg. Most likely an error. {self.cfg}"
        assert "inputNodes" in self.cfg["nodes"], "No input nodes in graph cfg."
        node_names, node_types = self.cfg["nodes"]["names"], self.cfg["nodes"]["types"]
        assert len(node_names) > 0, "At least one node must exist"
        assert len(node_names) == len(node_types), f"Names and types mismatch: {len(node_names)} vs {len(node_types)}"
        assert len(self.cfg["nodes"]["inputNodes"]) > 0, "No input nodes in graph cfg"
        if "hyperParameters" not in self.cfg or self.cfg["hyperParameters"] is None:
            self.cfg["hyperParameters"] = {}

    def _read_cfg(self, graph_cfg: Union[Dict, Path]) -> Dict:
        if isinstance(graph_cfg, (str, Path)):
            logger.info(f"Loading graph cfg from '{graph_cfg}'")
            self.path = graph_cfg
            graph_cfg = yaml.safe_load(open(graph_cfg, "r"))
        return copy(graph_cfg)

    def _get_nodes_args(self) -> Dict[str, Dict]:
        """Gets the arguments for each node, given its name. If no argument, an empty dict is set"""
        if not "hyperParameters" in self.cfg:
            return {node_name: {} for node_name in self.node_names}
        hparams = self.cfg["hyperParameters"]
        res = {}
        for node_name in self.node_names:
            if node_name not in hparams:
                res[node_name] = {}
            else:
                res[node_name] = hparams[node_name]
        return res

    def _setup_node_names(self):
        """Gets the names and types given the graph cfg and checks if any edges are left redundancy shrinking"""
        node_names, node_types = self.cfg["nodes"]["names"], self.cfg["nodes"]["types"]
        return node_names, node_types

    def __str__(self):
        f_str = f"""[Graph Cfg]
 - NGC Type: {self.ngc_type}
 - Node types: {self.node_types}
 - Node names: {self.node_names}
 - Input nodes: {self.input_nodes}
 - Output nodes: {self.output_nodes}
"""
        return f_str

    def __repr__(self):
        return str(self)
