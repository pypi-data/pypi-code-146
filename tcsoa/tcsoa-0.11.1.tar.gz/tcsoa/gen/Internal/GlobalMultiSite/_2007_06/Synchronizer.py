from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GmsSyncStatus(TcBaseObj):
    """
    It holds input object in GSIdentity format and its sync status.
    
    :var candidateObject: Input GSIdentity string.
    :var syncStatus: The status of object which can be one of the following
    1.    OUT OF DATE
    2.    UP TO DATE
    3.    UNDETERMINED
    """
    candidateObject: str = ''
    syncStatus: str = ''


@dataclass
class ObjectsByClass(TcBaseObj):
    """
    It holds the class and list of objects belonging to that class which needs to be checked for modification.
    
    :var className: Class name for which modified objects are returned.
    :var objectsList: Optional list of objects(string representation of BusinessObject) corresponding to class  which
    need to be checked for modification.
    """
    className: str = ''
    objectsList: List[str] = ()


@dataclass
class OwnershipChangeReplicaUpdateResponse(TcBaseObj):
    """
    It holds FMS ticket of log file and errors if any.
    
    :var logFmsTicket: The FMS ticket of log file which has status of operation either success or failure.
    :var serviceData: The service data
    """
    logFmsTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class ReplicaDeletionMasterUpdateResponse(TcBaseObj):
    """
    It holds the FMS ticket of log file which has status of an operation and errors if any.
    
    :var logFmsTicket: The FMS ticket of log file which has status of operation either success or failure.
    :var serviceData: The service data
    """
    logFmsTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class StubReplicationMasterUpdateResponse(TcBaseObj):
    """
    It holds FMS ticket to log file which has success or failure information for each input GSIdentity and errors if
    any.
    
    :var logFmsTicket: FMS ticket to log file
    :var serviceData: The service data
    """
    logFmsTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class SyncResponse(TcBaseObj):
    """
    It holds the objects that were modified since last export and errors if any.
    
    :var candidateObjectsList: A list of objects(string representation of BusinessObject) which were modified since
    last export or need synchronization.
    :var serviceData: The service data
    """
    candidateObjectsList: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class CheckSyncStateResponse(TcBaseObj):
    """
    It holds a list replica sync status for each input object, FMS ticket of log file and errors if any.
    
    :var replicaSyncStatusList: A list of GSIdentity and it's sync status
    :var logFmsTicket: The FMS ticket of log file which has status for each object with is either success or failed.
    
    :var serviceData: The service data
    """
    replicaSyncStatusList: List[GmsSyncStatus] = ()
    logFmsTicket: str = ''
    serviceData: ServiceData = None
