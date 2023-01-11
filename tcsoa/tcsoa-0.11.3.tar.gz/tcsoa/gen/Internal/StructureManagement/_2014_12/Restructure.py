from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, Item, PSViewType, ItemRevision
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReplaceItemsParameter(TcBaseObj):
    """
    Input structure for the operation 'replaceItems'. The structure contains selected BOMLine, information related to
    replacement Item and the replace option.
    
    :var bomLine: The selected BOMLine to do the replace operation.
    :var item: The replacement Item.
    :var itemRevision: The replacement ItemRevision.
    :var viewType: The view type to be used in replace. It determines the BOMView Revision to be used for the
    occurrence of the ItemRevision. If the replacement ItemRevision has no BOMView Revision, uses NULLTAG .
    For additional information, please see the Structure Manager Guide.
    :var replaceOption: Replacement options.
    - 0 for replacing the selected occurrence.
    - 1 for replacing all sibling occurrences of the selected in the parent assembly. 
    - 2 for replacing all occurrences of the selected in the entire structure.
    
    """
    bomLine: BOMLine = None
    item: Item = None
    itemRevision: ItemRevision = None
    viewType: PSViewType = None
    replaceOption: int = 0
