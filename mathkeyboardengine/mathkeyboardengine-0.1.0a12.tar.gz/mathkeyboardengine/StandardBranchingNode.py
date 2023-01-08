from typing import List
from .BranchingNode import BranchingNode
from .KeyboardMemory import KeyboardMemory
from .LatexConfiguration import LatexConfiguration
from .Placeholder import Placeholder

class StandardBranchingNode(BranchingNode):
  def __init__(self, before: str, then: str, *rest: str) -> None:
    placeholderCount = len(rest) + 1
    placeholders : List[Placeholder] = [Placeholder() for i in range(0, placeholderCount)]
    super().__init__(placeholders)
    self.before = before
    self.then = then
    self.rest = rest

  def getLatexPart(self, k: KeyboardMemory, latexConfiguration: LatexConfiguration) -> str:
    latex = self.before + self.placeholders[0].getLatex(k, latexConfiguration) + self.then
    for i in range(0, len(self.rest)):
      latex += self.placeholders[i + 1].getLatex(k, latexConfiguration) + self.rest[i]
    return latex
