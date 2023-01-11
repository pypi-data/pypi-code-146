"""Edge module"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Union
from torch import nn
import torch as tr

from ..node import Node
from ..message import Message

class Edge(nn.Module, ABC):
    """
    Edge class implementation
    Parameters:
    input_node The input node
    output_node The output node
    name The name of the edge. If not provided, assigned to "input node -> output node"
    """
    def __init__(self, nodes: List[Node], name: str = None):
        assert isinstance(nodes, list)
        for node in nodes:
            assert isinstance(node, Node)
        super().__init__()
        if name is None:
            name = f"Edge ({', '.join([str(x) for x in nodes])})"
        self.name = name
        self.nodes = nodes
        # This is needed here, so torch tracks the parameters of the edge's model.
        self._model = self.edge_model
        assert isinstance(self.model, nn.Module), f"Got {type(self.model)}"

    @property
    @abstractmethod
    def edge_model(self) -> nn.Module:
        """Gets the model of this edge"""

    @property
    def model(self):
        """Access the edge's model. This two step method is used to overwrite models dynamically, if needed."""
        if self._model is None:
            self._model = self.edge_model
        return self._model

    @property
    def input_node(self) -> Node:
        """The edge's input node, defaulting to the first one"""
        return self.nodes[0]

    @property
    def output_node(self) -> Node:
        """The edge's output node, defaulting to the last one"""
        return self.nodes[-1]

    @property
    def in_dims(self) -> int:
        """The edge's input dimensions, defualting to the number of dimensions of the input node"""
        return self.input_node.num_dims

    @property
    def out_dims(self) -> int:
        """The edge's output dimensions, defualting to the number of dimensions of the output node"""
        return self.output_node.num_dims

    def forward(self, x) -> tr.Tensor:
        """Forward method"""
        return self.model.forward(x)

    def message_pass(self, x, t: int) -> Message:
        """Message pass, which is a forward as well as adding the message to the output node plus some metadata"""
        if x is None:
            return None

        equal_messages = [msg for msg in self.output_node.messages if msg.equal_without_content(str(self), x)]
        # Deduplication optimization before doing forward again.
        if len(equal_messages) > 0:
            assert len(equal_messages) == 1, "messages should be unique!"
            return equal_messages[0]

        y = self.forward(x)
        message = Message(content=y, source=str(self), timestamp=t, path={str(self): x.detach()})
        self.output_node.add_message(message)
        return message

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, x: Union[Edge, str]) -> bool:
        other_name = x.name if isinstance(x, Edge) else x
        return self.name == other_name
