from BranchingNode import BranchingNode
from insertWithEncapsulateCurrent import insertWithEncapsulateCurrent
from KeyboardMemory import KeyboardMemory
from encapsulate import encapsulate
from popSelection import popSelection
from coalesce import coalesce
from lastOrNone import lastOrNone

def insertWithEncapsulateSelectionAndPrevious(k: KeyboardMemory, newNode: BranchingNode) -> None:
  if len(newNode.placeholders) < 2:
    raise Exception('Expected 2 placeholders.')
  selection = popSelection(k)
  secondPlaceholder = newNode.placeholders[1]
  encapsulate(selection, secondPlaceholder)
  insertWithEncapsulateCurrent(k, newNode)
  k.current = coalesce(lastOrNone(selection), secondPlaceholder)
