"""Ensemble edge module"""
from typing import Dict
from pathlib import Path
import torch as tr
from .ngc_edge import NGCEdge
from ...logger import logger

class EnsembleEdge(NGCEdge):
    """
    Ensemble edge takes 2 or more incoming pretrained edges, merges them and forwards on the final edges.
    Only the final one is trainable.
    """
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
