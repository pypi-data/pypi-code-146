from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ConfiguratorServiceResponse(TcBaseObj):
    """
    Represents the response object for executeConfiguratorService operation. It contains the response XML from the
    configurator service.
    
    :var responseData: This contains the service response xml. Details of response schemas are listed at
    "//plm/tcpmm10.1.1/tcbom/configurator/xids"
    :var serviceData: This member is provided by the standard SOA framework for all operations. It contains information
    about error status and additional objects that were affected in this operation.
    """
    responseData: str = ''
    serviceData: ServiceData = None
