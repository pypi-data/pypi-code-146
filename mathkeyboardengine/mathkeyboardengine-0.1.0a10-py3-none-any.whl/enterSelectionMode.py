from .KeyboardMemory import KeyboardMemory
from .setSelectionDiff import setSelectionDiff

def enterSelectionMode(k: KeyboardMemory) -> None:
  setSelectionDiff(k, 0)
