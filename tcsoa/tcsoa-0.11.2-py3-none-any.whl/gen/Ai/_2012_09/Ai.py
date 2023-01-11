from __future__ import annotations

from tcsoa.gen.BusinessObjects import RequestObject, AppInterface
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Ai._2006_03.Ai import StatusInfo
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindRequestsFilter(TcBaseObj):
    """
    structure that captures the filtering options for getting the Request Objects. This will include the AppInterface
    filter options too.
    
    :var aiQryParams: structure to capture the filter options on parent(s) ApplicationInterfaces of the RequestObject(s)
    :var requestState: vector  representing the requeststates to use for filtering. Currently, the only valid values
    are unique combinations of (case sensitive): Processing, Pending, Communicating, Completed, Rejected
    :var requestStatus: vector of strings representing the statuses on the request to search for. Currently, the valid
    values are a combination of (case sensitive): Normal,  Warning, Severe, Abort
    :var stateDescription: state description to use for searching for RequestObject.
    :var statusDescription: status message by which to filter for RequestObjects.
    :var customStrings: vector of strings that have the custom key and value pair to search on.
    :var requestType: the type of request - valid values:Publish, Sync. Empty vector if this filter option is not
    needed.
    """
    aiQryParams: ProjectFilter = None
    requestState: List[str] = ()
    requestStatus: List[str] = ()
    stateDescription: str = ''
    statusDescription: str = ''
    customStrings: StrToStrMap = None
    requestType: List[str] = ()


@dataclass
class FindRequestsResponse(TcBaseObj):
    """
    structure containing the response from findRequests method. partial failures are captured in the serviceData and
    found Requests are captured in RequestDetails.
    
    :var requests: list of found requests based on the input query.
    :var serviceData: Any partial errors are reported in this member.
    """
    requests: List[RequestDetail] = ()
    serviceData: ServiceData = None


@dataclass
class GetProjectsInfo2Response(TcBaseObj):
    """
    get the ProjectInfo structure for each of the specified ApplicationInterfaceObjects.
    
    :var infos: info about the ApplicationInterface objects
    :var serviceData: partial errors are returned in this structure.
    """
    infos: List[ProjectInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetRequestsInfo2Response(TcBaseObj):
    """
    get the details on the input RequestObject.
    
    :var details: details about the input RequestObjects. If there is an error getting info for any RequestObject, it
    will not be in this vector, but failure details will be in the serviceData.
    :var serviceData: serviceData to capture any partialErrors. client id used will be the position in the input vector.
    """
    details: List[RequestDetail] = ()
    serviceData: ServiceData = None


@dataclass
class ProjectFilter(TcBaseObj):
    """
    Structure to specify the filter when using getProjects  method.
    
    :var name: name of the AppliationInterface Object
    :var description: description of the ApplicationInterface Object
    :var releasedAfter: filtering by Date
    :var contextString: maps to the context string of AI object's Export TransferMode.
    :var targetSiteIds: valid site names to be used to search for ApplicationInterface objects.
    :var targetAppProjectId: if an application stamps a targetAppProject id using the setProjectsInfo method - they can
    use this for filtering.
    :var type: type of the ApplicationInterface Object. The type must be a valid type of AI Object.
    :var userId: userId to filter on (maps to owning user)
    :var groupName: filter on AI objects using groupName
    :var createdBefore: filtering by Date
    :var createdAfter: filtering by Date
    :var modifiedBefore: filtering by Date
    :var modifiedAfter: filtering by Date
    :var releasedBefore: filtering by Date
    """
    name: str = ''
    description: str = ''
    releasedAfter: datetime = None
    contextString: str = ''
    targetSiteIds: List[str] = ()
    targetAppProjectId: str = ''
    type: str = ''
    userId: str = ''
    groupName: str = ''
    createdBefore: datetime = None
    createdAfter: datetime = None
    modifiedBefore: datetime = None
    modifiedAfter: datetime = None
    releasedBefore: datetime = None


@dataclass
class ProjectInfo(TcBaseObj):
    """
    Structure to specify ApplicationInterface information.
    
    :var ai: The ApplicationInterfaceObject for which the info is relevant.
    :var targetAppProjectId: The projectId string recorded on the ApplicationInterface Object
    :var name: name of the AppliationInterface Object
    :var description: description of the ApplicationInterface Object
    :var targetSiteIds: The list of names of targetSiteIds to be set on the ApplicationInterface Object. Entries must
    be valid site names.
    """
    ai: AppInterface = None
    targetAppProjectId: str = ''
    name: str = ''
    description: str = ''
    targetSiteIds: List[str] = ()


@dataclass
class RequestDetail(TcBaseObj):
    """
    Structure representing the details of the RequestObject
    
    :var ro: the request object for which the details are being provided.
    :var name: name of the RequestObject
    :var description: description of the RequestObject
    :var stateDesc: description on the state of the RequestObject.
    :var status: the status fields of the RequestObject
    :var rscope: 2 values are possible:  0(whole)- no ExternalReference elements will be found in plmxml. Partial(1)
    then there will be ExternalReference elements in plmxml.
    :var rupdate: used to specify an incremental update. possible values are 0 (Full), 1 ( delta).
    :var kvPairs: key value pairs associated with the RequestObject. These would have been populated via the
    setRequestsInfo call.
    """
    ro: RequestObject = None
    name: str = ''
    description: str = ''
    stateDesc: str = ''
    status: StatusInfo = None
    rscope: int = 0
    rupdate: int = 0
    kvPairs: StrToStrMap = None


@dataclass
class RequestInfo(TcBaseObj):
    """
    structure representing gettable/settable information on a RequestObject by clients for a given RequestObject.
    
    :var ro: the object for which the data is being or retrieved.
    :var stateMessage: The string to set/get for the RequestObject's state_msg property.
    :var statusInfo: Structure to set the status and status_msg attributes of RequestObject. These typically are used
    to provide the TC user information about what happened in the relevant client application.
    :var kvPairs: key value pairs of strings to allow clients to set custom properties on the RequestObject. Limit of
    64 bytes on key and 256 bytes on value.
    """
    ro: RequestObject = None
    stateMessage: str = ''
    statusInfo: StatusInfo = None
    kvPairs: StrToStrMap = None


"""
string to string map.
"""
StrToStrMap = Dict[str, str]
