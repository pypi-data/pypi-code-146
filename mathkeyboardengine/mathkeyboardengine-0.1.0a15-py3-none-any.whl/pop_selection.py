from typing import List
from .KeyboardMemory import KeyboardMemory
from .leave_selection_mode import leave_selection_mode
from .Placeholder import Placeholder
from .TreeNode import TreeNode
from .first_before_or_none import first_before_or_none
from .coalesce import coalesce

def pop_selection(k: KeyboardMemory) -> List[TreeNode]:
  if k.selection_diff is None:
    raise Exception('Enter selection mode before calling this method.')
  if k.selection_diff == 0:
    leave_selection_mode(k)
    return []
  diff = k.selection_diff
  if isinstance(k.current, Placeholder):
    leave_selection_mode(k)
    return [k.current.nodes.pop(0) for i in range(diff)]
  else:
    siblings = k.current.parent_placeholder.nodes
    indexOfLeftBorder = siblings.index(k.inclusive_selection_left_border)
    k.current = coalesce(first_before_or_none(siblings, k.inclusive_selection_left_border), k.current.parent_placeholder)
    leave_selection_mode(k)
    return [siblings.pop(indexOfLeftBorder) for i in range(abs(diff))]
