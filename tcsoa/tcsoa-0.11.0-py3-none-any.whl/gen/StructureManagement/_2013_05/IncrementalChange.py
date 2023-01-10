from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, IncrementalChangeElement
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ObjectsICEInfo(TcBaseObj):
    """
    A structure to hold BOMLine or the MECfgLine component and their corresponding ICE.
    
    :var object: Business object (e.g. BOMLine, MECfgLine) for which the list of ICE are mapped with.
    
    :var ices: The list of structural ICE elements for the given business object.
    """
    object: BusinessObject = None
    ices: List[IncrementalChangeElement] = ()
