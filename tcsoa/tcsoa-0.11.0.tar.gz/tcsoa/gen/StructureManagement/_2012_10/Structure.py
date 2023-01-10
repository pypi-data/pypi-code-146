from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CutItemParam(TcBaseObj):
    """
    Structure contains the item revision to be deleted and the BOMWindow that is using it.
    
    :var parent: The BOMWindow where the selected items to be deleted appear.
    :var objs: A list of selected items to be deleted.
    """
    parent: BusinessObject = None
    objs: List[BusinessObject] = ()
