from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetIndexedObjectsAndUpdateResponse(TcBaseObj):
    """
    Structure containing list of indexed objects UIDs and service data with partial errors.
    
    :var indexedObjectsUIDs: The list of indexed objects UIDs
    :var serviceData: The service data object
    """
    indexedObjectsUIDs: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class QueryAndUpdateDataInput(TcBaseObj):
    """
    Input structure containing option value to query and update the objects among newly added, modified, deleted or
    all. It also includes a boolean dryRun flag.
    
    The queryAndUpdateOptions value is passed to skip or process in finding and updating the newly added, modified,
    deleted objects. When dryRun flag is true, only queries will be executed and no updates to the records are made.
    This dryRun mode can be used to know the statistics about the objects that are awating sync.
    
    :var queryAndUpdateOptions: Bit values. Supported values are Add=1, Modified=2, Deleted=4
    :var dryRun: If true, in dry run mode Queries will be executed; however, no updates to records are made.
    """
    queryAndUpdateOptions: int = 0
    dryRun: bool = False


@dataclass
class QueryAndUpdateSyncDataResponse(TcBaseObj):
    """
    Response structure contains the information about what the operation has found. The partial errors are added to the
    service data.
    
    :var syncInfo: A map(string, list of strings) containing status counts or other  information that can be used for
    further processing.
    :var serviceData: The service data object.
    """
    syncInfo: SyncInfo = None
    serviceData: ServiceData = None


"""
A map containing information generated during the operation execution.
This includes information like count of objects found as newly added or modified or deleted that need to be synced. It can also contain other information like logfile names etc... needed by the caller.

The syncInfo will contain "STATUSCOUNT" as key and value is a list of strings as mentioned below with the counts of the objects found for the respective queries. Additional key/value pairs can be supported in future.
ADDED:<Count>
DELETED:<Count>
MODIFIED:<Count>
MODIFIED VIA RELATION:<Count>
"""
SyncInfo = Dict[str, List[str]]
