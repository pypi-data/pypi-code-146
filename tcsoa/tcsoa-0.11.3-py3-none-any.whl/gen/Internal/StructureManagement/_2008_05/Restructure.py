from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ItemRevision
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReplaceInContextParameter(TcBaseObj):
    """
    This structure provides a set of input values for the replace in context action.
    
    :var bomLine: bomLine
    :var itemRevision: the item used to replace the item in context.
    """
    bomLine: BOMLine = None
    itemRevision: ItemRevision = None
