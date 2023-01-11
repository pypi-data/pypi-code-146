from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GlobalConstantValue2(TcBaseObj):
    """
    Holds the name of the global constant and corresponding global constant value.
    
    :var key: Name of the global constant.
    :var value: The global constant value(s) corresponding to the specified constant.
    """
    key: str = ''
    value: List[str] = ()


@dataclass
class GlobalConstantValueResponse2(TcBaseObj):
    """
    Holds the response for the 'getGlobalConstantValues' operation.
    
    :var constantValues: The requested global constants.
    :var serviceData: This contains the status of the operation. A partial error is returned If the name global
    constant cannot be added to the global default cache (74502).
    """
    constantValues: List[GlobalConstantValue2] = ()
    serviceData: ServiceData = None
