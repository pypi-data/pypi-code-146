from typing import List
from mathkeyboardengine.KeyboardMemory import KeyboardMemory
from mathkeyboardengine.leave_selection_mode import leave_selection_mode
from mathkeyboardengine.Placeholder import Placeholder
from mathkeyboardengine.TreeNode import TreeNode
from mathkeyboardengine._helpers.first_before_or_none import first_before_or_none
from mathkeyboardengine._helpers.coalesce import coalesce

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
    index_of_left_border = siblings.index(k.inclusive_selection_left_border)
    k.current = coalesce(first_before_or_none(siblings, k.inclusive_selection_left_border), k.current.parent_placeholder)
    leave_selection_mode(k)
    return [siblings.pop(index_of_left_border) for i in range(abs(diff))]
