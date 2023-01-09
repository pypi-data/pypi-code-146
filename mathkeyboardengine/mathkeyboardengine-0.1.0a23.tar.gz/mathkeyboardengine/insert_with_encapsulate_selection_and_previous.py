from mathkeyboardengine.BranchingNode import BranchingNode
from mathkeyboardengine.insert_with_encapsulate_current import insert_with_encapsulate_current
from mathkeyboardengine.KeyboardMemory import KeyboardMemory
from mathkeyboardengine._helpers.encapsulate import encapsulate
from mathkeyboardengine._helpers.pop_selection import pop_selection
from mathkeyboardengine._helpers.coalesce import coalesce
from mathkeyboardengine._helpers.last_or_none import last_or_none

def insert_with_encapsulate_selection_and_previous(k: KeyboardMemory, new_node: BranchingNode) -> None:
  if len(new_node.placeholders) < 2:
    raise Exception('Expected 2 placeholders.')
  selection = pop_selection(k)
  second_placeholder = new_node.placeholders[1]
  encapsulate(selection, second_placeholder)
  insert_with_encapsulate_current(k, new_node)
  k.current = coalesce(last_or_none(selection), second_placeholder)
