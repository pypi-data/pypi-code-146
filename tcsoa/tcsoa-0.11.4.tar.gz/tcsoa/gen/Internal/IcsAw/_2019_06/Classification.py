from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict


@dataclass
class ClassifyCommandVisibilityInfoResp(TcBaseObj):
    """
    Structure representing the classification visibility information returned by getClassificationCmdVisibilityInfo
    operation.
    
    :var wso2ClassifyMap: A map (WorkspaceObject, bool) of workspace objects to corresponding boolean visibility value.
    True &ndash; WorkspaceObject is classifiable. "Add" command will be visible in Classification tab.
    False &ndash; WorkspaceObject is not classifiable. "Add" command will not be visible in Classification tab.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    wso2ClassifyMap: Wso2ClassifyMap = None
    serviceData: ServiceData = None


"""
Map of WorkspaceObject to corresponding Boolean visibility value.
"""
Wso2ClassifyMap = Dict[BusinessObject, bool]
