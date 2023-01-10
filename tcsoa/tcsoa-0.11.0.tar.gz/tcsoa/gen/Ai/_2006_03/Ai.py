from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileTicket(TcBaseObj):
    """
    FileTicket details
    
    :var ticket: the FMS ticket
    :var originalFileName: name of the file that is displayed in TC UI
    """
    ticket: str = ''
    originalFileName: str = ''


@dataclass
class ApplicationRef(TcBaseObj):
    """
    Structure representing application neutral identifier
    
    :var application: The application where these fields can be resolved. For example - it is Teamcenter for TC.
    :var label: The identifier for the object.
    :var version: The optional version string.
    """
    application: str = ''
    label: str = ''
    version: str = ''


@dataclass
class GenerateFullSyncRequestResponse(TcBaseObj):
    """
    Used to generate the plmxml for a sync request.
    
    :var ticket: ticket
    :var data: data
    """
    ticket: FileTicket = None
    data: ServiceData = None


@dataclass
class GenerateStructureResponse(TcBaseObj):
    """
    generatestructure returns the transient file ticket on success.
    
    :var ticket: ticket
    :var data: data
    """
    ticket: str = ''
    data: ServiceData = None


@dataclass
class GetFileReadTicketsResponse(TcBaseObj):
    """
    tickets to download files referenced by plmxml.
    
    :var tickets: tickets
    :var data: data
    """
    tickets: List[FileTicket] = ()
    data: ServiceData = None


@dataclass
class GetFileWriteTicketsResponse(TcBaseObj):
    """
    Tickets to upload files referenced by plmxml.
    
    :var tickets: tickets
    :var data: data
    """
    tickets: List[str] = ()
    data: ServiceData = None


@dataclass
class GetNextApprovedRequestResponse(TcBaseObj):
    """
    get next approved request. Currently not used.
    
    :var ticket: ticket
    :var data: data
    """
    ticket: FileTicket = None
    data: ServiceData = None


@dataclass
class GetPropertiesOfObjectsResponse(TcBaseObj):
    """
    GetPropertiesOfObjectsResponse struct
    
    :var nameValues: nameValues
    :var data: data
    """
    nameValues: StrVStrMap = None
    data: ServiceData = None


@dataclass
class GetStructureReadTicketResponse(TcBaseObj):
    """
    response of getStructureReadTicket - returns the plmxml file ticket.
    
    :var ticket: ticket
    :var data: data
    """
    ticket: FileTicket = None
    data: ServiceData = None


@dataclass
class GetStructureWriteTicketResponse(TcBaseObj):
    """
    response of getStructureWriteTicket - returns the ticket to be used for uploading a plmxml file.
    
    :var ticket: ticket
    :var data: data
    """
    ticket: str = ''
    data: ServiceData = None


@dataclass
class ObjectsExistResponse(TcBaseObj):
    """
    response of ObjectsExist method
    
    :var bExist: does the object exist in Teamcenter or not.
    :var ids: All the ApplicationRef registered for the Teamcenter object
    :var data: used to report any partial failures.
    """
    bExist: List[bool] = ()
    ids: List[ApplicationRef] = ()
    data: ServiceData = None


@dataclass
class ProjectCreationData(TcBaseObj):
    """
    Project(AI) creation method data
    
    :var type: Type of the Application Interface object to be created.
    :var name: Name of the AI object to be created.
    :var description: Description of the AI object to be created.
    :var targetApplicationId: The application id to be set on the AI object.
    """
    type: str = ''
    name: str = ''
    description: str = ''
    targetApplicationId: str = ''


@dataclass
class ProjectFilter(TcBaseObj):
    """
    Structure to specify the filter when using GetProjects method.
    
    :var projectType: ProjectType enum. Set it to ProjectType_Any if not needed.
    :var name: name of the AppliationInterface Object
    :var releasedBefore: filtering by Date
    :var releasedAfter: filtering by Date
    :var applicationId: maps to the Export TransferMode's (of the AI) context string
    :var siteId: description of the ApplicationInterface Object
    :var targetAppProjectId: used only if projectType==ProjectType_Existing
    :var description: description of the ApplicationInterface Object
    :var type: type of the ApplicationInterface Object. The type must be a valid type of AI Object.
    :var userId: userId to filter on
    :var groupName: filter on AI objects using groupName
    :var createdBefore: filtering by Date
    :var createdAfter: filtering by Date
    :var modifiedBefore: filtering by Date
    :var modifiedAfter: filtering by Date
    """
    projectType: ProjectType = None
    name: str = ''
    releasedBefore: datetime = None
    releasedAfter: datetime = None
    applicationId: str = ''
    siteId: str = ''
    targetAppProjectId: str = ''
    description: str = ''
    type: str = ''
    userId: str = ''
    groupName: str = ''
    createdBefore: datetime = None
    createdAfter: datetime = None
    modifiedBefore: datetime = None
    modifiedAfter: datetime = None


@dataclass
class ProjectInfo(TcBaseObj):
    """
    Structure to specify ApplicationInterface information.
    
    :var targetAppProjectId: The projectId string recorded on the ApplicationInterface Object
    :var name: name of the AppliationInterface Object
    :var description: description of the ApplicationInterface Object
    """
    targetAppProjectId: str = ''
    name: str = ''
    description: str = ''


@dataclass
class RequestDetail(TcBaseObj):
    """
    Structure representing the details of the RequestObject
    
    :var name: name of the RequestObject
    :var description: description of the RequestObject
    :var stateDesc: description on the state of the RequestObject.
    :var status: the status fields of the RequestObject
    :var scope: RequestScope_Whole - no ExternalReference elements will be found in plmxml. If Partial then there will
    be ExternalReference elements in plmxml.
    :var update: used to specify an incremental update.
    """
    name: str = ''
    description: str = ''
    stateDesc: str = ''
    status: StatusInfo = None
    scope: RequestScope = None
    update: UpdateType = None


@dataclass
class StateFilter(TcBaseObj):
    """
    Structure to filter RequestObject
    
    :var states: vector of RequestState enums
    :var types: vector of RequestType enums
    """
    states: List[RequestState] = ()
    types: List[RequestType] = ()


@dataclass
class StatusInfo(TcBaseObj):
    """
    Structure representing the status fields of the RequestObject
    
    :var status: RequestStatus enum RequestStatus_Normal etc.
    :var description: status message of the Request.
    """
    status: RequestStatus = None
    description: str = ''


@dataclass
class CommitFileData(TcBaseObj):
    """
    commitFileData structure to be used when commiting files to teamcenter.
    
    :var ticket: the write ticket returned from Teamcenter from a prior call to GetWriteFileTickets.
    :var id: If used with AI object, this represents the id of the RequestObject.
    :var filename: filename as specified, when getting the write ticket.
    """
    ticket: str = ''
    id: ApplicationRef = None
    filename: str = ''


@dataclass
class CommitFilesResponse(TcBaseObj):
    """
    commit files response.
    
    :var failedCommits: failedCommits
    :var data: data
    """
    failedCommits: List[CommitFileData] = ()
    data: ServiceData = None


@dataclass
class CommitStructureFileResponse(TcBaseObj):
    """
    returns the fileIds if the saved plmxml file.
    
    :var fileId: fileId
    :var data: data
    """
    fileId: str = ''
    data: ServiceData = None


@dataclass
class Configuration(TcBaseObj):
    """
    Configuration structure.
    
    :var id: Tag of ConfigurationContext or StructureContext or RevRule or VariantRule or storedOptionSetId,or
    TransferMode.
    :var rulename: if id is NULLTAG, then used to specify the revisionrule by name.
    :var useDefaultRevisionRule: if true - the Teamcenter preferences are used to pick up the rev rule. Overrides the
    above 2 members if true.
    """
    id: BusinessObject = None
    rulename: str = ''
    useDefaultRevisionRule: bool = False


@dataclass
class CreatePublishRequestResponse(TcBaseObj):
    """
    response of the createPublishRequest method.
    
    :var ticket: ticket
    :var data: data
    """
    ticket: FileTicket = None
    data: ServiceData = None


class FileType(Enum):
    """
    Type of file being uploaded to Teamcenter.
    """
    Binary = 'FileType_Binary'
    Text = 'FileType_Text'


class ProjectType(Enum):
    """
    Filter on whether the project_id is set on the ApplicationInterface object or not
    """
    New = 'ProjectType_New'
    Existing = 'ProjectType_Existing'
    Any = 'ProjectType_Any'


class RequestScope(Enum):
    """
    RequestScope
    """
    Whole = 'RequestScope_Whole'
    Partial = 'RequestScope_Partial'
    Any = 'RequestScope_Any'


class RequestState(Enum):
    """
    State of the Request Object
    """
    New = 'RequestState_New'
    Processing = 'RequestState_Processing'
    Pending = 'RequestState_Pending'
    Communicating = 'RequestState_Communicating'
    Completed = 'RequestState_Completed'
    Rejected = 'RequestState_Rejected'
    Any = 'RequestState_Any'


class RequestStatus(Enum):
    """
    Status of the Request Object. TC or application can set these depending on which party is doing the authoring.
    """
    Normal = 'RequestStatus_Normal'
    Warning = 'RequestStatus_Warning'
    Severe = 'RequestStatus_Severe'
    Abort = 'RequestStatus_Abort'
    Any = 'RequestStatus_Any'


class RequestType(Enum):
    """
    Type of the Request Object
    """
    Publish = 'RequestType_Publish'
    Sync = 'RequestTypeSync'
    Any = 'RequestType_Any'
    Notify = 'RequestType_Notify'


class UpdateType(Enum):
    """
    Request update type
    """
    Full = 'UpdateType_Full'
    Delta = 'UpdateType_Delta'
    Any = 'UpdateType_Any'


"""
StrVStrMap
"""
StrVStrMap = Dict[str, List[str]]
