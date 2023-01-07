from typing import Union
from Placeholder import Placeholder
from StandardBranchingNode import StandardBranchingNode

class AscendingBranchingNode(StandardBranchingNode):
  def getMoveDownSuggestion(self, fromPlaceholder: Placeholder) -> Union[Placeholder, None]:
    currentPlaceholderIndex = self.placeholders.index(fromPlaceholder)
    if currentPlaceholderIndex > 0:
      return self.placeholders[currentPlaceholderIndex - 1]
    else:
      return None  

  def getMoveUpSuggestion(self, fromPlaceholder: Placeholder) -> Union[Placeholder, None]:
    currentPlaceholderIndex = self.placeholders.index(fromPlaceholder)
    if currentPlaceholderIndex < len(self.placeholders) - 1:
      return self.placeholders[currentPlaceholderIndex + 1]
    else:
      return None
