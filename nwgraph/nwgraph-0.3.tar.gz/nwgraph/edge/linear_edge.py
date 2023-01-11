"""Linear Edge module"""
from typing import List
from overrides import overrides
from torch import nn
from .directed_edge import DirectedEdge
from ..node import Node

class LinearEdge(DirectedEdge):
    """Linear edge implementation"""
    @property
    @overrides
    def edge_model(self) -> nn.Module:
        assert len(self.nodes) == 2
        nodes: List[Node] = self.nodes
        return nn.Linear(nodes[0].num_dims, nodes[1].num_dims)
