from __future__ import annotations

from tcsoa.gen.Internal.Visualization._2008_06.StructureManagement import AreRecipesMergableResponse, ExpandPSFromOccurrenceListPref, ExpandPSFromOccurrenceListResponse, AreRecipesMergableInfo, CreateVisSCsFromBOMsResponse, CreateBOMsFromRecipesResponse, ExpandPSFromOccurrenceListInfo, CreateVisSCsFromBOMsInfo, CreateBOMsFromRecipesInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Visualization._2008_06.DataManagement import UpdateTwoDSnapshotInput, SaveSessionResponse, MarkupInput, UserAgentDataInfo, SessionModelUpdateResponse, IdInfo, UpdateTwoDSnapshotResponse, SessionInfo, SessionModelResponse, MarkupResponse, SessionModelInput, VVITicketsResponse, UpdateSesssionModel, CreateTwoDSnapshotResponse, MarkupUpdateInput, TwoDSnapshotInput, GetLatestFileReadTicketsResponse, UpdateSessionModelWithSessionInput, ServerInfo, MarkupUpdateResponse, GetLatestFileReadTicketsInfo, MetaDataStampTicketsResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def saveSession(cls, inputs: List[UpdateSessionModelWithSessionInput]) -> SaveSessionResponse:
        """
        This operation is responsible for committing the session file (of extension .vf) to the Vis_Session Dataset.
        This is done after the Vis_Session Dataset is created via 'createSessionModel' visualization operation or
        updated via the 'updateSessionModel' visualization operation (See Dependency section).  Creating or updating of
        the Vis_Session Dataset involves committing miscellaneous files like markups, images, other dependent files
        etc. and necessary relations to the Teamcenter objects as per the data model. The existence of all the relevant
        Teamcenter managed objects referenced by the session are recorded in the Teamcenter visualization session file
        and committed to the Vis_Session Dataset via 'saveSession' operation. Associated Dataset and IMANFile objects
        are then accessible to other authorized clients throughout the PLM system.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        
        Use cases:
        The mechanism for a client application to save session contains several steps.
        
        1.    Client application invokes the 'FileManagementService::getWriteTickets' operation to obtain an FMS write
        ticket for each file / IMANFile object that will be stored in the markup Dataset. 
        
        2.    Use a FMS operation to upload the files to the PLM volume (see the Dependencies section below).  The
        client application is responsible for making sure that the FMS operation used to upload the files indicates
        that the file uploads were successful. If a file upload were to fail, then the file should not be committed. 
        This should effectively prevent the construction of database infrastructure referencing files not present in
        the volume.  Check the documentation for each operation to determine how to react to upload failures.  Some
        upload operations are defined in such a way that a single result code is returned to the caller, or a single
        exception thrown, to indicate that the bulk file upload was entirely unsuccessful.  These operations typically
        roll back all the successfully uploaded files before returning to the caller.  Some operations may accept a
        flag indicating whether uploads should continue when an error is encountered.  Other operations return a
        separate result code for each file, indicating which files were successfully uploaded to a PLM volume and which
        uploads failed.
        
        It is the responsibility of the client application to either commit or rollback all successfully uploaded
        files.  Files that failed to upload need not be rolled back.
        
        Client responsibilities if upload of files to the volume fails:
        a.    Client applications must not invoke the 'saveSession' visualization operation on files that did not
        successfully upload to the PLM volume.  This causes file access errors downstream, when clients attempt to
        reference (or download) the file data, which will be missing from the PLM volume.
        b.    In the event of a partial upload success (some files uploaded successfully, but others did not), it is
        the responsibility of the client application to determine whether it is acceptable in context to commit the
        successfully uploaded files to the PLM system.
        - If not, then there is a companion FMS operation to roll back the successfully uploaded files (see
        Dependencies section).  The rollback method removes the files from the PLM volume.
        - If so, then it is the responsibility of the client application to avoid including information corresponding
        to the files that did not successfully upload to the PLM volume in the input list passed to the 'saveSession'
        visualization operation.
        
        
        
        3.    The client application then invokes the 'createSessionModel' or 'updateSessionModel' visualization
        operations on the successfully uploaded files. 
        This step creates or updates visualization supported session Dataset of types Vis_Session and commits the
        uploaded files to the Dataset.  In addition, these operations also associate the session Dataset to input
        Teamcenter objects with relevant relations as per the data model. Associated Dataset and IMANFile objects are
        then accessible to other authorized clients through the PLM system. If there are any failures during this
        operation, the client is responsible for rolling back the associated file from the volume through the FMS
        operation.  Check the documentation for each API to determine how to react to cleanup activity.
        
        Note:  In cases where the session is created against BOMView or BOMViewRevision or Teamcenter runtime objects
        like BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner, it is the responsibility
        of the client to create VisStructureContext object and provide VisStructureContext as an input to
        'createSessionModel' or 'updateSessionModel' operation.
        
        4.    After creating or updating the Vis_Session Dataset via 'createSessionModel' or 'updateSessionModel'
        respectively, the information of all the relevant Teamcenter managed objects in the session is noted in the
        session file (.vf). An FMS write ticket is then obtained for the session file and uploaded via FMS operation to
        Teamcenter volume.
        
        5.    Use 'saveSession' visualization operation to commit the session file to the Vis_Session Dataset.
        
        NOTE: It is the responsibility of the client to do cleanup as appropriate according to failures types.
        
        This operation is used in conjunction with other 'FileManagementService' service operations, 'Visualization'
        service operations and the FMS.  Please consult the documentation for each of these available operations for
        details on the requirements, usage, and environments in which they should be used.
        
        These dependencies include:
        
        1.    FMS operation for obtaining an FMS write ticket.
        
        'FileManagementService::getWriteTickets'    This operation obtains FMS write tickets for IMANFile objects.
        
        2.    FMS operations for uploading and rolling back the files to/from the PLM volume.
        
        Library                        Binding
        
        FCCClientProxy.lib                C
        
        'FCC_UploadFileToPLM'        Uploads a file to a PLM volume.
        'FCC_UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FCC_RollbackFile'                Removes a file from a PLM volume.
        'FCC_RollbackFiles'                Removes multiple files from a PLM volume.
        
        fccjavaclientproxy.jar            Java
        
        'FileCacheProxy.UploadFileToPLM'        Uploads a file to a PLM volume.
        'FileCacheProxy.UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FileCacheProxy.RollbackFile'                Removes a file from a PLM volume.
        'FileCacheProxy.RollbackFiles'            Removes multiple files from a PLM volume.
        
        FSCClientProxy.dll
        FSCNativeClientProxy.dll        C
        
        'FSC_Upload'                    Uploads a file to a PLM volume.
        'FSC_UploadMultiple'        Uploads multiple files to a PLM volume.
        'FSC_Rollback'                Removes a file from a PLM volume.
        'FSC_RollbackMultiple'        Removes multiple files from a PLM volume.
        
        fscjavaclientproxy.jar            Java
        
        'CommonsFSCWholeFileIOImpl.upload'        Uploads one or more files to a PLM volume.
        'CommonsFSCWholeFileIOImpl.rollback'        Removes one or more files from a PLM volume.
        
        
        3.    Visualization operations for creating the VisStructureContext when the markups are created against
        Teamcenter objects like BOMView, BOMViewRevision or Teamcenter runtime objects like BOMLines from Structure
        Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs (const std::vector< Teamcenter::Soa::Internal::Visualization::_2008_06::
        StructureManagement::CreateVisSCsFromBOMsInfo > & info)'; 
        
        4.    Visualization operations for creating or updating the session Dataset, associating the Vis_Session
        Dataset with the input Teamcenter objects and committing the files to the session Dataset.
        
        NOTE:  'createSessionModel' / 'updateSessionModel' operation should be followed by 'saveSession' operation.
        """
        return cls.execute_soa_method(
            method_name='saveSession',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SaveSessionResponse,
        )

    @classmethod
    def updateMarkup(cls, inputs: List[MarkupUpdateInput]) -> MarkupUpdateResponse:
        """
        This operation updates the markup Datasets of types DirectModel3DMarkup, Markup or DirectModelMarkup and
        commits the uploaded files to the Dataset.  In addition, this operation may associate the markup Dataset to an
        input Teamcenter object (e.g. VisStructureContext) with relevant relation as per the data model.  Associated
        Dataset and ImanFile objects are then accessible to other authorized clients throughout the PLM system.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        
        Use cases:
        The mechanism for a client application to update markups requires several steps.
        
        1.    Client application invokes the 'FileManagementService::getWriteTickets' operation to obtain an FMS write
        ticket for each file / ImanFile object that will be stored in the markup Dataset. 
        
        2.    Use a FMS operation to upload the files to the PLM volume (see the Dependencies section below).  The
        client application is responsible for making sure that the FMS operation used to upload the files indicates
        that the file uploads were successful. If a file upload were to fail, then the file should not be committed. 
        This should effectively prevent the construction of database infrastructure referencing files not present in
        the volume.  Check the documentation for each operation to determine how to react to upload failures.  Some
        upload operations are defined in such a way that a single result code is returned to the caller, or a single
        exception thrown, to indicate that the bulk file upload was entirely unsuccessful.  These operations typically
        roll back all the successfully uploaded files before returning to the caller.  Some operations may accept a
        flag indicating whether uploads should continue when an error is encountered.  Other operations return a
        separate result code for each file, indicating which files were successfully uploaded to a PLM volume and which
        uploads failed.
        
        It is the responsibility of the client application to either commit or rollback all successfully uploaded
        files.  Files that failed to upload need not be rolled back.
        
        Client responsibilities if upload of files to the volume fails:
        a.    Client applications must not invoke the 'updateMarkup' visualization operation on files that did not
        successfully upload to the PLM volume.  This causes file access errors downstream, when clients attempt to
        reference (or download) the file data, which will be missing from the PLM volume.
        b.    In the event of a partial upload success (some files uploaded successfully, but others did not), it is
        the responsibility of the client application to determine whether it is acceptable in context to commit the
        successfully uploaded files to the PLM system.
        - If not, then there is a companion FMS operation to roll back the successfully uploaded files (see
        Dependencies section).  The rollback method removes the files from the PLM volume.
        - If so, then it is the responsibility of the client application to avoid including information corresponding
        to the files that did not successfully upload to the PLM volume in the input list passed to the 'updateMarkup'
        visualization operation.
        
        
        
        3.    The client application then invokes the 'updateMarkup' visualization operation on the successfully
        uploaded files.   This step updates the visualization supported markup Dataset of types DirectModel3DMarkup,
        Markup, DirectModelMarkup and commits the uploaded files to the Dataset.  In addition, this operation may
        associate the updated markup Dataset with input Teamcenter object like VisStructureContext with relevant
        relation as per the data model. Associated Dataset and IMANFile objects are then accessible to other authorized
        clients through the PLM system. If there are any failures during this operation, client is responsible for
        rolling back the associated file from the volume through FMS operations.  Check the documentation for each
        operation to determine how to react to cleanup activity.
        
        Note:  In case markups are created against BOMView or BOMViewRevision or Teamcenter runtime objects like
        BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner, it is the responsibility of the
        client to create VisStructureContext object and provide VisStructureContext as an input to the operation.
        
        Use Case References:
        This operation is used in conjunction with other FileManagementService service operations, Visualization
        service operations and the FMS.  Please consult the documentation for each of these available operations for
        details on the requirements, usage, and environments in which they should be used.  
        
        These dependencies include:
        
        1.    FMS operation for obtaining a FMS write ticket:
        'FileManagementService::getWriteTickets'    This operation obtains FMS write tickets for IMANFile objects.
        
        2.    FMS methods for uploading and rolling back the files to/from the PLM volume.
        
        Library                        Binding
        
        FCCClientProxy.lib                C
        
        'FCC_UploadFileToPLM'        Uploads a file to a PLM volume.
        'FCC_UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FCC_RollbackFile'                Removes a file from a PLM volume.
        'FCC_RollbackFiles'                Removes multiple files from a PLM volume.
        
        fccjavaclientproxy.jar            Java
        
        'FileCacheProxy.UploadFileToPLM'        Uploads a file to a PLM volume.
        'FileCacheProxy.UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FileCacheProxy.RollbackFile'                Removes a file from a PLM volume.
        'FileCacheProxy.RollbackFiles'            Removes multiple files from a PLM volume.
        
        FSCClientProxy.dll
        FSCNativeClientProxy.dll        C
        
        'FSC_Upload'                    Uploads a file to a PLM volume.
        'FSC_UploadMultiple'        Uploads multiple files to a PLM volume.
        'FSC_Rollback'                Removes a file from a PLM volume.
        'FSC_RollbackMultiple'        Removes multiple files from a PLM volume.
        
        fscjavaclientproxy.jar            Java
        
        'CommonsFSCWholeFileIOImpl.upload'        Uploads one or more files to a PLM volume.
        'CommonsFSCWholeFileIOImpl.rollback'        Removes one or more files from a PLM volume.
        
        3.    Visualization operations for creating the VisStructureContext when the markups are created against
        Teamcenter objects like BOMView, BOMViewRevision or Teamcenter runtime objects like BOMLines from Structure
        Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs (const std::vector< Teamcenter::Soa::Internal::Visualization::_2008_06::
        StructureManagement::CreateVisSCsFromBOMsInfo > & info); '
        
        4.    Visualization operations for creating the markup Dataset, associating the created markup Dataset and the
        input Teamcenter objects and committing the files to the markup Dataset.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement::MarkupResponse createMarkup ( const
        std::vector<Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement::MarkupInput >& inputs ) ;'
        """
        return cls.execute_soa_method(
            method_name='updateMarkup',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=MarkupUpdateResponse,
        )

    @classmethod
    def updateSessionModel(cls, inputs: List[UpdateSesssionModel]) -> SessionModelUpdateResponse:
        """
        This operation updates the Vis_Session Dataset and commits the uploaded files to the Dataset. Updating of
        Vis_Session Dataset involves committing miscellaneous files like markups, images, dependent files etc. and
        attaching necessary relations to the Teamcenter objects as per the data model. This operation must be followed
        by a call to the 'saveSession' operation. The information of all the relevant Teamcenter managed objects in the
        session is noted in the Teamcenter visualization session file and committed to the Vis_Session Dataset via the
        'saveSession' operation. Associated Dataset and IMANFile objects are then accessible to other authorized
        clients through the PLM system.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        
        Use cases:
        The mechanism for a client application to update session contains several steps.
        
        1.    Client application invokes the' FileManagementService::getWriteTickets' operation to obtain an FMS write
        ticket for each file / IMANFile object that will be stored in the markup Dataset. 
        
        2.    Use a FMS operation to upload the files to the PLM volume (see the Dependencies section below).  The
        client application is responsible for making sure that the FMS operation used to upload the files indicates
        that the file uploads were successful. If a file upload were to fail, then the file should not be committed. 
        This should effectively prevent the construction of database infrastructure referencing files not present in
        the volume.  Check the documentation for each operation to determine how to react to upload failures.  Some
        upload operations are defined in such a way that a single result code is returned to the caller, or a single
        exception thrown, to indicate that the bulk file upload was entirely unsuccessful.  These operations typically
        roll back all the successfully uploaded files before returning to the caller.  Some operations may accept a
        flag indicating whether uploads should continue when an error is encountered.  Other operations return a
        separate result code for each file, indicating which files were successfully uploaded to a PLM volume and which
        uploads failed.
        
        It is the responsibility of the client application to either commit or rollback all successfully uploaded
        files.  Files that failed to upload need not be rolled back.
        
        Client responsibilities if upload of files to the volume fails:
        a.    Client applications must not invoke the 'updateSessionModel' visualization operation on files that did
        not successfully upload to the PLM volume.  This causes file access errors downstream, when clients attempt to
        reference (or download) the file data, which will be missing from the PLM volume.
        b.    In the event of a partial upload success (some files uploaded successfully, but others did not), it is
        the responsibility of the client application to determine whether it is acceptable in context to commit the
        successfully uploaded files to the PLM system.
        - If not, then there is a companion FMS operation to roll back the successfully uploaded files.  The rollback
        method removes the files from the PLM volume.
        - If so, then it is the responsibility of the client application to avoid including information corresponding
        to the files that did not successfully upload to the PLM volume in the input list passed to the
        'updateSessionModel' visualization operation.
        
        
        
        3.    The client application then invokes the 'updateSessionModel' visualization operation on the successfully
        uploaded files. 
        This step updates the session Dataset of type Vis_Session and commits the uploaded files to the Dataset.  In
        addition, this operation also associates the session Dataset to the input Teamcenter objects with relevant
        relations as per the data model. Associated Dataset and ImanFile objects are then accessible to other
        authorized clients through the PLM system. If there are any failures during this operation, client is
        responsible for rolling back the associated file from the volume through FMS operation.  Check the
        documentation for each operation to determine how to react to cleanup activity.
        
        Note:  In case the session is created against BOMView or BOMViewRevision or Teamcenter runtime objects like
        BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner, it is the responsibility of the
        client to create VisStructureContext object and provide VisStructureContext as an input to the
        'updateSessionModel' operation.
        
        4.    After updating the Vis_Session Dataset via 'updateSessionModel', the information for all the relevant
        Teamcenter managed objects in the session is noted in the session file (.vf). An FMS write ticket is then
        obtained for the session file and the file uploaded via FMS operation to Teamcenter volume.
        
        5.    Use 'saveSession' visualization operation to commit the session file to the Vis_Session Dataset.
        
        NOTE: It is the responsibility of the client to do cleanup as appropriate according to failures types.
        
        Use Case References:
        
        This operation is used in conjunction with other FileManagementService service operations, Visualization
        service operations and the FMS.  Please consult the documentation for each of these available operations for
        details on the requirements, usage, and environments in which they should be used.  These dependencies include:
        
        1.    FMS operation for obtaining an FMS write ticket.
        'FileManagementService::getWriteTickets'        This operation obtains FMS write tickets for IMANFile objects 
        
        2.    FMS operations for uploading and rolling back the files to/from the PLM volume.
        
        Library                        Binding
        
        FCCClientProxy.lib                C
        
        'FCC_UploadFileToPLM'        Uploads a file to a PLM volume.
        'FCC_UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FCC_RollbackFile'                Removes a file from a PLM volume.
        'FCC_RollbackFiles'                Removes multiple files from a PLM volume.
        
        fccjavaclientproxy.jar            Java
        
        'FileCacheProxy.UploadFileToPLM'        Uploads a file to a PLM volume.
        'FileCacheProxy.UploadFilesToPLM    '    Uploads multiple files to a PLM volume.
        'FileCacheProxy.RollbackFile'                Removes a file from a PLM volume.
        'FileCacheProxy.RollbackFiles'            Removes multiple files from a PLM volume.
        
        FSCClientProxy.dll
        FSCNativeClientProxy.dll        C
        
        'FSC_Upload'                    Uploads a file to a PLM volume.
        'FSC_UploadMultiple'        Uploads multiple files to a PLM volume.
        'FSC_Rollback'                Removes a file from a PLM volume.
        'FSC_RollbackMultiple'        Removes multiple files from a PLM volume.
        
        fscjavaclientproxy.jar            Java
        
        'CommonsFSCWholeFileIOImpl.upload'        Uploads one or more files to a PLM volume.
        'CommonsFSCWholeFileIOImpl.rollback'        Removes one or more files from a PLM volume.
        
        3.    'Visualization' operations for creating the VisStructureContext when the markups are created against
        Teamcenter objects like BOMView, BOMViewRevision or Teamcenter runtime objects like BOMLines from Structure
        Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs (const std::vector< Teamcenter::Soa::Internal::Visualization::_2008_06::
        StructureManagement::CreateVisSCsFromBOMsInfo > & info); '
        
        4.    'Visualization' operations for creating or updating the session Dataset, associating the Vis_Session
        Dataset with the input Teamcenter objects and committing the files to the session Dataset.
        
        NOTE:  'createSessionModel' / 'updateSessionModel' operation should be followed by 'saveSession' operation.
        """
        return cls.execute_soa_method(
            method_name='updateSessionModel',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SessionModelUpdateResponse,
        )

    @classmethod
    def updateTwoDSnaphot(cls, input: List[UpdateTwoDSnapshotInput]) -> UpdateTwoDSnapshotResponse:
        """
        A 2D snapshot dataset (Vis_snapshot_2D_View_Data) is an object in Teamcenter used to capture the state of a 2D
        scene including markups and viewport information.  This object is used for manufacturing planning and issue
        capture use cases.  The dataset and associated data model is designed to support change management, and updates
        to the base image without significant rework to the previously captured snapshots.  That is, the snapshots can
        be easily re-used and updated.  The data model consists of a dataset storing several files (markup layer CGM
        files, viewport xml file, thumbnail image, and asset image), a relation to the ItemRevision managing the base
        image, and a form containing attributes that can be used to search for snapshots based on certain attribute
        criteria. 
        This service is focused on updating a 2D snapshot dataset that has been previously created with the
        createTwoDSnapshot service.  Several of the input structures are shared between create and update services. 
        This service updates a list of 2D snapshot Datasets with the named references provided.
        
        Use cases:
        User updates a snapshot of a particular view of a 2D image with markups to illustrate an area of interest. 
        This snapshot dataset is updated in Teamcenter and later re-opened, recreating the view.
            1.    User opens a 2D snapshot dataset that has been previously created.  This can be done by sending the
        dataset to the MPP application or Lifecycle viewer, or by finding the dataset in the 2D snapshot gallery of the
        2D viewer embedded in the Manufacturing Process Planner (MPP) application
            2.    The system recreates the 2D scene represented by the 2D snapshot by opening the base image and
        applying the viewfile information and markups
            3.    The user updates the 2D scene by changing it in some way.  Typical changes are changing the view
        port, editing the markup layers, or editing the form data
            4.    User updates the 2D snapshot using the appropriate user action.
            5.    The system calls the updateTwoDSnapshot service and provides the new information including new
        dataset information (e.g. type, name, description), and new named reference information (e.g. new markup layer
        files, new view file, etc).  The dataset is updated with the appropriate data model by this service.
        
        When the Vis_snapshot_2D_View_Data dataset is updated, a new version of the dataset is created with the new and
        updated information.   
        """
        return cls.execute_soa_method(
            method_name='updateTwoDSnaphot',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=UpdateTwoDSnapshotResponse,
        )

    @classmethod
    def createLaunchFile(cls, idInfos: List[IdInfo], serverInfo: ServerInfo, userDataAgentInfo: UserAgentDataInfo, sessionInfo: SessionInfo) -> VVITicketsResponse:
        """
        This operation generates a VVI file which is used to launch integrated standalone visualization or Lifecycle
        Viewer with selected objects from Teamcenter and preserve a two way communication link between the viewer and
        the server.  These files are not intended to be permanent (i.e. transient) and should be generated with each
        launch.  For example, the VVI format is not guaranteed to be supported if the server or viewer is updated.  VFZ
        files are used if more than one object is launched at a time.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes) which is used to download the VVI file from the transient file volume to the client.  This
        operation generates the launch file (VFZ or VVI), stores it in the FMS transient volume, and returns the FMS
        ticket.  The client that initiated this operation is responsible for downloading the transient file (VVI or
        VFZ) with the transient ticket from transient volume to a local file system. Transient (VVI or VFZ) file is
        then consumed by the visualization client.  The viewer will then establish the server connection and load the
        object(s) specified in the VVI file.  Launch on multiple objects will generate a VFZ file (zip of all the VVI
        files) and transient ticket of VFZ file would be sent to client. 
        
        This service supports launch on one or more Teamcenter persistent objects such as Dataset, Item, ItemRevision,
        BOMViewRevision, and BOMView. It also supports launch of configured structure containing BOMLines from
        Structure Manager or BOPLines from Manufacturing Process Planner, but in this case the caller must first create
        a VisStructureContext object (See Dependency section for operation to use).  Valid launch object types and
        order preference can be configured with the Teamcenter Preferences VMU_Datasets, VMU_FileSearchOrder and
        VMU_RelationSearchOrder.
        
        
        Use cases:
        This operation supports the mechanism of visualizing Teamcenter specific objects in Teamcenter Visualization
        client. There are several steps to support this mechanism.
        
        1.    The client application that initiates the launch will provide:
        
        A vector of IdInfo objects that contains one or more pieces of information about Teamcenter objects that needs
        to be visualized in the viewer (e.g., If Dataset is launched, then information about its Item, ItemRevision and
        type of operation, including any additional information can be provided). Note: In case launch of Teamcenter
        runtime objects like BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner, it is the
        responsibility of the client to create VisStructureContext object and provide VisStructureContext as the object
        to be launched (See Dependency section for operation to use).
        SessionInfo object contains session relevant information for Teamcenter Visualization to connect to the session
        (e.g., session discriminator and any other additional session relevant key value pair)
        ServerInfo object contains server information for Teamcenter Visualization to connect to the server. (e.g.,
        protocol, server URL, connection mode of the server and any other additional server relevant key value pair)
        UserAgentDataInfo object contains client application information who initiated the launch. (e.g., application
        name, application version, and any other additional client application relevant key value pair).
        
        
        2.    After gathering the necessary information as listed in step 1, client application then invokes the
        DataManagementService::createLaunchFile operation to obtain an FMS read ticket for the launch file (VVI or
        VFZ), that has relevant information for visualizing Teamcenter persistent or runtime objects.
        
        See the Dependencies section below for details.
        
        3.    Use a File Management System (FMS) Application Programmatic Interface (API) to download the transient
        file (VVI or VFZ) from transient volume.
        
        Check the documentation for each API to determine how to react to download failures.
        
        Use Case References:
        This operation is used in conjunction with other FileManagementService service operations, Visualization
        service operations and the FMS. Please consult the documentation for each of these available operations for
        details on the requirements, usage, and environments in which they should be used. 
        
        These references include:
        
        1.    FMS methods for registering the transient file tickets prior to downloading the transient file.
        
        Library                    Binding
        FCCClientProxy.lib            C            
        
        FCC_RegisterTicket        Decrypts the ticket, registers the File with client cache, and returns File UID that
        may or may not correspond to the UID of the ticketed file.
        FCC_RegisterTickets    Decrypts multiple tickets, registers the Files with client cache, and returns File UIDs
        that may or may not correspond to the UID of the ticketed file.
        
        
        fccjavaclientproxy.jar        Java
        
        FileCacheProxy.RegisterTicket        Decrypts the ticket, registers the File with client cache, and returns
        File UID that may or may not correspond to the UID of the ticketed file.
        FileCacheProxy. RegisterTickets        Decrypts multiple tickets, registers the Files with client cache, and
        returns File UIDs that may or may not correspond to the UID of the ticketed file.
        
        
        2.    FMS methods for downloading the single transient file to a local file system from Teamcenter Transient
        volume.
        
        Library                    Binding
        FCCClientProxy.lib            C
        
        FCC_DownloadFileToLocation        Downloads a file from a Transient volume into a local filename specified by
        the caller.
        FCC_DownloadFilesToLocation    Downloads multiple files from a Transient volume into local filenames specified
        by the caller.
        
        
        fccjavaclientproxy.jar        Java
        
        FileCacheProxy.DownloadFileToLocation    Downloads a file from a Transient volume into a local filename
        specified by the caller.
        FileCacheProxy.DownloadFilesToLocation    Downloads multiple files from a Transient volume into local filenames
        specified by the caller.
        
        
        FSCClientProxy.dll
        FSCNativeClientProxy.dll    C    
        
        FSC_Download            Downloads a file from a Transient volume into a local filename specified by the caller.
        FSC_DownloadMultiple    Downloads multiple files from a Transient volume into local filenames specified by the
        caller.
        
        
        fscjavaclientproxy.jar    Java    
        
        CommonsFSCWholeFileIOImpl.download    Downloads one or more files from a Transient volume into local filenames
        specified by the caller.
        
        
        NOTE: 
        
        In 4 tier mode, you can also use any of the FSC APIs with transient file tickets. In 2 tier mode, a client must
        use one of the 4 FCC calls listed above. This list may not be complete. Several sets of wrapper classes exist
        within Teamcenter source code base which invoke these FMS operation implementations.
        
        
        3.    Visualization operations for creating the VisStructureContext from clients that initiate the launch of
        Teamcenter runtime objects like BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs'
        """
        return cls.execute_soa_method(
            method_name='createLaunchFile',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'idInfos': idInfos, 'serverInfo': serverInfo, 'userDataAgentInfo': userDataAgentInfo, 'sessionInfo': sessionInfo},
            response_cls=VVITicketsResponse,
        )

    @classmethod
    def createMarkup(cls, inputs: List[MarkupInput]) -> MarkupResponse:
        """
        This operation creates the visualization supported markup Dataset of types DirectModel3DMarkup, Markup or
        DirectModelMarkup and commits the uploaded files to the Dataset.  In addition, this operation also associates
        the newly created markup Dataset to input Teamcenter objects with relevant relations as per the data model. 
        Associated Dataset and IMANFile objects are then accessible to other authorized clients throughout the PLM
        system.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        Use cases:
        The mechanism for a client application to associate the markups to the Teamcenter objects requires several
        steps.  
        
        1.    Client application invokes the' FileManagementService::getWriteTickets' operation to obtain an FMS write
        ticket for each file / IMANFile object that will be stored in the markup Dataset. 
        
        See the Dependencies section below for details.
        
        2.    Use a FMS operation to upload the files to the PLM volume (see the Dependencies section below).  The
        client application is responsible for making sure that the FMS operation used to upload the files indicates
        that the file uploads were successful. If a file upload were to fail, then the file should not be committed. 
        This should effectively prevent the construction of database infrastructure referencing files not present in
        the volume.  Check the documentation for each operation to determine how to react to upload failures.  Some
        upload operations are defined in such a way that a single result code is returned to the caller, or a single
        exception thrown, to indicate that the bulk file upload was entirely unsuccessful.  These operations typically
        roll back all the successfully uploaded files before returning to the caller.  Some operations may accept a
        flag indicating whether uploads should continue when an error is encountered.  Other operations return a
        separate result code for each file, indicating which files were successfully uploaded to a PLM volume ahich
        uploads failed.
        
        It is the responsibility of the client application to either commit or rollback all successfully uploaded
        files.  Files that failed to upload need not be rolled back.
        
        Client responsibilities if upload of files to the volume fails:
        a.    Client applications must not invoke the 'createMarkup' visualization operation on files that did not
        successfully upload to the PLM volume.  This causes file access errors downstream, when clients attempt to
        reference (or download) the file data, which will be missing from the PLM volume.
        
        b.    In the event of a partial upload success (some files uploaded successfully, but others did not), it is
        the responsibility of the client application to determine whether it is acceptable in context to commit the
        successfully uploaded files to the PLM system.
        - If not, then there is a companion FMS operation to roll back the successfully uploaded files (see
        Dependencies section).  The rollback method removes the files from the PLM volume.
        - If so, then it is the responsibility of the client application to avoid including information corresponding
        to the files that did not successfully upload to the PLM volume in the input list passed to the 'createMarkup'
        visualization operation.
        
        
        
        3.    The client application then invokes the createMarkup visualization operation on the successfully uploaded
        files.  This step creates the visualization supported markup Dataset of types DirectModel3DMarkup, Markup,
        DirectModelMarkup and commits the uploaded files to the Dataset.  In addition, this operation also associates
        the newly created markup Dataset with input Teamcenter objects with relevant relations as per the data model. 
        Associated Dataset and IMANFile objects are then accessible to other authorized clients through the PLM system.
        If there are any failures during this operation, the client is responsible for rolling back the associated file
        from the volume through FMS operation.  Check the documentation for each operation to determine how to react to
        cleanup activity.
        
        Example:
        Markup Dataset of type DirectModel3DMarkup is created for markup files authored on 3D data (e.g.,
        DirectModel/DirectModelAssembly/VisStructureContext).
        
        Note:  In case markups are created against BOMView or BOMViewRevision or Teamcenter runtime objects like
        BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner, it is the responsibility of the
        client to create VisStructureContext object and provide VisStructureContext as an input to the operation (See
        Dependency section for service operations to use).
        
        Markup Datasets of type Markup are created for markup files created against 2D data (e.g., Image Dataset).
        
        Use Case References:
        
        1.    FMS operation for obtaining an FMS write ticket.
        
        'FileManagementService::getWriteTickets'    This operation obtains FMS write tickets for IMANFile objects 
        
        2.    FMS operations for uploading and rolling back the files to/from the PLM volume.
        
        Library                        Binding
        
        FCCClientProxy.lib                C
        
        'FCC_UploadFileToPLM'        Uploads a file to a PLM volume.
        'FCC_UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FCC_RollbackFile'                Removes a file from a PLM volume.
        'FCC_RollbackFiles'                Removes multiple files from a PLM volume.
        
        fccjavaclientproxy.jar        Java
        
        'FileCacheProxy.UploadFileToPLM'        Uploads a file to a PLM volume.
        'FileCacheProxy.UploadFilesToPLM'        Uploads multiple files to a PLM volume.
        'FileCacheProxy.RollbackFile'                Removes a file from a PLM volume.
        'FileCacheProxy.RollbackFiles'            Removes multiple files from a PLM volume.
        
        FSCClientProxy.dll
        FSCNativeClientProxy.dll        C
        
        'FSC_Upload    '                Uploads a file to a PLM volume.
        'FSC_UploadMultiple'        Uploads multiple files to a PLM volume.
        'FSC_Rollback'                 Removes a file from a PLM volume.
        'FSC_RollbackMultiple'        Removes multiple files from a PLM volume.
        
        fscjavaclientproxy.jar        Java
        
        'CommonsFSCWholeFileIOImpl.upload'    Uploads one or more files to a PLM volume.
        'CommonsFSCWholeFileIOImpl.rollback'    Removes one or more files from a PLM volume.
        
        NOTE: This list may not be complete.  Several sets of wrapper classes exist within Teamcenter source code base
        which invoke these FMS operation implementations.
        
        3.    Visualization operations for creating the VisStructureContext when the markups are created against
        Teamcenter objects like BOMView, BOMViewRevision or Teamcenter runtime objects like BOMLines from Structure
        Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs (const std::vector< Teamcenter::Soa::Internal::Visualization::_2008_06::
        StructureManagement::CreateVisSCsFromBOMsInfo > & info);' 
        
        4.    Visualization operations for creating the markup Dataset, associating the created markup Dataset and the
        input Teamcenter objects and committing the files to the markup Dataset.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement::MarkupResponse createMarkup ( const
        std::vector<Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement::MarkupInput >& inputs ) ;'
        """
        return cls.execute_soa_method(
            method_name='createMarkup',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=MarkupResponse,
        )

    @classmethod
    def createSessionModel(cls, inputs: List[SessionModelInput]) -> SessionModelResponse:
        """
        This operation creates the data model for the Vis_Session Dataset type and commits the uploaded files (markups,
        images etc) to the Dataset.  In addition, this operation also associates the newly created Vis_Session Dataset
        to input Teamcenter objects with relevant relations as per the data model. After initial creation, the
        'saveSession' Visualization operation is a required step and needs to be invoked to successfully upload the
        Teamcenter Visualization session file to the Vis_Session Dataset.  Saving of Teamcenter visualization session
        to Teamcenter is a two step process. It contains internal references to the other files it depends on, so they
        must be saved first via 'createSessionModel' Visualization operation (see Dependencies Section). After the
        references are persisted, then the Teamcenter visualization session file is persisted via 'saveSession'
        Visualization operation (see Dependencies Section).  Associated Dataset and ImanFile objects are then
        accessible to other authorized clients throughout the PLM system.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        Use cases:
        The mechanism for a client application to associate the session to the Teamcenter objects requires several
        steps.
        
        1.    Client application invokes the 'FileManagementService::getWriteTickets' operation to obtain an FMS write
        ticket for each file / IMANFile object that will be stored in the markup Dataset. 
        
        See the Use Case Referencion below for details.
        
        2.    Use a FMS operation to upload the files to the PLM volume (see the Use Case References section below).
        The client application is responsible for making sure that the FMS operation used to upload the files indicates
        that the file uploads were successful. If a file upload were to fail, then the file should not be committed.
        This should effectively prevent the construction of database infrastructure referencing files not present in
        the volume. Check the documentation for each operation to determine how to react to upload failures. Some
        upload operations are defined in such a way that a single result code is returned to the caller, or a single
        exception thrown, to indicate that the bulk file upload was entirely unsuccessful. These operations typically
        roll back all the successfully uploaded files before returning to the caller. Some operations may accept a flag
        indicating whether uploads should continue when an error is encountered. Other operations return a separate
        result code for each file, indicating which files were successfully uploaded to a PLM volume and which uploads
        failed.
        
        It is the responsibility of the client application to either commit or rollback all successfully uploaded
        files. Files that failed to upload need not be rolled back.
        
        Client responsibilities if upload of files to the volume fails:
        a.    Client applications must not invoke the createSessionModel visualization operation on files that did not
        successfully upload to the PLM volume. This causes file access errors downstream, when clients attempt to
        reference (or download) the file data, which will be missing from the PLM volume.
        
        b.    In the event of a partial upload success (some files uploaded successfully, but others did not), it is
        the responsibility of the client application to determine whether it is acceptable in context to commit the
        successfully uploaded files to the PLM system.
        
        If not, then there is a companion FMS operation to roll back the successfully uploaded files (see Dependencies
        section). The rollback method removes the files from the PLM volume.
        If so, then it is the responsibility of the client application to avoid including information corresponding to
        the files that did not successfully upload to the PLM volume in the input list passed to the createSessionModel
        visualization operation.
        
        
        3.    The client application then invokes the createSessionModel visualization operations on the successfully
        uploaded files. 
        This step creates the visualization supported session Dataset of type Vis_Session and commits the uploaded
        files to the Dataset. In addition, this operation also associates the newly created session Dataset with input
        Teamcenter objects with relevant relations as per the data model. Associated Dataset and IMANFile objects are
        then accessible to other authorized clients through the PLM system. If there are any failures during this
        operation, client is responsible for rolling back the associated file from the volume through FMS operations.
        Check the documentation for each API to determine how to react to cleanup activity.
        
        Note: In case session is created against BOMView, BOMViewRevision or Teamcenter runtime objects like BOMLines
        from Structure Manager or BOPLines from Manufacturing Process Planner, it is the responsibility of the client
        to create VisStructureContext object and provide VisStructureContext as an input to the operation (See Use Case
        References section for service operations to use).
        
        Use Case References:
        This operation is used in conjunction with other FileManagementService service operations, Visualization
        service operations and the FMS. Please consult the documentation for each of these available operations for
        details on the requirements, usage, and environments in which they should be used. These dependencies include:
        
        1.    FMS operation for obtaining a FMS write ticket:
        FileManagementService::getWriteTickets        This operation obtains FMS write tickets for IMANFile objects 
        
        2.    FMS methods for uploading and rolling back the files to/from the PLM volume.
        
        Library                        Binding
        
        FCCClientProxy.lib                C
        
        FCC_UploadFileToPLM        Uploads a file to a PLM volume.
        FCC_UploadFilesToPLM        Uploads multiple files to a PLM volume.
        FCC_RollbackFile                Removes a file from a PLM volume.
        FCC_RollbackFiles                Removes multiple files from a PLM volume.
        
        fccjavaclientproxy.jar            Java
        
        FileCacheProxy.UploadFileToPLM        Uploads a file to a PLM volume.
        FileCacheProxy.UploadFilesToPLM        Uploads multiple files to a PLM volume.
        FileCacheProxy.RollbackFile                Removes a file from a PLM volume.
        FileCacheProxy.RollbackFiles            Removes multiple files from a PLM volume.
        
        FSCClientProxy.dll
        FSCNativeClientProxy.dll        C
        
        FSC_Upload                    Uploads a file to a PLM volume.
        FSC_UploadMultiple        Uploads multiple files to a PLM volume.
        FSC_Rollback                Removes a file from a PLM volume.
        FSC_RollbackMultiple        Removes multiple files from a PLM volume.
        
        fscjavaclientproxy.jar            Java
        
        CommonsFSCWholeFileIOImpl.upload        Uploads one or more files to a PLM volume.
        CommonsFSCWholeFileIOImpl.rollback        Removes one or more files from a PLM volume.
        
        3.    Visualization operations for creating the VisStructureContext when the session are created against
        Teamcenter objects like BOMView, BOMViewRevision or Teamcenter runtime objects like BOMLines from Structure
        Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs '
        
        4.    Visualization operations for creating the session Dataset, associating the created Vis_Session Dataset
        and the input Teamcenter objects and committing the files to the session Dataset.
        NOTE: The createSessionModel operation should be followed by saveSession operation.
        
        Following are the list of Visualization operations needed to create Vis_Session Dataset:
        
        'Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement::SessionModelResponse createSessionModel(
        Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement::SaveSessionResponse saveSession '
        
        NOTE: Please refer to Visualization service documentation for saveSession operation. 
        
        """
        return cls.execute_soa_method(
            method_name='createSessionModel',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SessionModelResponse,
        )

    @classmethod
    def createTwoDSnapshot(cls, input: List[TwoDSnapshotInput]) -> CreateTwoDSnapshotResponse:
        """
        A 2D snapshot dataset (Vis_snapshot_2D_View_Data) is an object in Teamcenter used to capture the state of a 2D
        scene including markups and viewport information.  This object is used for manufacturing planning and issue
        capture use cases.  The dataset and associated data model is designed to support change management, and updates
        to the base image without significant rework to the previously captured snapshots.  That is, the snapshots can
        be easily re-used and updated.  The data model consists of a dataset storing several files (markup layer CGM
        files, viewport xml file, thumbnail image, and asset image), a relation to the ItemRevision managing the base
        image, and a form containing attributes that can be used to search for snapshots based on certain attribute
        criteria. 
        This service creates a list of 2D snapshot Datasets and creates the TC_snap_shot_2d relation type between
        created Dataset and the ItemRevision containing the base image.   The service creates all elements of the data
        model including all relations and named references.
        
        
        Use cases:
        User creates a snapshot of a particular view of a 2D image with markups to illustrate an area of interest. 
        This snapshot is stored as a dataset in Teamcenter and later re-opened, recreating the view.  Typical use case
        steps are as follows:
            1.    User opens an ItemRevision that contains a 2D image into visualization.  Most typically this is a 2D
        drawing for a part that is to be manufactured.
            2.    User zooms and pans on the image to display the area of interest
            3.    User adds markups and annotations to the image
            4.    User saves a 2D snapshot object in Teamcenter that captures the view data for the 2D scene
            5.    System calls this service (createTwoDSnapshot) and passes the base image ItemRevision, dataset
        information (e.g. name, etc), file information to upload, and form data containing special attributes attached
        to the dataset.  The dataset is created with appropriate data model by this service.
        
        Once a 2D snapshot is created in Teamcenter, it can be opened in visualization to recreate a 2D scene.   The
        dataset can be sent to a viewer directly, or it can be displayed in the 2D snapshot gallery contained in the 2D
        viewer tab of the Manufacturing Process Planner (MPP) application.  
        """
        return cls.execute_soa_method(
            method_name='createTwoDSnapshot',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateTwoDSnapshotResponse,
        )

    @classmethod
    def authenticateUser(cls, username: str, password: str) -> bool:
        """
        This method validates that the specified username and password is valid. The call will take at a minimum 2
        seconds to complete to prevent a possible password probing attack.
        
        Use cases:
        A client can use this method to validate that the specified user and password credentials are valid. In some
        cases, there might be a need to impersonate a user without logging out from the current session. This method
        simply validated that the username and password combination is valid.
        
        Exceptions:
        >The service does not throw any exceptions but error codes will be returned in the service data on failure. 
        
        Return codes:
        10011: the specified use cannot be found.
        208016: If a required argument is not specified like the username.
        """
        return cls.execute_soa_method(
            method_name='authenticateUser',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'username': username, 'password': password},
            response_cls=bool,
        )

    @classmethod
    def getLatestFileReadTickets(cls, info: List[GetLatestFileReadTicketsInfo]) -> GetLatestFileReadTicketsResponse:
        """
        PLMXML files consumed by visualization contain file references of the form Dataset UID, IMANFile UID /
        filename.extension.  These references (often referred to as DAKIDs) can be resolved by either using the
        IMANFile UID directly, or by using the Dataset UID / named reference / original file name and
        resolving/objecting the latest version of the file from the volume.  For the visualization integrations, JT
        files may be updated constantly by CAD integration; however, persisted PLMXML files are expected to retrieve
        the latest JT file versions.  This method was created for visualization as a means to fetch the latest version
        of a JT file in bulk during PLMXML file loading.
        
        This method will find the latest named reference using the specified data in the 'GetLatestFileReadTicketsInfo'
        struct. The Dataset specified will have the named references listed. The named reference that has the matching
        original filename will be used to retrieve a read ticket. That way a Dataset can be versioned and this method
        will find the latest named reference even when the 'namedRef' object in the input points to and older version. 
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        
        Use cases:
        This method can be used when object references are stored externally and there is a possibility that the
        dataset had been updated since this reference was recorded. A typical example is a plmxml file created against
        a structure and some parts has been updated by the CAD system after creation. In order to visualize the new
        updated geometry, a ticket for the latest Dataset / named reference should be created. 
        
        PLMXML file loading use case:
        - User loads a PLMXML file that was persisted in Teamcenter or on the local file system
        - Visualization client loads the structure into memory and renders the assembly tree
        - User sets a node visible in the assembly tree
        - System gathers all the child occurrences of the specified node, and collects all the DAKIDs for all the
        children that must be loaded to service the visibility request.  If the top node was selected, a single call
        for parts referenced referenced in the structure will be made
        - The system calls the 'getLatestFileReadTickets' operation and passes all the appropriate DAKID information
        for all the child occurrence JT files that must be loaded to service the visibility request
        - The service returns the FMS file tickets
        - The system uses the FCCClientProxy to stream the files via FMS
        
        """
        return cls.execute_soa_method(
            method_name='getLatestFileReadTickets',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'info': info},
            response_cls=GetLatestFileReadTicketsResponse,
        )

    @classmethod
    def getMetaDataStamp(cls, application: str, servermode: int, ids: List[BusinessObject]) -> MetaDataStampTicketsResponse:
        """
        Metadata stamp for an object is generated based on the Business Object specified using the ids vector. The
        transient ticket for this generated file is sent back in the return data. The ticket can then be used to
        retrieve the file using a FMS service method like 'FccProxy::downloadFiles'. A Metadatastamp template is
        provided in Teamcenter containing MDS file with Teamcenter property name, default values and stamp. The
        Teamcenter site preference MetaDataStamp_template is used to find the item where the dataset template is
        stored. This file is processed and each Attribute specified will be replaced with the matching object property
        values if found. This file will be created in the transient volume and the transient ticket of the file is sent
        to client in the response data.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes).
        
        
        Use cases:
        The 'getMetaDataStamp' operation is used to create an overlay stamp mainly when printing a document from
        Teamcenter Visualization. The Teamcenter Visualization application has an integration to retrieve this file
        when printing a document opened from Teamcenter.  The MDS file created by this service can also be used by the
        VisView Convert and Print utilities.
        """
        return cls.execute_soa_method(
            method_name='getMetaDataStamp',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='DataManagement',
            params={'application': application, 'servermode': servermode, 'ids': ids},
            response_cls=MetaDataStampTicketsResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def createBOMsFromRecipes(cls, info: List[CreateBOMsFromRecipesInfo]) -> CreateBOMsFromRecipesResponse:
        """
        For each CreateBOMsFromRecipesInfo input structure, create a BOMWindow and then configures it according to the
        recipe contained in the supplied configuration object. The supplied configuration object is expected to be of
        type StructureContext, Fnd0StructureContext or ConfigurationContext and if not, then no BOMWindow will be
        created. If the configuration object is of type ConfigurationContext then the topline object must also be
        supplied; the topline object is not used when the configuration object is of type StructureContext because it
        contains its own topline reference. The BOMWindow settings that will be configured include:
        - The topline object.
        - The settings stored in the ConfigurationContext object.
        - If the configuration object is a StructureContext object that represents a manufacturing composition then the
        additional composition windows will also be created and configured.
        
        
        
        Use cases:
        When the user desires to reconstruct a BOMWindow from an object that recorded the configuration recipe of a
        previously configured BOMWindow. For example, this operation is used when sending selected BOMLines from the
        Structure Manager to Teamcenter Visualization. A VisStructureContext object is created to record the
        configuration settings of the BOMWindow of the Structure Manager as well as record the selected BOMLines as a
        list of occurrences. Teamcenter Visualization is given this VisStructureContext object which is used to create
        a BOMWindow configured the same as the BOMWindow in Structure Manger from which from which the
        VisStructureContext object was created.  This BOMWindow is then used by Teamcenter Visualization to obtain
        occurrences that can be visualized or otherwise examined.
        
        The following pruned launch use case illustrates the primary utilization of this method for launching selected
        lines to integrated standalone visualization or Lifecycle Viewer
        - User opens structure in Structure Manager (SM)/Multi Structure Manager (MSM)/Manufacturing Process Planner
        (MPP), configures it, selects some lines, and sends those lines to Lifecycle Viewer or integrated standalone
        visualization.
        - The launching client (system) calls createVisSCsFromBOMs to record the selected lines and BOM configuration
        information.
        - The visualization client receives the request to open the selected lines as an object reference to a
        VisStructureContext object.
        - The visualization client calls the createBOMsFromRecipes operation and passes the VisStructureContext object
        reference.
        - The system creates a BOMWindow and configures it properly (to match launching configuration).
        - The client pulls the occurrence_list property from the VisStructureContext object.
        - The client issues an expandPSFromOccurrenceList call to load the occurrences.
        - The client(system) loads the selected occurrences into the visualization client, the structure is pruned to
        contain only the occurrences sent.
        
        
        Use Case References: 
        The createBOMsFromRecipes operation acts upon previously persisted configuration objects, such as a
        VisStructureContext object.
        
        The following services are used in conjunction with createBOMsFromRecipes to complete the use case above.
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. CreateVisSCsFromBOMs
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. AreRecipesMergible
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. expandPSFromOccurrenceList
        """
        return cls.execute_soa_method(
            method_name='createBOMsFromRecipes',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateBOMsFromRecipesResponse,
        )

    @classmethod
    def createVisSCsFromBOMs(cls, info: List[CreateVisSCsFromBOMsInfo]) -> CreateVisSCsFromBOMsResponse:
        """
        This operation takes a list of BOMLines (the occurrences list) and returns the VisStructureContext objects
        representing the configuration state of the BOMWindow (referred to as the configuration recipe). This
        configuration includes:
        - The occurrence UID chains for the input/selected BOMLines up to but not including the top line. 
        - Optional IMANFile reference to the PLMXML static representation of the BOMWindow.
        
        
        
        This service supports both the interoperation of selected BOMLines from the Teamcenter Rich Client to
        Teamcenter Visualization and also the capture/persistence of the configuration recipe for a particular
        BOMWindow. The occurrence list records the selected BOMLines at the time of interoperation and can be used in
        later operations to populate/expand a BOMWindow with those same occurrences (see 'expandPSFromOccurrenceList'
        operation for more information).
        
        Use cases:
        When the user desires to create a persistent object that records the configuration recipe of a particular
        BOMWindow. The resulting VisStructureContext object would assumedly be used to later reconstruct a BOMWindow
        with the same configuration recipe and the recorded UID occurrence chains would be used to populate/expand the
        constructed BOMWindow with specific BOMLines. For example, this operation is used when sending selected
        BOMLines from the Structure Manager to Teamcenter Visualization and also to capture the configuration recipe
        for storage in Vis Sessions.
        
        Visualization pruned launch use case
        - User opens a structure in Structure Manager (SM)/Multi Structure Manager (MSM)/Manufacturing Process Planner
        (MPP), and configures it
        - User selects some lines they want to send to visualization as a pruned structure
        - System calls 'createVisSCsFromBOMs' to record the selected lines and the configuration of the BOM to send
        
        
        
        Visualization session save use case
        - 1.    User performs Visualization pruned launch use case and loads occurrences into visualization
        - 2.    User creates some authored visualization content (e.g. snapshots, motions, etc)
        - 3.    User saves session to Teamcenter
        - 4.    System calls 'createRecipesFromBOMs' operation to capture the configuration and any pruning information
        as a VisStructureContext object.  UID of object returned.
        - 5.    System writes the VisStructureContext object reference into the visualization session data
        - 6.    System saves the visualiation session dataset to Teamcenter, and relates it to the VisStructureContext
        object created by the service
        
        
        
        Visualization Technical Illustration and 3D Markup save use cases
        Similar to session save use case, except saving a different data type.  Uses this service to create the recipe
        for the authored visualization data in the Teamcenter data model.
        
        Use Case Dependencies: 
        The 'createVisSCsFromBOMs' operation is called with input BOMLines from an existing BOM Window. Therefore, the
        BOMWindow must have already been created and populated with at least a top line.
        
        The following services are used in conjunction with this service to complete the use cases above.
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'createBOMsFromRecipes'
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'areRecipesMergible'
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'expandPSFromOccurrenceList'
        Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement. 'createSessionModel'
        Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement. 'saveSession'
        Teamcenter::Soa::Internal::Visualization::_2008_06::DataManagement. 'updateSessionModel'
        """
        return cls.execute_soa_method(
            method_name='createVisSCsFromBOMs',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateVisSCsFromBOMsResponse,
        )

    @classmethod
    def expandPSFromOccurrenceList(cls, info: List[ExpandPSFromOccurrenceListInfo], pref: ExpandPSFromOccurrenceListPref) -> ExpandPSFromOccurrenceListResponse:
        """
        This operation returns BOMLines for the occurrences recorded in the occurrence list of the input occurrence
        object. Optionally, it can also return the objects of given type and relation that are attached to the objects
        that the BOMLines represent ('objectofBOMLine'). 
        
        The operation can expand datasets and other objects related to parent and child BOMLines.  Expansion of the
        related objects can be controlled by specifying a filter. The filter criteria supported are: relation name,
        related object type, and named references. 
        
        This operation allows for expansion to reference object associated to a named reference.  Typically this is a
        file and in that case a FMS ticket will be returned to provide access to this file. Where a named reference
        points to a file, this operation allows caller to specify from a defined set of handler options, which specific
        handler should be used in choosing file(s) to return.  This is specified through the input parameter
        'NamedRefHandler' (included in the info object).
        
        
        Use cases:
        When the user wants to expand a specific list of occurrences into an existing BOMWindow that contains the
        parent BOMLine of the occurrences.
        This service is used to support the following primary use cases.
        
        Pruned launch of selected lines to visualization
        - User opens structure in Structure Manager/Multi Structure Manager/Manufacturing Process Planner, configures
        it, selects some lines, and sends those lines to Lifecycle Viewer or integrated standalone visualization
        - The launching client (system) calls 'createVisSCsFromBOMs' to record the selected lines and BOM configuration
        information
        - The visualization client receives the request to open the selected lines as an object reference to a
        VisStructureContext object
        - The visualization client calls the 'createBOMsFromRecipes' operation and passes the VisStructureContext
        object reference
        - The system creates a BOMWindow and configures it properly (to match launching configuration)
        - The client pulls the occurrence_list from the VisStructureContext object
        - The client issues an 'expandPSFromOccurrenceList' call to load the occurrences
        - The client(system) loads the selected occurrences in the visualization client, the structure is pruned to
        contain only those occurrences sent
        
        
        
        Product View launch to visualization
        - 1.    User selects a Product View in the Product View Gallery of embedded visualization inside Structure
        Manager/Multi Structure Manager/Manufacturing Process Planner, or in My Teamcenter and sends it to integrated
        standalone TcVis or Lifecycle Viewer
        - 2.    The visualization client receives the request to open the selected product View
        - 3.     The visualization client interrogates the Product View data model, fetches the files from the dataset,
        and gets a list of visible lines for the Product View
        - 4.    The client issues an 'expandPSFromOccurrenceList' call for all visible lines referenced by the Product
        View
        - 5.    The client loads the visible lines then applies the product view
        
        
        
        Use Case Dependencies: 
        The 'expandPSFormOccurrenceList' operation is called for existing parent BOMLines within a BOMWindow (i.e. the
        parent BOMLine(s) must already exist within a created BOMWindow) and also requires a previously
        captured/defined list of occurrences represented as a list of UID strings.
        
        The following services are used in conjunction with 'expandPSFromOccurrenceList' to complete the use cases
        above.
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'createVisSCsFromBOMs'
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'createBOMsFromRecipes'
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'areRecipesMergible'
        Teamcenter::Soa::Internal::Visualization::_2010_09::DataManagement. 'getSnapshot3DInfo'
        """
        return cls.execute_soa_method(
            method_name='expandPSFromOccurrenceList',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info, 'pref': pref},
            response_cls=ExpandPSFromOccurrenceListResponse,
        )

    @classmethod
    def areRecipesMergable(cls, info: List[AreRecipesMergableInfo]) -> AreRecipesMergableResponse:
        """
        This operation takes a list of configuration object/BOMWindow pairs and determines if their configuration
        recipes are equivalent. That is, the configuration of the BOMWindow is compared to the configuration recipe
        recorded in the configuration object. For the configurations to be considered equivalent the following must all
        be true:
        - The top line recorded in the configuration object must match the top line of the BOMWindow.
        - The RevisionRule recorded in the configuration object must be equivalent to the RevisionRule of the BOMWindow.
        - If the BOMWindow has variant options set on the top line then the configuration object must have the same
        variant option names and the option values must match those in the BOMWindow.
        - If the BOMWindow has an active assembly arrangement then the configuration object must have the same assembly
        arrangement object recorded.
        
        
        
        This service supports use cases involving the interoperation of selected BOMLines from the Teamcenter Rich
        Client to Teamcenter Visualization. The occurrences list of the configuration object records the selected
        BOMLines at the time of interoperation. The occurrences list is then be used in a later operation to populate a
        BOM Window with those same occurrences (see 'expandPSFromOccurrencesList' operation for more information). This
        operation is used to determine if the selected lines in the new interoperation request can be merged (opened
        within) an existing document in Teamcenter Visualization opened as a result of a previous interoperation.
        
        Use cases:
        A Teamcenter Visualization client has a configured BOMWindow from a previous interoperation with Teamcenter.
        That client then receives a new request to open a configuration object. The client may use this service to
        determine if the occurrences recorded in the new configuration object may be merged into its existing BOMWindow.
        The basic user flow where this service is utilized by visualization is as follows:
        - User opens Structure Manager/Multi Structure Manager/Manufacturing Process Planner, configures the structure,
        selects some lines, and sends those lines to Lifecycle Viewer or standalone Teamcenter Visualization.
        - The viewer client opens the structure, configures it as it was in the launching client, and then expands and
        loads the selected occurrences that were sent.
        - User goes back to Structure Manager/Multi Structure Manager/Manufacturing Process Planner client, selects a
        few more occurrences to also send and merge into the open structure inside visualization, and sends those lines
        to Lifecycle Viewer or standalone Teamcenter Visualization.
        - Visualization receives the merge request from the user, and the system calls the 'areRecipesMergible' service
        to determine if the specified occurrences can be merged into an already open window in the visualization
        client. If mergable, the visualization client merges the occurrences into an existing open structure.
        
        
        
        Use Case References: 
        There must be a previously existing configured BOM Window and an existing configuration object.
        
        The following services are used in conjunctions with areRecipesMergible to complete the use case above.
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'createVisSCsFromBOMs'
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'createBOMsFromRecipes'
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. 'expandPSFromOccurrenceList'
        """
        return cls.execute_soa_method(
            method_name='areRecipesMergable',
            library='Internal-Visualization',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=AreRecipesMergableResponse,
        )
