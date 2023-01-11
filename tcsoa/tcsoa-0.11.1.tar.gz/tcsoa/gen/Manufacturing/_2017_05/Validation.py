from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RegisteredCallbackObjectsResponse(TcBaseObj):
    """
    The response is the object containing registered callback function details and the service data
    
    :var parameters: The registered callback functions details for given input type.
    :var serviceData: Standard ServiceData member.
    """
    parameters: List[RegisteredCallbackParam] = ()
    serviceData: ServiceData = None


@dataclass
class RegisteredCallbackParam(TcBaseObj):
    """
    The data objects which contains the  details of customized registered callback functions.
    
    :var type: The registered callback function type. Supported types are: "Normalization_Callback",
    "MFG_ValidationChecksCallback" or any customized callback type used to register callback.
    :var library: The customization DLL name.
    :var name: The customization callback name.
    :var functionName: The registered callback function name.
    """
    type: str = ''
    library: str = ''
    name: str = ''
    functionName: str = ''
