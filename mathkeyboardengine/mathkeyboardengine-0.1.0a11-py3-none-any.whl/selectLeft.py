from .KeyboardMemory import KeyboardMemory
from .Placeholder import Placeholder
from .TreeNode import TreeNode
from .coalesce import coalesce
from .setSelectionDiff import setSelectionDiff

def selectLeft(k: KeyboardMemory) -> None:
  oldDiffWithCurrent = coalesce(k.selectionDiff, 0)
  if (
    (isinstance(k.current, TreeNode) and k.current.parentPlaceholder.nodes.index(k.current) + oldDiffWithCurrent >= 0) or 
    (isinstance(k.current, Placeholder) and oldDiffWithCurrent > 0)
  ):
    setSelectionDiff(k, oldDiffWithCurrent - 1)
  elif (
    isinstance(k.inclusiveSelectionLeftBorder, TreeNode) and 
    k.inclusiveSelectionLeftBorder.parentPlaceholder.nodes.index(k.inclusiveSelectionLeftBorder) == 0 and
    k.inclusiveSelectionLeftBorder.parentPlaceholder.parentNode is not None
  ):
    k.current = k.inclusiveSelectionLeftBorder.parentPlaceholder.parentNode
    setSelectionDiff(k, -1)
