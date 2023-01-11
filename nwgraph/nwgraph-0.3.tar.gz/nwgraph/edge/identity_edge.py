"""Identity Edge module"""
from overrides import overrides
from torch import nn
from .directed_edge import DirectedEdge

class IdentityEdge(DirectedEdge):
    """Identity Edge class"""
    @property
    @overrides
    def edge_model(self) -> nn.Module:
        assert len(self.nodes) == 2
        return nn.Identity()

    @property
    @overrides
    def out_dims(self) -> int:
        """The edge's output dimensions of IdentityEdges is the same as the input node's (just copy information)"""
        return self.input_node.num_dims
