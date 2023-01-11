from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetVPSRConditionsResponse(TcBaseObj):
    """
    Response structure for service operation 'getVPSRConditions'.
    
    :var condData: It is a list of 'ConditionData' structres which contain information of the conditions found.
    :var serviceData: Standard 'ServiceData' structure. It contains partial errors and failures along with the
    clientIds.
    """
    condData: List[ConditionData] = ()
    serviceData: ServiceData = None


@dataclass
class ConditionData(TcBaseObj):
    """
    A structure containing name and expression of a condition entry.
    
    :var condName: The name of condition.
    :var condExpress: The expression of condition.
    """
    condName: str = ''
    condExpress: str = ''
