from typing import List
from TreeNode import TreeNode
from PartOfNumberWithDigits import PartOfNumberWithDigits
from Placeholder import Placeholder

def encapsulateAllPartsOfNumberWithDigitsLeftOfIndex(exclusiveRightIndex: int, siblingNodes: List[TreeNode], toPlaceholder: Placeholder) -> None:
  for i in range(exclusiveRightIndex - 1, -1, -1):
    siblingNode = siblingNodes[i]
    if isinstance(siblingNode, PartOfNumberWithDigits):
      siblingNodes.remove(siblingNode)
      toPlaceholder.nodes.insert(0, siblingNode)
      siblingNode.parentPlaceholder = toPlaceholder
    else:
      break
