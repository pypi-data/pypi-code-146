from .KeyboardMemory import KeyboardMemory
from .pop_selection import pop_selection

def delete_selection(k: KeyboardMemory) -> None:
  pop_selection(k)
