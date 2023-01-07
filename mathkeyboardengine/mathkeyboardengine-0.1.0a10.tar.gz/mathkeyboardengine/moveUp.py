from .KeyboardMemory import KeyboardMemory
from .BranchingNode import BranchingNode
from .Placeholder import Placeholder
from .coalesce import coalesce
from .lastOrNone import lastOrNone

def moveUp(k: KeyboardMemory) -> None:
  fromPlaceholder = k.current if isinstance(k.current, Placeholder) else k.current.parentPlaceholder
  suggestingNode: BranchingNode
  while True:
    if fromPlaceholder.parentNode is None:
      return
    suggestingNode = fromPlaceholder.parentNode
    suggestion = suggestingNode.getMoveUpSuggestion(fromPlaceholder)
    if suggestion is not None:
      k.current = coalesce(lastOrNone(suggestion.nodes), suggestion)
      return
    fromPlaceholder = suggestingNode.parentPlaceholder
