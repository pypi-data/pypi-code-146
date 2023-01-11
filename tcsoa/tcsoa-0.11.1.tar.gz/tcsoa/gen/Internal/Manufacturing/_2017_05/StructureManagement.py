from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PropertyData(TcBaseObj):
    """
    PropertyData containing synchronization result for the propertyName. This can be used for the result of dry run and
    for displaying the logs.
    
    :var propertyName: Name of the property. Supported values are:
    - status: Specifies the status of the operation. Valid values of status are "Pass", "Fail", "Partial" and "NA" (Not
    Applicable). "Pass" signifies that source and target object synchronization operation is passed, "Fail" signifies
    failed, "Partial" signifies partially passed and "NA" signifies that the operation is not applicable for the source
    and target object.
    - statusDisplayValue: Specifies if the result for synchronization operation is to be displayed or not in UI. Valid
    values are "True" and "False".
    - failedBOMLines: Specifies BOMLines for which synchronization operation is failed. Valid values are uid of the
    BOMLines.
    
    
    :var values: Value of the property. See propertyName for supported values.
    :var dataType: Type of the data. Supported values are: "boolean", "string" and "businessObject".
    """
    propertyName: str = ''
    values: List[str] = ()
    dataType: str = ''


@dataclass
class SyncMasterAndAlternativeInputInfo(TcBaseObj):
    """
    The input to the service is a structure which contains list of objects to be synchronized.
    
    :var syncStructsInfo: A list of SyncStructsInfo containing source and target object(s) to be synchronized.
    :var syncParams: A map (string, string) representing synchronization parameter and its value.
    Valid options are:
    - ("DryRun", "true") for validating the synchronization scenario before the actual updates are done.
    - ("ExcludeExistingStudy", "true") for synchronizing the study objects and to exclude the study objects if already
    present in target structure.
    
    """
    syncStructsInfo: List[SyncStructsInfo] = ()
    syncParams: SyncParams = None


@dataclass
class SyncMasterAndAlternativeResponse(TcBaseObj):
    """
    The response contains the list of synchronization results.
    
    :var serviceData: The service data containing partial errors.
    :var syncResult: A list of SyncResult containing result of syncMasterAndAlternative operation.
    """
    serviceData: ServiceData = None
    syncResult: List[SyncResult] = ()


@dataclass
class SyncResult(TcBaseObj):
    """
    A list of SyncResult containing result of syncMasterAndAlternative operation.
    
    :var source: The source object.
    :var target: The target object.
    :var resultData: A list of PropertyData containing synchronization result for the propertyName. This can be used
    for the result of dry run and for displaying the logs.
    """
    source: BusinessObject = None
    target: BusinessObject = None
    resultData: List[PropertyData] = ()


@dataclass
class SyncStructsInfo(TcBaseObj):
    """
    A list of SyncStructsInfo containing source and target object(s) to be synchronized.
    
    :var target: A list of target objects to be synchronized. It can be BOMLine or MECollaborationContext (CC) objects.
    :var source: A list of source BOMLine objects to be synchronized. It can be Study top line of type Mfg0BvrStudy or
    Operation line of type Mfg0BvrOperation.
    """
    target: List[BusinessObject] = ()
    source: List[BusinessObject] = ()


"""
A map (string, string) representing synchronization parameter and its value.
Valid options are:
- ("DryRun", "true") for validating the synchronization scenario before the actual updates are done.
- ("ExcludeExistingStudy", "true") for synchronizing the study objects and to exclude the study objects if already present in target structure.


"""
SyncParams = Dict[str, str]
