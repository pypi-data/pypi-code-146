from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateArrangementsResponse(TcBaseObj):
    """
    GenerateArrangementsResponse struct
    
    :var fileTicket: The FMS ticket is used to get the generated PLMXML file.
    :var serviceData: The service data is used to report any partial failures.
    """
    fileTicket: str = ''
    serviceData: ServiceData = None
