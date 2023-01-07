from typing import Union
from BranchingNode import BranchingNode
from KeyboardMemory import KeyboardMemory
from Placeholder import Placeholder
from TreeNode import TreeNode
from coalesce import coalesce
from firstBeforeOrNone import firstBeforeOrNone
from lastOrNone import lastOrNone

def moveLeft(k: KeyboardMemory) -> None:
  if isinstance(k.current, Placeholder):
    if k.current.parentNode is None:
      return
    previousPlaceholder: Union[Placeholder, None] = firstBeforeOrNone(k.current.parentNode.placeholders, k.current)
    if previousPlaceholder is not None:
      k.current = coalesce(lastOrNone(previousPlaceholder.nodes), previousPlaceholder)
    else:
      ancestorPlaceholder = k.current.parentNode.parentPlaceholder
      nodePreviousToParentOfCurrent: Union[TreeNode, None] = firstBeforeOrNone(ancestorPlaceholder.nodes, k.current.parentNode)
      k.current = coalesce(nodePreviousToParentOfCurrent, ancestorPlaceholder)
  else:
    if isinstance(k.current, BranchingNode):
      placeholder = k.current.placeholders[-1]
      k.current = coalesce(lastOrNone(placeholder.nodes), placeholder)
    else:
      k.current = coalesce(firstBeforeOrNone(k.current.parentPlaceholder.nodes, k.current), k.current.parentPlaceholder)
