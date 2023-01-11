from mathkeyboardengine.KeyboardMemory import KeyboardMemory
from mathkeyboardengine.LatexConfiguration import LatexConfiguration

def get_edit_mode_latex(k : KeyboardMemory, latexconfiguration : LatexConfiguration) -> str:
  return k.syntax_tree_root.get_latex(k, latexconfiguration)
