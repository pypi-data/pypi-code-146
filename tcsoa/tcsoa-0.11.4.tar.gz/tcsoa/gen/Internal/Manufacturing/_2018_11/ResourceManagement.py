from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AutoPositionComponentByCSYSResponse(TcBaseObj):
    """
    Response from autoPositionComponentByCSYS
    
    :var serviceData: The service data containing partial errors if any.
    :var possibleSourceCSYSs: The list of CSYSs from parent component, if there are multiple possible CSYSs appropriate
    for positioning.
    :var possibleTargetCSYSs: The list of CSYSs from child component, if there are multiple possible CSYSs appropriate
    for positioning.
    """
    serviceData: ServiceData = None
    possibleSourceCSYSs: List[AutoPositioningOutput] = ()
    possibleTargetCSYSs: List[AutoPositioningOutput] = ()


@dataclass
class AutoPositioningOutput(TcBaseObj):
    """
    AutoPositioningOutput
    
    :var strCSYSBOMLine: CSYS BOMLine.
    :var strCSYSBOMLineName: Name of the CSYS.
    """
    strCSYSBOMLine: str = ''
    strCSYSBOMLineName: str = ''
