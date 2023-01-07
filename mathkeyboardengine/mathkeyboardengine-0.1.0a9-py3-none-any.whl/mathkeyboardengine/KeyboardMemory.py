from typing import Union
from Placeholder import Placeholder
from TreeNode import TreeNode

class KeyboardMemory:
  def __init__(self) -> None:
    self.syntaxTreeRoot : Placeholder = Placeholder()
    self.current : Union[TreeNode, Placeholder] = self.syntaxTreeRoot
    self.selectionDiff : Union[int, None] = None
    self.inclusiveSelectionRightBorder : Union[TreeNode, None] = None
    self.inclusiveSelectionLeftBorder : Union[TreeNode, Placeholder, None] = None
