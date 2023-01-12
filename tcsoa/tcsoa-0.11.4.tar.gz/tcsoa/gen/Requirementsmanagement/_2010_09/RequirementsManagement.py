from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0BuildingBlockBOMLine
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MoveLineInfo(TcBaseObj):
    """
    'MoveLineInfo' structure represents the parameters required to re-sequence the selected Fnd0BuildingBlockBOMLine
    object in the BOM structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var operation: The operation integer value to decide the operation performed. Following operation can be supported
    by 'MoveLineInfo'.
    - Move Up
    - Move Down
    - Promote
    - Demote
    - Edit Number 
    
    
    :var selectedLine: The Fnd0BuildingBlockBOMLine object, on which operation will be performed.
    :var newNumber: The new Number property value, will be used when Edit Number operation will be performed.  Based on
    new property value selected BOM line will be moved in the BOM structure.
    """
    clientId: str = ''
    operation: int = 0
    selectedLine: Fnd0BuildingBlockBOMLine = None
    newNumber: str = ''


@dataclass
class MoveLineResponse(TcBaseObj):
    """
    MoveLineResponse structure contains the ServiceData object.
    
    :var serviceData: The Service Data.
    """
    serviceData: ServiceData = None
