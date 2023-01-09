from mathkeyboardengine.KeyboardMemory import KeyboardMemory
from mathkeyboardengine._helpers.pop_selection import pop_selection

def delete_selection(k: KeyboardMemory) -> None:
  pop_selection(k)
