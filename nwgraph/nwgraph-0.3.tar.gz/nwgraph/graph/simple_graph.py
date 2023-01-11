"""Simple graph module"""
from typing import Dict, List
from overrides import overrides
import torch as tr
from .graph import Graph
from ..message import Message
from ..node import Node

class SimpleGraph(Graph):
    """Simple graph class"""
    @overrides
    def message_pass(self, t: int) -> Dict[Node, List[Message]]:
        # Pass all messages to the neighbours
        for edge in self.edges:
            edge.message_pass(edge.input_node.state, t)
        # Only put nodes in the messages dict if any messages were exchanged this step.
        nodes_messages = {node: node.messages for node in self.nodes if len(node.messages) > 0}
        return nodes_messages

    @overrides
    def aggregate(self, messages: Dict[Node, List[Message]], t: int) -> Dict[Node, tr.Tensor]:
        # Simplest aggregation step, sum the messages
        return {node_name: sum(m.content for m in node_messages) for node_name, node_messages in messages.items()}

    @overrides
    def update(self, aggregation: Dict[Node, tr.Tensor], t: int) -> Dict[Node, tr.Tensor]:
        # Simplest update step. Return whatever the aggregate function computed.
        return aggregation
