from __future__ import annotations

from tcsoa.gen.AWS2._2017_06.UiConfig import ColumnConfigData
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOrResetUIColumnConfigResponse(TcBaseObj):
    """
    This structure returns information to the client about column configurations. The ServiceData contains information
    about errors encountered during processing.
    
    :var clientName: The client for which the configurations are applicable.
    :var columnConfigurations: List of column configurations data.
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    """
    clientName: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    serviceData: ServiceData = None
