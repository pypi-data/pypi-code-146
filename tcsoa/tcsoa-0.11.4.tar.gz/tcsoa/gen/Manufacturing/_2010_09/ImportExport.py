from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportInput(TcBaseObj):
    """
    Input for importManufacturingFeatures
    
    :var fileName: The unique name of the PLMXML File in the transient volume.
    :var root: The root object (in the structure to which we import the data). The root is always a BOMLine that
    corresponds to an item in the product structure.
    """
    fileName: str = ''
    root: BusinessObject = None


@dataclass
class ImportResponse(TcBaseObj):
    """
    The output of importManufaturingFeatures
    
    :var serviceData: The service data
    :var logFileFullPath: The full path of the log file (created by the import).
    """
    serviceData: ServiceData = None
    logFileFullPath: str = ''
