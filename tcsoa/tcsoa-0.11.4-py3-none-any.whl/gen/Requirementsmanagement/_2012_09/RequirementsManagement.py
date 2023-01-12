from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetBOMLineInfo(TcBaseObj):
    """
    Structure represents the parameters required to get BOMLine after create.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var selectedBomLine: Parent BOMLine under which newly created BOMLine will be attached.
    :var newComp: Item for which BOMLine needs to be created.
    """
    clientId: str = ''
    selectedBomLine: BOMLine = None
    newComp: BusinessObject = None
