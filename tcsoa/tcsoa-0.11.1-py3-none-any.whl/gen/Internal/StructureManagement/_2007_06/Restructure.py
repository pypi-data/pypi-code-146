from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, ItemRevision
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InsertLevelParameter(TcBaseObj):
    """
    This structure provides a set of input values for the insert level action.
    
    :var bomLines: the selected BOM lines above which to insert a level
    :var itemRevision: the item to insert above the selected BOM lines
    :var viewType: the bom view type
    :var isPrecise: is the BOM view precise?
    """
    bomLines: List[BOMLine] = ()
    itemRevision: ItemRevision = None
    viewType: BusinessObject = None
    isPrecise: bool = False


@dataclass
class MoveNodeParameter(TcBaseObj):
    """
    The structure provides a set of input values for move node action.
    
    :var newParent: the item to attach the pending-cut lines
    :var bomLines: the pending-cut BOM lines to move
    """
    newParent: BOMLine = None
    bomLines: List[BOMLine] = ()


@dataclass
class SplitOccurrenceParameter(TcBaseObj):
    """
    This structure provides a set of input values for the split occurrence action.
    
    :var bomLine: the selected BOM line from which to split occurrence
    :var quantity: the quantity to split from the original BOM lines
    """
    bomLine: BOMLine = None
    quantity: str = ''
