"""Directed edge module"""
from .edge import Edge
from ..node import Node


class DirectedEdge(Edge):
    """A simple one directional edge where node A connects to node B."""
    def __init__(self, input_node: Node, output_node: Node, name: str = None):
        name = f"{input_node} ({input_node.num_dims}) -> {output_node} ({output_node.num_dims})" \
            if name is None else name
        super().__init__([input_node, output_node], name)
