"""NGCEdge module"""
from __future__ import annotations
from typing import Dict
from pathlib import Path
from overrides import overrides
from torch import nn
from nwgraph import Node, Edge
from nwgraph.edge import DirectedEdge
import torch as tr

from ...logger import logger
from ...utils import ModelFn

class NGCEdge(DirectedEdge):
    """NGCEdge is the base class of all edges in the NGC project"""
    def __init__(self, input_node: Node, output_node: Node, name: str, model_type: ModelFn):
        self.model_type = model_type
        super().__init__(input_node, output_node, name)

    @property
    @overrides
    def edge_model(self) -> nn.Module:
        """Gets the edge model"""
        return self.model_type(self.input_node.num_dims, self.output_node.num_dims)

    def load_weights(self, edge_weights_file: Path):
        """Loads the weights given a path"""
        assert edge_weights_file.exists(), f"Edge '{self}' weights file: '{edge_weights_file}' does not exist."
        logger.debug2(f"Loading weight for {self} from '{edge_weights_file}'")
        state_dict: Dict = tr.load(edge_weights_file, map_location="cpu")["state_dict"]
        edge_keys = self.state_dict().keys()
        assert len(state_dict.keys()) == len(edge_keys)
        renamed_state_dict = {k: state_dict[k_old] for k, k_old in zip(edge_keys, state_dict.keys())}
        self.load_state_dict(renamed_state_dict, strict=True)

    @staticmethod
    def build_from_edge(edge: Edge) -> NGCEdge:
        """builds the ngc edge from a regular edge (for compatibility purposes mostly)"""
        return NGCEdge(edge.input_node, edge.output_node, edge.name, type(edge.edge_model))
