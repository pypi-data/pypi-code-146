from .KeyboardMemory import KeyboardMemory
from .LatexConfiguration import LatexConfiguration

def getEditModeLatex(k : KeyboardMemory, latexConfiguration : LatexConfiguration) -> str:
  return k.syntaxTreeRoot.getLatex(k, latexConfiguration)
