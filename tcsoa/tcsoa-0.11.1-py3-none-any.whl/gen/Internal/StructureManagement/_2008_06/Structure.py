from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import WorkspaceObject, PSBOMViewRevision
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindHighestFindNumInExpandInput(TcBaseObj):
    """
    Input structure for findHighestFindNumberInExpand operation
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var bvr: bvr for which the highest sequence number is expected to be returned
    :var occType: (optional) The name of the occurrence type. If the occurrence type is set here, 
    the highest sequence number is only estimated from expanded BOMLines with specific occurrence type. If the
    occurrence type is an empty string, all expanded BOMLines are used to get the highest sequence number.
    """
    clientId: str = ''
    bvr: PSBOMViewRevision = None
    occType: str = ''


@dataclass
class FindHighestFindNumberInExpandResponse(TcBaseObj):
    """
    Return structure for findHighestFindNumberInExpand operation
    
    :var incrementNumber: stride length between find numbers
    :var serviceData: Standard ServiceData member
    :var output: vec of output structures
    """
    incrementNumber: int = 0
    serviceData: ServiceData = None
    output: List[FindHighestFindNumberOutputStruct] = ()


@dataclass
class FindHighestFindNumberOutputStruct(TcBaseObj):
    """
    Return structure for findHighestFindNumberOutputStruct
    
    :var highestFindNumber: The highest find number
    :var clientId: client id
    """
    highestFindNumber: int = 0
    clientId: str = ''


@dataclass
class CopyRecursivelyResponse(TcBaseObj):
    """
    This structure provides a set of input values for the re-sequence action.
    
    :var createdIcRevs: any newly created IncrementalChange revisions
    :var createdFutureIcRevs: any newly created future IC revisions.
    :var serviceData: the newly created object will be in here
    """
    createdIcRevs: List[WorkspaceObject] = ()
    createdFutureIcRevs: List[WorkspaceObject] = ()
    serviceData: ServiceData = None
