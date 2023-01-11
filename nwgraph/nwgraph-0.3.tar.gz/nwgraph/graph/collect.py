"""Collect states and messages algorithm"""
from typing import Dict, List
import torch as tr
from ..node import Node
from ..message import Message

def graph_collect_states_and_messages(self: "Graph", x: Dict[str, tr.Tensor], t: int) \
    -> Dict[Node, Dict[str, tr.Tensor]]:
    """Given an input item (x), collect all the states and messages after traversing the graph t iterations"""
    with tr.no_grad():
        _ = self.forward(x, t)
    collected_items = {}
    for node in self.nodes:
        node_items = {}
        for state_t, state in node.state_history.items():
            node_items[f"state_{state_t}"] = state if state is not None else None
        messages: List[Message]
        for msg_t, messages in node.messages_history.items():
            for message in messages:
                node_items[f"{message.source}_{msg_t}"] = message.content if message.content is not None else None
        collected_items[node.name] = node_items
    return collected_items
