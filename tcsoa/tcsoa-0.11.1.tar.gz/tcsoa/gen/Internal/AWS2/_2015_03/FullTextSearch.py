from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetAMImpactedObjectsResponse(TcBaseObj):
    """
    Data structure that holds the UIDs of Teamcenter business objects whose READ access is impacted by the Access
    Manager rule tree changes, a Boolean flag that indicates if full reindex is needed or not and the service data with
    any partial errors that might happen while finding the impacted objects.
    
    :var impactedUids: List of unique identifiers (UIDs) of Teamcenter business objects whose READ access is impacted
    by the Access Manager rule changes.
    :var queriedDateTime: The date and time at which the AM impacted objects are queried for. Require this to keep
    track of sync case.
    :var serviceData: The Service Data.
    """
    impactedUids: List[str] = ()
    queriedDateTime: datetime = None
    serviceData: ServiceData = None


@dataclass
class GetIndexedObjectsResponse(TcBaseObj):
    """
    Structure containing list of indexed object UIDs and service data with partial errors.
    
    :var indexedObjectsUIDs: The list of indexed object UIDs.
    :var serviceData: The Service Data.
    """
    indexedObjectsUIDs: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class GetModifiedObjectsToSyncResponse(TcBaseObj):
    """
    Structure containing the list of modified object UIDs since the last sync run and the timestamp when the query is
    executed to find the modified objects.
    
    
    
    :var modifiedObjectsUIDs: The list of object UIDs that were modified after they been exported and indexed.
    :var queriedDateTime: The timestamp at which the modified objects are queried.
    :var serviceData: The Service Data.
    """
    modifiedObjectsUIDs: List[str] = ()
    queriedDateTime: datetime = None
    serviceData: ServiceData = None
