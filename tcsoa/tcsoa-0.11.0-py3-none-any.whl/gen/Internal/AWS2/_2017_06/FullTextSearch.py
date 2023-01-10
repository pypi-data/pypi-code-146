from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class IdentifyImpactedObjInput(TcBaseObj):
    """
    The input values for the identifyImpactedObjects operation.
    
    :var tieSyncStatus: TIE_sync_status value to mark impacted objects.
    Valid values are positive integers, defined in core/tie/tie_privileged.h
    Examples:
    1 = TIE_sync_status_replication_pending
    15 = TIE_sync_status_revrule_refresh_pending
    :var impactingOperations: bit values Add=1, Modified=2, Deleted=4
    :var returnObjIds: Should the operation return the list of impacted object UIDs.
    If true the operation will return the list of objects identified, if false list will be empty.
    """
    tieSyncStatus: int = 0
    impactingOperations: int = 0
    returnObjIds: bool = False


@dataclass
class IdentifyImpactedObjectsResponse(TcBaseObj):
    """
    The list of impacted Revisionable Object UIDs from the identifyImpactedObjects operation.
    
    :var impactedObjectsUIDs: List that contains the impacted object UIDs due to adds/modify/deletes that happened
    after last time index.
    :var serviceData: The Service Data
    """
    impactedObjectsUIDs: List[str] = ()
    serviceData: ServiceData = None
