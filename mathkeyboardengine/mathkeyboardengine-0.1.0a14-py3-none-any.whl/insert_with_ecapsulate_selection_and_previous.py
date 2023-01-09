from .BranchingNode import BranchingNode
from .insert_with_encapsulate_current import insert_with_encapsulate_current
from .KeyboardMemory import KeyboardMemory
from .encapsulate import encapsulate
from .pop_selection import pop_selection
from .coalesce import coalesce
from .last_or_none import last_or_none

def insert_with_ecapsulate_selection_and_previous(k: KeyboardMemory, new_node: BranchingNode) -> None:
  if len(new_node.placeholders) < 2:
    raise Exception('Expected 2 placeholders.')
  selection = pop_selection(k)
  second_placeholder = new_node.placeholders[1]
  encapsulate(selection, second_placeholder)
  insert_with_encapsulate_current(k, new_node)
  k.current = coalesce(last_or_none(selection), second_placeholder)
