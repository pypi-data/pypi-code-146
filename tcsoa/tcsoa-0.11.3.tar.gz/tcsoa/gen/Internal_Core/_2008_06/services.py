from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile
from tcsoa.gen.Internal.Core._2008_06.FileManagement import GetRegularFileWriteTicketsInput, CommitUploadedRegularFilesInput, GetFileTransferTicketsResponse, CommitUploadedRegularFilesResponse, GetRegularFileWriteTicketsResponse, WriteTicketsInput, UpdateImanFileCommitsResponse, FileTicketsResponse
from tcsoa.gen.Internal.Core._2008_06.DispatcherManagement import UpdateDispatcherRequestArgs, CreateDatasetOfVersionArgs, UpdateDispatcherRequestResponse, QueryDispatcherRequestsResponse, CreateDatasetOfVersionResponse, InsertDatasetVersionArgs, InsertDatasetVersionResponse, QueryDispatcherRequestsArgs
from tcsoa.gen.Internal.Core._2008_06.DataManagement import MultiRelMultiLevelExpandInput, CreateRelationsResponse, Relationship, MultiRelationMultiLevelExpandResponse
from typing import List
from tcsoa.gen.Core._2008_06.DataManagement import SaveAsNewItemInfo, ReviseResponse2, ReviseInfo, SaveAsNewItemResponse2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class FileManagementService(TcService):

    @classmethod
    def getRegularFileTicketsForUpload(cls, inputs: List[GetRegularFileWriteTicketsInput]) -> GetRegularFileWriteTicketsResponse:
        """
        This operation obtains File Management System (FMS) write tickets for a set of supplied ImanFile objects.  The
        supplied tickets are required by the File Management System (FMS) to upload files to a Teamcenter volume.  The
        'imanFiles' input parameter contains the list of ImanFile objects to be transferred.
        These files are typically standalone files which are not attached to a Dataset as named reference.   No Dataset
        or named reference relation is required or created during this operation.  This operation is intended for use
        only by the Dispatcher module to store input and log files in Teamcenter volumes.
        This operation supports the upload (addition) of files to a Teamcenter volume.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        
        Use cases:
        Two major use cases are supported:
        - Attach translation input files to a Dispatcher request during request creation.
        
        
        In this use case, a Dispatcher Client uploads the input files to a Teamcenter volume, so that the ImanFile
        representing the data file can be attached to a Dispatcher request.
        - Attach log files to Dispatcher request during request update.
        
        
        In this use case, the Dispatcher Client uploads the log file of a completed translation task to a Teamcenter
        volume, and attaches a reference to the ImanFile representing the log file to the Dispatcher request for post
        mortem analysis.
        """
        return cls.execute_soa_method(
            method_name='getRegularFileTicketsForUpload',
            library='Internal-Core',
            service_date='2008_06',
            service_name='FileManagement',
            params={'inputs': inputs},
            response_cls=GetRegularFileWriteTicketsResponse,
        )

    @classmethod
    def getWriteTickets(cls, inputs: List[WriteTicketsInput]) -> FileTicketsResponse:
        """
        This operation obtains File Management System (FMS) write tickets  for a set of supplied files that will be
        uploaded to Teamcenter.  Dataset creation is not required prior to requesting the tickets. The write tickets
        are used to transfer files from a local storage location to the Teamcenter volume.
        This operation is used in conjunction with other 'FileManagementService' operations , Visualization operations
        for creating the datamodel , committing the uploaded file to the Teamcenter database and associating the
        uploaded data files in the Teamcenter volume with the Dataset named references and the File Management System
        (FMS).  Please consult the documentation for each of these available operations for details on the
        requirements, usage, and environments in which they should be used.
        This operation supports the upload (addition) of files as ImanFile objectsto a Teamcenter volume.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        
        Use cases:
        This operation supports file uploads from the Teamcenter Visualization module.
        """
        return cls.execute_soa_method(
            method_name='getWriteTickets',
            library='Internal-Core',
            service_date='2008_06',
            service_name='FileManagement',
            params={'inputs': inputs},
            response_cls=FileTicketsResponse,
        )

    @classmethod
    def commitRegularFiles(cls, inputs: List[CommitUploadedRegularFilesInput]) -> CommitUploadedRegularFilesResponse:
        """
        This operation is invoked after successfully uploading a file to a Teamcenter volume.
        These files are typically standalone files which are not attached to a Dataset as named reference.   No Dataset
        or named reference relation is required or created during this operation.  This operation is intended for use
        only by the Dispatcher module to store input and log files in Teamcenter volumes.
        This operation supports the upload (addition) of files to a Teamcenter volume.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        
        Use cases:
        Two major use cases are supported:
        - Attach translation input files to a Dispatcher request during request creation.
        
        
        In this use case, a Dispatcher Client uploads the input files to a Teamcenter volume, so that the ImanFile
        representing the data file can be attached to a Dispatcher request.
        - Attach log files to Dispatcher request during request update.
        
        
        In this use case, the Dispatcher Client uploads the log file of a completed translation task to a Teamcenter
        volume, and attaches a reference to the ImanFile representing the log file to the Dispatcher request for
        postmortem analysis.
        """
        return cls.execute_soa_method(
            method_name='commitRegularFiles',
            library='Internal-Core',
            service_date='2008_06',
            service_name='FileManagement',
            params={'inputs': inputs},
            response_cls=CommitUploadedRegularFilesResponse,
        )

    @classmethod
    def updateImanFileCommits(cls, cleanupInfo: List[str]) -> UpdateImanFileCommitsResponse:
        """
        This operation recommits files that have been successfully moved to a new volume by the File Management System
        (FMS) StoreAndForward feature.  This operation is intended for use only by the 'DatabaseOperations'() method of
        an FMSTransferTool transfer task running in a Dispatcher Client context.
        The File Management System (FMS) StoreAndForward feature redirects uploads to a temporary volume that is close
        to the uploading user, called a Default Local Volume.  The system then transfers the file to its final home in
        a Default Volume in a background FMSTransferTool process executed on a Dispatcher Module.
        The first step of the background operation is to transfer the file(s) from the Default Local Volume to the
        Default Volume.  After the file transfer completes, the DatabaseOperations step of the FMSFileTransferTool
        dispatcher task invokes this operation to commit the new volumes of each file to the Teamcenter database.
        This operation also returns the write tickets necessary to remove the file from the Default Local Volume after
        any outstanding FMS tickets expire.  This information is persisted in a second dispatcher task, which also
        executes in a background operation on a Dispatcher Module.
        The FMSTransferTool TaskPrep method invokes the 'getFileTransferTickets'() operation to obtain the FMS tickets
        necessary to transfer the files between the two volumes.  The tickets are written to a temporary file stored in
        the Dispatcher staging directory, and processed by the FMSTransferTool.  The FMSTransferTool manages the file
        transfers, and writes the results to an output file.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        
        Use cases:
        This operation supports the File Management System (FMS) StoreAndForward feature.
        """
        return cls.execute_soa_method(
            method_name='updateImanFileCommits',
            library='Internal-Core',
            service_date='2008_06',
            service_name='FileManagement',
            params={'cleanupInfo': cleanupInfo},
            response_cls=UpdateImanFileCommitsResponse,
        )

    @classmethod
    def getFileTransferTickets(cls, imanFiles: List[ImanFile]) -> GetFileTransferTicketsResponse:
        """
        This operation obtains File Management System (FMS) transfer tickets for a set of supplied ImanFile objects. 
        The supplied tickets are used to transfer files from a temporary volume to a final destination volume as a part
        of the FMS StoreAndForward feature.  The imanFiles input parameter contains the list of ImanFile objects to be
        transferred.  This operation is intended for use only by the TaskPrep method of an FMSTransferTool transfer
        task running in a Dispatcher Client context.
        The File Management System (FMS) StoreAndForward feature redirects uploads to a temporary volume that is close
        to the uploading user, called a Default Local Volume.  The system then transfers the file to its final home in
        a Default Volume in a background FMSTransferTool  process executed on a Dispatcher Module.
        The first step of the background operation is to transfer the file(s) from the Default Local Volume to the
        Default Volume.  This operation is invoked by the FMSTransferTool TaskPrep() method to obtain the FMS tickets
        necessary to transfer the files between the two volumes.  The tickets are written to a temporary file stored in
        the Dispatcher staging directory, and processed by the FMSTransferTool.  The FMSTransferTool manages the file
        transfers, and writes the results to an output file.
        After the files are successfully transferred from the Default Local Volume to the Default Volume, the
        'DatabaseOperations'() method of the FMSFileTransferTool dispatcher task invokes the
        'FileManagementService::updateImanFileCommits' operation to update the Teamcenter database with the new file
        location.
        This operation is unpublished.  It is supported only for internal Siemens PLM purposes.  Customers should not
        invoke this operation.
        
        Use cases:
        This operation supports the File Management System (FMS) StoreAndForward feature.
        """
        return cls.execute_soa_method(
            method_name='getFileTransferTickets',
            library='Internal-Core',
            service_date='2008_06',
            service_name='FileManagement',
            params={'imanFiles': imanFiles},
            response_cls=GetFileTransferTicketsResponse,
        )


class DispatcherManagementService(TcService):

    @classmethod
    def insertDatasetVersion(cls, inputs: List[InsertDatasetVersionArgs]) -> InsertDatasetVersionResponse:
        """
        Insert a Datasets at a specific version.
        
        Use cases:
        When creating Datasets in the system, sometimes the versions are to be specified.  This is an important detail
        to maintain, especially during migration of external data into Teamcenter from another system.  This operation
        provides the ability to insert a Dataset at a particular version within the system which are different than the
        standard behavior provided by the Data Management Services.
        """
        return cls.execute_soa_method(
            method_name='insertDatasetVersion',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DispatcherManagement',
            params={'inputs': inputs},
            response_cls=InsertDatasetVersionResponse,
        )

    @classmethod
    def queryDispatcherRequests(cls, inputs: List[QueryDispatcherRequestsArgs]) -> QueryDispatcherRequestsResponse:
        """
        Search for any DispatcherRequests matching the associated values within Teamcenter.
        
        Use cases:
        Instead of using saved queries to find DispatcherRequests in the system, you would use this method which is
        specific to finding DispatcherRequests.
        """
        return cls.execute_soa_method(
            method_name='queryDispatcherRequests',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DispatcherManagement',
            params={'inputs': inputs},
            response_cls=QueryDispatcherRequestsResponse,
        )

    @classmethod
    def updateDispatcherRequests(cls, inputs: List[UpdateDispatcherRequestArgs]) -> UpdateDispatcherRequestResponse:
        """
        Update DispatcherRequest objects within the Teamcenter database.
        This operation allows updating of the following DispatcherRequest properties:
        - State
        - KeyValue Args
        - Data Files
        
        
        
        Use cases:
        When the need arises to update a DispatcherRequest object, this method provides that ability to update a few
        select properties of the DispatcherRequest.
        """
        return cls.execute_soa_method(
            method_name='updateDispatcherRequests',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DispatcherManagement',
            params={'inputs': inputs},
            response_cls=UpdateDispatcherRequestResponse,
        )

    @classmethod
    def createDatasetOfVersion(cls, inputs: List[CreateDatasetOfVersionArgs]) -> CreateDatasetOfVersionResponse:
        """
        Creates a new Dataset  with a particular version. This is similar to the Core DataManagement createDataset
        operation with the exception that this operation takes a specific version and creates the Dataset at that
        version even if it is the first instance of that Dataset.
        
        Use cases:
        If a Dataset does not already exist within Teamcenter and the applications needs to create one but have it
        begin at a certain version, this operation will provide that ability.  This is a key factor when migrating data
        from other systems where the versions need to stay in sync for validation purposes.
        """
        return cls.execute_soa_method(
            method_name='createDatasetOfVersion',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DispatcherManagement',
            params={'inputs': inputs},
            response_cls=CreateDatasetOfVersionResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def multiRelationMultiLevelExpand(cls, input: MultiRelMultiLevelExpandInput) -> MultiRelationMultiLevelExpandResponse:
        """
        Can be used to expand one or more relations over an entire structure. It recursively expands the relations
        again on the secondary objects of the expand results, until no more relations are found. Branches that lead
        into directed cycles are detected and not followed. So the method will not run into endless loops if the
        structure contains directed cycles.
        """
        return cls.execute_soa_method(
            method_name='multiRelationMultiLevelExpand',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=MultiRelationMultiLevelExpandResponse,
        )

    @classmethod
    def reviseObject(cls, info: List[ReviseInfo], deepCopyRequired: bool) -> ReviseResponse2:
        """
        This operation provides ability to revise all the existing ItemRevision objects given in the input and carry
        forward its relations based on the 'deepCopyRequired' flag. When applying deep copy rules, if user overridden
        deep copy information is provided in the input, then old relations are propagated to the new ItemRevision based
        on the input. If no deep copy information is provided in the input, the deep rules in the database will apply.
        If user provides new property values for the master form in the input, these will be copied to the newly
        created ItemRevision's master form.
        """
        return cls.execute_soa_method(
            method_name='reviseObject',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'info': info, 'deepCopyRequired': deepCopyRequired},
            response_cls=ReviseResponse2,
        )

    @classmethod
    def saveAsNewItemObject(cls, info: List[SaveAsNewItemInfo], deepCopyRequired: bool) -> SaveAsNewItemResponse2:
        """
        This operation provides ability to create new Item objects based on existing ItemRevision objects in the input
        info. It optionally carries forward ItemRevision relations based on the 'deepCopyRequired' flag.  When applying
        deep copy rules, if user overridden deep copy information is provided in the input, then old ItemRevision
        relations are propagated to the new ItemRevision based on the input. If no deep copy rule information is
        provided in the input, the deep rules in the database will be applied. If user provides new property values for
        the Item and ItemRevision master forms in the input, then these will be copied to the master forms of the newly
        created Item and ItemRevision.
        
        Use cases:
        Use this operation to create one or more new Item objects from one or more existing ItemRevision.  The new Item
        and first ItemRevision will be based on the input ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='saveAsNewItemObject',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'info': info, 'deepCopyRequired': deepCopyRequired},
            response_cls=SaveAsNewItemResponse2,
        )

    @classmethod
    def setDefaultProjectForProjectMembers(cls, project: BusinessObject, projectMembers: List[BusinessObject]) -> ServiceData:
        """
        This operation will set the given TC_Project object as user's default project in user context by setting it in
        TC_UserContext object. If the given object is invalid then this operation will return an error with code 7007:
        Invalid tag in the standard ServiceData .
        """
        return cls.execute_soa_method(
            method_name='setDefaultProjectForProjectMembers',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'project': project, 'projectMembers': projectMembers},
            response_cls=ServiceData,
        )

    @classmethod
    def createCachedRelations(cls, input: List[Relationship]) -> CreateRelationsResponse:
        """
        Creates the specified relation between the input objects (primary and secondary objects) for each input
        structure. The relation object created using this service will be cached  in the runtime memory.It also
        initializes all the properties on the relation which are not marked as mandatory for its creation. The service
        operation createRelations, on the other hand does not initialize any property on the new relation it created.
        
        Use cases:
        Use Case 1: Create a relation based on the Generic Relationship Management (GRM) rule definition with property
        on the relation set to a value.
        
        Custom Items, namely, Cus03_tem1 and Cus03_Item2 are related to each other through a relation busuness object
        Cus03_Relation. Cus03_Relation has two properties cus03_relationUsage and cus03_relationUsageDescription. The
        property cus03_relationUsage is a mandatory property at the time of creation of the relation while the property
        cus03_relaionUsageDescription is a property whose initial value cannot be null. Following steps are done by the
        'createCachedRelations' operation. 
        
        - Relation business object is created
        - All properties are initialized to the initial value which is specified in the InitialValue property constant
        for the given property.
        
        """
        return cls.execute_soa_method(
            method_name='createCachedRelations',
            library='Internal-Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateRelationsResponse,
        )


class SessionService(TcService):

    @classmethod
    def cancelOperation(cls, id: str) -> bool:
        """
        Cancel a service request. Currently only 'executeSavedQuery' supports the ability to interrupt and cancel the
        operation.
        """
        return cls.execute_soa_method(
            method_name='cancelOperation',
            library='Internal-Core',
            service_date='2008_06',
            service_name='Session',
            params={'id': id},
            response_cls=bool,
        )
