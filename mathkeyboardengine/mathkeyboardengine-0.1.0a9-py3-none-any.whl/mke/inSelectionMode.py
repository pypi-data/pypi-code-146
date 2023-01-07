from KeyboardMemory import KeyboardMemory

def inSelectionMode(k: KeyboardMemory) -> bool:
  return k.selectionDiff is not None
