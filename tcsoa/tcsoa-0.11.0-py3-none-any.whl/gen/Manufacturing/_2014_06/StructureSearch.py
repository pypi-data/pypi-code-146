from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SrchConnectedLinesOutput(TcBaseObj):
    """
    Object containing input connection and connected BOMLines.
    
    :var connectionLine: Input connection BOMLine.
    :var connectedLines: Connected BOMLine objects.
    """
    connectionLine: BusinessObject = None
    connectedLines: List[BusinessObject] = ()


@dataclass
class SrchConnectedLinesResponse(TcBaseObj):
    """
    Return object for searchConnectedLines operation.
    
    :var output: List of objects containing input connection and connected BOMLines.
    :var serviceData: Standard service data.
    """
    output: List[SrchConnectedLinesOutput] = ()
    serviceData: ServiceData = None
