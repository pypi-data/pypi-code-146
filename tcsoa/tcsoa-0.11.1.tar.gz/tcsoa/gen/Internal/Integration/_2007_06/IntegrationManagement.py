from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ConnectResponse(TcBaseObj):
    """
    Holds a ServiceData (ConnectResponse.serviceData), and number of licenses avaliable.
    
    :var outputVal: outputVal
    :var serviceData: serviceData
    """
    outputVal: int = 0
    serviceData: ServiceData = None
