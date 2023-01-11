"""TwoHop link module"""
from typing import Callable, Dict
from pathlib import Path
from nwgraph.node import Node
import torch as tr
from .ngc_edge import NGCEdge
from ...logger import logger

class TwoHopLink(NGCEdge):
    """Two Hop link class implementation."""
    def __init__(self, single_link_input_node: Node, input_node: Node,
                 output_node: Node, name: str, model_type: Callable):
        super().__init__(input_node, output_node, name, model_type)
        self.single_link_input_node = single_link_input_node

    def load_weights(self, edge_weights_file: Path):
        assert edge_weights_file.exists(), f"Edge '{self}' weights file: '{edge_weights_file}' does not exist."
        logger.debug(f"Loading weight for {self} from '{edge_weights_file}'")
        state_dict: Dict = tr.load(edge_weights_file, map_location="cpu")["state_dict"]
        edge_keys = self.state_dict().keys()
        # Ensemble edges have 2 or more edges. We need just the last keys.
        # This assert may fail if edges use different models though.
        assert len(state_dict.keys()) % len(edge_keys) == 0
        orig_keys = list(state_dict.keys())
        renamed_state_dict = {}
        # We take the last N keys, assuming that this edge was the last one in the trained subgraph.
        for i, new_edge_key in enumerate(edge_keys):
            orig_state_dict_key = orig_keys[-len(edge_keys) + i]
            renamed_state_dict[new_edge_key] = state_dict[orig_state_dict_key]
        self.load_state_dict(renamed_state_dict, strict=True)
