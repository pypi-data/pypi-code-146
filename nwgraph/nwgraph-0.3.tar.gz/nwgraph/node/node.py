"""Node module"""
from __future__ import annotations
from typing import List, Union, Dict
import torch as tr
from ..message import Message

class Node:
    """NWgraph Node class with a name and ndims for state shape"""
    def __init__(self, name: str, num_dims: int = None):
        assert isinstance(num_dims, int), f"Expected num_dims to be a number, got {num_dims}"
        self.name = name
        self.num_dims = num_dims

        # The state of the node is a tensor. For GT nodes, it is the GT data, however, for nodes that receive messages
        #  via their neighbours, this state is updated from the messages in the aggregate/update methods.
        self.state_history: Dict[int, tr.Tensor] = {}

        # Messages are the items received at this node via all its incoming edges.
        self.messages_history: Dict[int, List[Message]] = {}
        self._active_messages: List[Message] = []

    @property
    def state(self) -> tr.Tensor:
        """The state of this node is the last one in the history"""
        if len(self.state_history) == 0:
            return None
        last_key = tuple(self.state_history.keys())[-1]
        return self.state_history[last_key]

    @property
    def messages(self) -> List[Message]:
        """The list of messages of this node"""
        return list(self._active_messages)

    def reset(self):
        """Resets the node to initial state with no messages"""
        self.state_history = {}
        self.messages_history = {}
        self._active_messages = []

    def add_message(self, message: Message):
        """Adds a message to this node"""
        assert isinstance(message, Message)

        if message not in self._active_messages:
            self._active_messages.append(message)
        if message.timestamp not in self.messages_history:
            self.messages_history[message.timestamp] = []
        if message not in self.messages_history[message.timestamp]:
            self.messages_history[message.timestamp].append(message)

    def clear_messages(self):
        """Clear the messages of this node"""
        self._active_messages = []

    def set_state(self, state: tr.Tensor, timestamp: int):
        """Sets the state of this node (can also be None)"""
        assert isinstance(state, (tr.Tensor, type(None))), f"Got {type(state)}"
        if isinstance(state, tr.Tensor):
            assert state.shape[-1] == self.num_dims, f"Bad shape for the state: {state.shape} vs {self.num_dims}"
        assert timestamp not in self.state_history, f"Timestamp {timestamp} for '{str(self)}' already exist in history"
        self.state_history[timestamp] = state if isinstance(state, tr.Tensor) else None

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        state = tuple(self.state.shape) if self.state is not None else None
        return f"{self.name} (state: {state}, num_messages: {len(self.messages)}, num_dims: {self.num_dims})"

    # This and __eq__ are used so we can put node in dict and access them via strings
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, x: Union[Node, str]) -> bool:
        other_name = x.name if isinstance(x, Node) else x
        return self.name == other_name
