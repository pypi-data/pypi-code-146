from __future__ import annotations

from tcsoa.gen.BusinessObjects import RequestObject, AppInterface
from tcsoa.gen.Ai._2006_03.Ai import CommitFilesResponse, Configuration, GenerateStructureResponse, GenerateFullSyncRequestResponse, GetStructureReadTicketResponse, GetNextApprovedRequestResponse, RequestDetail, GetPropertiesOfObjectsResponse, CommitFileData, StateFilter, ProjectFilter, ObjectsExistResponse, GetStructureWriteTicketResponse, FileType, CommitStructureFileResponse, ProjectCreationData, GetFileWriteTicketsResponse, UpdateType, GetFileReadTicketsResponse, ProjectInfo, ApplicationRef, CreatePublishRequestResponse, StatusInfo, FileTicket
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def getProjectsInfo(cls, aiIds: List[AppInterface]) -> ServiceData:
        """
        Get details of the specified AI Objects.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getProjectsInfo',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'aiIds': aiIds},
            response_cls=ServiceData,
        )

    @classmethod
    def getPropertiesOfObjects(cls, appRefs: List[ApplicationRef], propertySetNames: List[str]) -> GetPropertiesOfObjectsResponse:
        """
        Get Properties of Teamcenter obects based on a propertyset created using the plmxml admin application.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getPropertiesOfObjects',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'appRefs': appRefs, 'propertySetNames': propertySetNames},
            response_cls=GetPropertiesOfObjectsResponse,
        )

    @classmethod
    def getRequestsForProject(cls, projectId: AppInterface, filter: StateFilter) -> ServiceData:
        """
        Given a Project(AI) object, get the RequestObjects based on the optional filter.
        default filter used: RequestType Sync and RequestState - pending.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getRequestsForProject',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'projectId': projectId, 'filter': filter},
            response_cls=ServiceData,
        )

    @classmethod
    def getRequestsInfo(cls, reqIds: List[RequestObject]) -> ServiceData:
        """
        Given a vector of RequestObjects, get details on those. This can be used if the
        RequestObject Ids are known. If not, GetProjectRequests can be used.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getRequestsInfo',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'reqIds': reqIds},
            response_cls=ServiceData,
        )

    @classmethod
    def getStructureReadTicket(cls, id: RequestObject, type: UpdateType) -> GetStructureReadTicketResponse:
        """
        Used to download the ticket for the plmxml file associated with the RequestObject.
        This ticket is then to be used with FCC client Proxy to download the file.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getStructureReadTicket',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id, 'type': type},
            response_cls=GetStructureReadTicketResponse,
        )

    @classmethod
    def getStructureWriteTicket(cls, originalFileName: str) -> GetStructureWriteTicketResponse:
        """
        Used to download the ticket for the plmxml file that will be uploaded by the client. This ticket
        is then to be used with FCC client Proxy to actually upload the file.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getStructureWriteTicket',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'originalFileName': originalFileName},
            response_cls=GetStructureWriteTicketResponse,
        )

    @classmethod
    def commitFiles(cls, reqObj: RequestObject, data: List[CommitFileData]) -> CommitFilesResponse:
        """
        After a call to getFileWriteTickets - this method is to be used to create TeamCenter file objects - referencing
        the files in the volume.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='commitFiles',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'reqObj': reqObj, 'data': data},
            response_cls=CommitFilesResponse,
        )

    @classmethod
    def commitStructureFile(cls, id: RequestObject, ticket: FileTicket, pUpdate: UpdateType) -> CommitStructureFileResponse:
        """
        This method is to be used to save a plmxml file after getting the write ticket using the
        GetStructureWriteTicket method.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='commitStructureFile',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id, 'ticket': ticket, 'pUpdate': pUpdate},
            response_cls=CommitStructureFileResponse,
        )

    @classmethod
    def objectsExist(cls, objIds: List[ApplicationRef]) -> ObjectsExistResponse:
        """
        Given 1 or more ApplicationRef objects - find the corresponding TeamCenter Object(s). Typically,
        the ApplicationRef is obtained from a plmxml file. The ApplicationRef for Teamcenter objects is
        (from a client point of view) - application='TcEng', label=teamcenter_uid, version=teamcenter_uid.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='objectsExist',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'objIds': objIds},
            response_cls=ObjectsExistResponse,
        )

    @classmethod
    def processPublishRequest(cls, id: RequestObject) -> ServiceData:
        """
        Process(import) the plmxml corresponding to the RequestObject
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='processPublishRequest',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id},
            response_cls=ServiceData,
        )

    @classmethod
    def processStructure(cls, transferModeName: str, plmxmlFileId: str, config: Configuration) -> ServiceData:
        """
        Import a plmxml for a previously uploaded plmxml via getStructureWriteTicket, fcc method to upload the file and
        commitStructureFile (with no associated RequestObject - non AI plmxml import)
        
        Note: 
        For importing plmxml that contains datasets or other attachments you need to use 'importObjectsFromPLMXML' from
        'globalmultisite.ImportExportService'.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='processStructure',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'transferModeName': transferModeName, 'plmxmlFileId': plmxmlFileId, 'config': config},
            response_cls=ServiceData,
        )

    @classmethod
    def setExchangeMessage(cls, id: RequestObject, stateMsg: str, info: StatusInfo) -> ServiceData:
        """
        Set any StatusInfo on the RequestObject and state description
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='setExchangeMessage',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id, 'stateMsg': stateMsg, 'info': info},
            response_cls=ServiceData,
        )

    @classmethod
    def setProjectsInfo(cls, projectIds: List[AppInterface], infos: List[ProjectInfo]) -> ServiceData:
        """
        Set details of the specified AI Objects from the supplied vector of ProjectInfo objects. You can only set
        targetAppProjectId, description and name fields.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='setProjectsInfo',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'projectIds': projectIds, 'infos': infos},
            response_cls=ServiceData,
        )

    @classmethod
    def startExchange(cls, id: RequestObject) -> ServiceData:
        """
        Set Communicating State on the RequestObject. To be called before uploading or downloading
        files to the RequestObject
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='startExchange',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id},
            response_cls=ServiceData,
        )

    @classmethod
    def createProjects(cls, projectDatas: List[ProjectCreationData]) -> ServiceData:
        """
        Create ApplicationInterface Objects in Teamcenter based on the input values
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='createProjects',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'projectDatas': projectDatas},
            response_cls=ServiceData,
        )

    @classmethod
    def createPublishRequest(cls, id: AppInterface, detail: RequestDetail, plmxmlFileName: str) -> CreatePublishRequestResponse:
        """
        Create a new RequestObject of type Publish on the specified AI Object.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='createPublishRequest',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id, 'detail': detail, 'plmxmlFileName': plmxmlFileName},
            response_cls=CreatePublishRequestResponse,
        )

    @classmethod
    def deleteProjects(cls, projectIds: List[AppInterface]) -> ServiceData:
        """
        Delete the specified AI Objects from the Database.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='deleteProjects',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'projectIds': projectIds},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteRequests(cls, requestIds: List[RequestObject]) -> ServiceData:
        """
        Given 1 or more requestObjects - delete them from the database
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='deleteRequests',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'requestIds': requestIds},
            response_cls=ServiceData,
        )

    @classmethod
    def endExchange(cls, id: RequestObject, stateMsg: str, info: StatusInfo) -> ServiceData:
        """
        Set Completed state on the Sync RequestObject or Pending state on a Publish RequestObject.
        StatusInfo and state description can be set by client
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='endExchange',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id, 'stateMsg': stateMsg, 'info': info},
            response_cls=ServiceData,
        )

    @classmethod
    def generateFullSyncRequest(cls, id: AppInterface, name: str, description: str, baseRefs: List[ApplicationRef]) -> GenerateFullSyncRequestResponse:
        """
        Generate a Sync Request on a new AI or Existing AI object.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='generateFullSyncRequest',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'id': id, 'name': name, 'description': description, 'baseRefs': baseRefs},
            response_cls=GenerateFullSyncRequestResponse,
        )

    @classmethod
    def generateStructure(cls, idsToProcess: List[ApplicationRef], transferModeName: str, config: Configuration, serverMode: int) -> GenerateStructureResponse:
        """
        Generate a plmxml for the given set of ids.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='generateStructure',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'idsToProcess': idsToProcess, 'transferModeName': transferModeName, 'config': config, 'serverMode': serverMode},
            response_cls=GenerateStructureResponse,
        )

    @classmethod
    def getFileReadTickets(cls, fileIds: List[ApplicationRef]) -> GetFileReadTicketsResponse:
        """
        Used to download the tickets for the files referenced by the plmxml file previously exported from Teamcenter.
        These tickets are then to be used with FCC client Proxy to actually download the files.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getFileReadTickets',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'fileIds': fileIds},
            response_cls=GetFileReadTicketsResponse,
        )

    @classmethod
    def getFileWriteTickets(cls, originalFileNames: List[str], fileTypes: List[FileType]) -> GetFileWriteTicketsResponse:
        """
        Used to download the tickets for the files referenced by the plmxml file created by a client application.
        These tickets are then to be used with FCC client Proxy to actually upload(commit) the files.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getFileWriteTickets',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'originalFileNames': originalFileNames, 'fileTypes': fileTypes},
            response_cls=GetFileWriteTicketsResponse,
        )

    @classmethod
    def getNextApprovedRequest(cls, projectId: AppInterface, curReq: RequestObject) -> GetNextApprovedRequestResponse:
        """
        Given a  RequestObject get the next approved pending sync RequestObject
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getNextApprovedRequest',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'projectId': projectId, 'curReq': curReq},
            response_cls=GetNextApprovedRequestResponse,
        )

    @classmethod
    def getProjects(cls, filter: ProjectFilter) -> ServiceData:
        """
        Get a list of projects that are available on this database based on the filter specified.
        Suggest atleast filtering based on type of AppInterface
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='getProjects',
            library='Ai',
            service_date='2006_03',
            service_name='Ai',
            params={'filter': filter},
            response_cls=ServiceData,
        )
