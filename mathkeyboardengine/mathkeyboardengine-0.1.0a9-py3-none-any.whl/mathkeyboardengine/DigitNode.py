from KeyboardMemory import KeyboardMemory
from LatexConfiguration import LatexConfiguration
from PartOfNumberWithDigits import PartOfNumberWithDigits

class DigitNode(PartOfNumberWithDigits):
  def __init__(self, digit: str) -> None:
    super().__init__()
    self.latex = digit
  
  def getLatexPart(self, k: KeyboardMemory, latexConfiguration: LatexConfiguration) -> str:
    return self.latex
