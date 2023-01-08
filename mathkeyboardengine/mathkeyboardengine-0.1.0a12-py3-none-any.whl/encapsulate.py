from typing import List
from .Placeholder import Placeholder
from .TreeNode import TreeNode

def encapsulate(nodes: List[TreeNode], encapsulatingPlaceholder: Placeholder) -> None:
  for node in nodes:
    node.parentPlaceholder = encapsulatingPlaceholder
    encapsulatingPlaceholder.nodes.append(node)
