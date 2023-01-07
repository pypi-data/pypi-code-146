from typing import Union
from KeyboardMemory import KeyboardMemory
from LatexConfiguration import LatexConfiguration
from Placeholder import Placeholder
from TreeNode import TreeNode

emptyKeyboardMemory = KeyboardMemory()

def getViewModeLatex(x : Union[KeyboardMemory, Placeholder, TreeNode], latexConfiguration : LatexConfiguration) -> str:
  syntaxTreeComponent = x.syntaxTreeRoot if isinstance(x, KeyboardMemory) else x
  return syntaxTreeComponent.getLatex(emptyKeyboardMemory, latexConfiguration)

def getEditModeLatex(k : KeyboardMemory, latexConfiguration : LatexConfiguration) -> str:
  return k.syntaxTreeRoot.getLatex(k, latexConfiguration)
