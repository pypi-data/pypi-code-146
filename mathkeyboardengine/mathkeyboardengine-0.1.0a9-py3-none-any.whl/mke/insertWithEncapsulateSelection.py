from BranchingNode import BranchingNode
from insert import insert
from KeyboardMemory import KeyboardMemory
from moveRight import moveRight
from encapsulate import encapsulate
from popSelection import popSelection

def insertWithEncapsulateSelection(k: KeyboardMemory, newNode: BranchingNode) -> None:
  selection = popSelection(k)
  insert(k, newNode)
  if len(selection) > 0:
    encapsulatingPlaceholder = newNode.placeholders[0]
    encapsulate(selection, encapsulatingPlaceholder)
    k.current = selection[-1]
    moveRight(k)
