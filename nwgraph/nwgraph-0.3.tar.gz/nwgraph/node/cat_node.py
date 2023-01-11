"""Cat node module"""
from typing import List
from .node import Node

class CatNode(Node):
    """Cat node implementation"""
    def __init__(self, nodes: List[Node], name: str = None):
        self.nodes = nodes
        dims = sum(x.num_dims for x in nodes)
        # "CatNode([A, B, C])" => [A,B,C]
        name = f"[{','.join([x.name for x in nodes])}]" if name is None else name
        super().__init__(name, dims)
