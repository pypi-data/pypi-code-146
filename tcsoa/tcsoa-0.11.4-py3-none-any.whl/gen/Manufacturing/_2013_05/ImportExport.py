from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportScope(TcBaseObj):
    """
    The detail input for importing manufacturing features.
    
    :var fileName: The full path of the PLMXML file
    :var container: The container under which manufacturing features are to be imported.
    :var importMode: The mode of import. The possible values of the import mode are as follows.     
    keepExistingFeatures - The existing discrete manufacturing features (MFGs)under the container should not be
    deleted.      refreshWholeContainer - The existing discrete manufacturing features under the container may be
    deleted.
    """
    fileName: str = ''
    container: BusinessObject = None
    importMode: str = ''


@dataclass
class AdvancedImportInput(TcBaseObj):
    """
    Advanced Input for importing the manufacturing features.
    
    :var context: A BOMLine object in the product structure. Under this object the connected parts of imported
    manufacturing features are searched.
    :var content: List of detail inputs. The detail input elaborates about the container, the import mode and the input
    PLMXML file.
    """
    context: BusinessObject = None
    content: List[ImportScope] = ()


@dataclass
class AdvancedImportResponse(TcBaseObj):
    """
    The response of PLMXML import of the manufacturing features.
    
    :var serviceData: The service data.The error conditions and the corresponding error codes are as listed below.     
    200373 Import is tried to be done from an incomplete PLMXML file.      200374 The preference
    MEImportMFGsManufacturingFeatureIdAttributeName does not have any value.      200376 The preference
    MEImportMFGsManufacturingFeatureIdAttributeName has incorrect value.      200375 The preference
    MEImportMFGsManufacturingFeatureIdAttributeName does not have any value.      200377 The preference
    MEImportMFGsManufacturingFeatureIdAttributeName has incorrect value.      200xxx Import has failed for a container.
    :var logFileName: The name of the generated log file.
    :var logFileTicket: The fms ticket for the transient file that captures the log of import.
    """
    serviceData: ServiceData = None
    logFileName: str = ''
    logFileTicket: str = ''
