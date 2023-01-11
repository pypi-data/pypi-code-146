from __future__ import annotations

from tcsoa.gen.Visualization._2011_02.StructureManagement import CreateVisSCsFromBOMsInfo, CreateVisSCInfo, CreateVisSCsFromBOMsResponse, CreateVisSCResponse
from tcsoa.gen.Visualization._2011_02.DataManagement import SessionInfo, UserAgentDataInfo, IdInfo, ServerInfo, VVITicketsResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createLaunchFile(cls, idInfos: List[IdInfo], serverInfo: ServerInfo, userDataAgentInfo: UserAgentDataInfo, sessionInfo: SessionInfo) -> VVITicketsResponse:
        """
        This service generates a VVI file which is used to launch Teamcenter Visualization viewers with selected
        objects from Teamcenter and preserve a two way communication link between the viewer and the server.  These
        files are not intended to be permanent and should be generated with each launch.  For example, the VVI format
        is not guaranteed to be supported if the server or viewer is updated.  VFZ files are used if more than one
        object is launched at a time.
        
        This operation requires the Teamcenter File Management System (FMS) to be installed (including FCC and
        transient volumes) for retrieval of the VVI file from the transient file volume.  This operation generates the
        launch file (VFZ or VVI), stores it in the FMS transient volume, and returns the FMS ticket.  The client that
        initiated this operation is responsible for downloading the transient file (VVI or VFZ) with the transient
        ticket from transient volume to a local file system. Transient (VVI or VFZ) file is then consumed by the
        Teamcenter Visualization client.  The viewer will then establish the server connection and load the object(s)
        specified in the VVI file.  Launch on multiple objects will generate a VFZ file (zip of all the vvi files) and
        transient ticket of VFZ file would be sent to client. 
        
        This service supports launch on Teamcenter persistent objects like Dataset, Item, ItemRevision,
        BOMViewRevision, BOMView. It also supports launch of selected BOMLines of a configured structure from Structure
        Manager or BOPLines from Manufacturing Process Planner, but in this case the caller must first create a
        VisStructureContext object (See Dependency section for operation to use).  Valid launch object types and
        behavior such as priority order can be configured with the Teamcenter Preferences VMU_Datasets,
        VMU_FileSearchOrder and VMU_RelationSearchOrder.
        
        
        Use cases:
        This operation supports the mechanism of visualizing Teamcenter specific objects in Teamcenter Visualization
        client. There are several steps to support this mechanism.
        
        1.    The client application that initiates the launch will provide:
        
        A vector of IdInfo objects that contains one or more pieces of information about Teamcenter objects that needs
        to be visualized in the viewer (e.g., If Dataset is launched, then information about its Item, ItemRevision and
        type of operation, including any additional information can be provided). Note: In case launch of Teamcenter
        runtime objects like BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner, it is the
        responsibility of the client to create VisStructureContext object and provide VisStructureContext as the object
        to be laud (See Dependency section for operation to use).
        SessionInfo object contains session relevant information for Teamcenter Visualization to connect to the session
        (e.g., session discriminator and any other additional session relevant key value pair)
        ServerInfo object contains server information for Teamcenter Visualization to connect to the server. (e.g.,
        protocol, server URL, connection mode of the server and any other additional server relevant key value pair)
        UserAgentDataInfo object contains client application information who initiated the launch. (e.g., application
        name, application version, and any other additional client application relevant key value pair).
        
        
        2.    After gathering the necessary information as listed in step 1, client application then invokes the
        'DataManagementService::createLaunchFile' operation to obtain an FMS read ticket for the launch file (VVI or
        VFZ), that has relevant information for visualizing Teamcenter persistent or runtime objects.
        
        See the Dependencies section below for details.
        
        3.    Use a File Management System (FMS) Application Programmatic Interface (API) to download the transient
        file (VVI or VFZ) from transient volume.
        
        Check the documentation for each API to determine how to react to download failures.
        
        Use Case References:
        This operation is used in conjunction with other 'FileManagementService' service operations, 'Visualization'
        service operations, FccProxy and the FileManagementUtility. Please consult the documentation for each of these
        available operations for details on the requirements, usage, and environments in which they should be used. 
        
        Visualization operations for creating the VisStructureContext from clients that initiate the launch of
        Teamcenter runtime objects like BOMLines from Structure Manager or BOPLines from Manufacturing Process Planner.
        
        'Teamcenter::Soa::Internal::Visualization::_2011_02:: StructureManagement::CreateVisSCsFromBOMsResponse
        createVisSCsFromBOMs' 
        
        """
        return cls.execute_soa_method(
            method_name='createLaunchFile',
            library='Visualization',
            service_date='2011_02',
            service_name='DataManagement',
            params={'idInfos': idInfos, 'serverInfo': serverInfo, 'userDataAgentInfo': userDataAgentInfo, 'sessionInfo': sessionInfo},
            response_cls=VVITicketsResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def createVisSC(cls, info: List[CreateVisSCInfo]) -> CreateVisSCResponse:
        """
        This operation takes a list of ConfigurationContext/top line object pairs and creates a VisStructureContext
        object based on that input. The user may optionally supply a list of occurrences in the form of UID chains and
        a file reference for the static PLMXML representation of the configuration. If an occurrence list or a static
        structure file are supplied they will be set as properties on the VisStructureContext object. The list of
        occurrences can be used to populate/expand any BOMWindows that are subsequently created using the output
        VisStructureContext object.
        
        Use cases:
        When the user desires to create a single persistent object that records a particular configuration recipe and
        the caller already has the component objects that make up the configuration. This case might occur if the
        configuration elements of a BOMWindow were captured but the BOMWindow was then deleted. This is often the case
        when using the Teamcenter Thin Client.
        
        
        The createVisSC operation requires input configuration objects and their top lines. Therefore, these objects
        must have been obtained based on some previous configuration scenario.
        """
        return cls.execute_soa_method(
            method_name='createVisSC',
            library='Visualization',
            service_date='2011_02',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateVisSCResponse,
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
        later operations to populate/expand a BOMWindow with those same occurrences.
        
        Use cases:
        When the user desires to create a persistent object that records the configuration recipe of a particular
        BOMWindow. The resulting VisStructureContext object would assumedly be used to later reconstruct a BOMWindow
        with the same configuration recipe and the recorded occurrence chains would be used to populate/expand the
        constructed BOMWindow with specific BOMLines. For example, this operation is used when sending selected
        BOMLines from the Structure Manager to Teamcenter Visualization and also to capture the configuration recipe
        for storage in Vis Sessions.
        
        Visualization pruned launch use case
        - User opens a structure in Structure Manager (SM)/Multi Structure Manager (MSM)/Manufacturing Process Planner
        (MPP), and configures it
        - User selects some lines they want to send to visualization as a pruned structure
        - System calls createVisSCsFromBOMs to record the selected lines and the configuration of the BOM to send
        
        
        
        The createVisSCsFromBOMs operation is called with input BOMLines from an existing BOMWindow. Therefore, the
        BOMWindow must have already been created and populated with at least a top line.
        """
        return cls.execute_soa_method(
            method_name='createVisSCsFromBOMs',
            library='Visualization',
            service_date='2011_02',
            service_name='StructureManagement',
            params={'info': info},
            response_cls=CreateVisSCsFromBOMsResponse,
        )
