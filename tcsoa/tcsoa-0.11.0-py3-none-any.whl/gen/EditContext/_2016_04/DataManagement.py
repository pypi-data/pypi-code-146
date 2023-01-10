from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List
from tcsoa.gen.BusinessObjects import WorkspaceObject, POM_object


@dataclass
class SetChangeContextResponse(TcBaseObj):
    """
    Contains the input edit context and the configured input objects.
    
    :var serviceData: Contains any partial errors that occur during the operation.
    :var configuredObjects: Contains the input edit context and the configured input objects.
    """
    serviceData: ServiceData = None
    configuredObjects: ChangeContextMap = None


"""
Maps the context used to configure objects and the list of configured objects.
"""
ChangeContextMap = Dict[WorkspaceObject, List[POM_object]]
