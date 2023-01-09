from typing import List
from .Placeholder import Placeholder
from .TreeNode import TreeNode

def encapsulate(nodes: List[TreeNode], encapsulating_placeholder: Placeholder) -> None:
  for node in nodes:
    node.parent_placeholder = encapsulating_placeholder
    encapsulating_placeholder.nodes.append(node)
