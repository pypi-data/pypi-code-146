from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetGOPartSolutionsResponse(TcBaseObj):
    """
    The GetGOPartSolutionsResponse structure represents output of vector of APN of line of usages (part solution),
    instantiating architecture  bom window and the service data.
    
    :var louBomLine: vector of BOMLine of LOU
    :var archBomWindow: Instantiating Architecture Bom window
    :var serviceData: serviceData returned as response for retrieving
    information on LOU APN
    """
    louBomLine: List[BOMLine] = ()
    archBomWindow: BOMWindow = None
    serviceData: ServiceData = None


@dataclass
class GetPastePrimeInfo(TcBaseObj):
    """
    This structure contains the list of the source and target BOMLine objects and a flag to indicate which attributes
    needs to be copied from the source BOMLine to target BOMLine.
    
    :var parentBomLine: List of the target Architecture Breakdown or Architecture Breakdown Element BOMLine objects.
    
    :var componentBomLine: List of the source Architecture Breakdown Element BOMLine objects.
    
    :var flag: Flag to decide which attributes need to be copied from the source to the target BOMLine.
    If flag value is 1 then only variability will be copied from the source to target BOMLine.
    If flag value is 2 then variability and NVEs will be copied from the source to target BOMLine.
    If flag value is 3 then variability, NVEs and part solutions will be copied from the source to target BOMLine.
    """
    parentBomLine: List[BOMLine] = ()
    componentBomLine: List[BOMLine] = ()
    flag: int = 0
