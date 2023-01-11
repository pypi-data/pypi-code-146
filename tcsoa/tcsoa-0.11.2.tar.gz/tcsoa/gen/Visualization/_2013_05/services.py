from __future__ import annotations

from tcsoa.gen.Visualization._2011_02.StructureManagement import CreateVisSCsFromBOMsInfo, CreateVisSCsFromBOMsResponse
from tcsoa.gen.Visualization._2013_05.DataManagement import LaunchInfoResponse, SessionInfo2, IdInfo2
from typing import List
from tcsoa.gen.Visualization._2013_05.StructureManagement import OptionKeyToOptionValueMap
from tcsoa.gen.Visualization._2011_02.DataManagement import UserAgentDataInfo, ServerInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createLaunchInfo(cls, idInfos: List[IdInfo2], serverInfo: ServerInfo, userDataAgentInfo: UserAgentDataInfo, sessionInfo: SessionInfo2) -> LaunchInfoResponse:
        """
        This service generates a VVI file which is used to launch Teamcenter Visualization viewers with selected
        objects from Teamcenter and preserve a two way communication link between the viewer and the server.  This
        operation can return the VVI type information as a string buffer or as a read file ticket to a vvi/vfz file in
        the FMS transient file volume.
        NOTE: VVI and VFZ files are not intended to be persisted and should be generated with each launch of
        visualization. For example, the VVI format is not guaranteed to be supported if the server or viewer is
        updated. VFZ files are used if more than one object is launched at a time, while VVI files are used for single
        objects.
        The client can retrieve the VVI/VFZ launch file information via string buffer or through the transient file
        volume. This is controlled by setting the hasTransientVolume flag of the SessionInfo2 input structure.  With
        the hasTransientVolume flag set to false, the launch info returns a vvi string buffer for each launch object or
        as a stream of vvi string buffers for multiple launch objects.  Using the API in this way can avoid setup and
        use of the FMS system directly by the calling client.  It is the responsibility of the client to decipher the
        response data structure.  For example, the vvi string buffer(s) can be written out as a vvi or vfz file on the
        client and passed to visualization, or the string buffer can be passed directly to embedded visualization if
        using the PLMVis toolkit.  With the hasTransientVolume flag set to true, the operation requires the Teamcenter
        File Management System (FMS) to be installed (including FCC and transient volumes) for retrieval of the VVI
        file from the transient file volume. This operation generates the launch file (VFZ or VVI), stores it in the
        FMS transient volume, and returns the FMS ticket. The client that initiated this operation is responsible for
        downloading the transient file (VVI or VFZ) with the transient ticket from transient volume to a local file
        system. The transient (VVI or VFZ) file is consumed by the Teamcenter Visualization client. The viewer will
        then establish the server connection and load the object(s) specified in the VVI file.  Launch on multiple
        objects will generate a VFZ file (zip of all the vvi files) and transient ticket of VFZ file would be sent to
        client.
        This service supports launch on Teamcenter persistent objects like Dataset, Item, ItemRevision,
        BOMViewRevision, BOMView. It also supports launch of selected BOMLines of a configured structure from Structure
        Manager or BOPLines from Manufacturing Process Planner, but in this case the caller must first create a
        VisStructureContext object. Valid launch object types and behavior such as priority order can be configured
        with the Teamcenter Preferences VMU_Datasets, VMU_FileSearchOrder and VMU_RelationSearchOrder.
        """
        return cls.execute_soa_method(
            method_name='createLaunchInfo',
            library='Visualization',
            service_date='2013_05',
            service_name='DataManagement',
            params={'idInfos': idInfos, 'serverInfo': serverInfo, 'userDataAgentInfo': userDataAgentInfo, 'sessionInfo': sessionInfo},
            response_cls=LaunchInfoResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def createVisSCsFromBOMs(cls, info: List[CreateVisSCsFromBOMsInfo], options: OptionKeyToOptionValueMap) -> CreateVisSCsFromBOMsResponse:
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
        with the same configuration recipe and the recorded UID occurrence chains would be used to populate/expand the
        constructed BOMWindow with specific BOMLines. For example, this operation is used when sending selected
        BOMLines from the Structure Manager to Teamcenter Visualization and also to capture the configuration recipe
        for storage in Vis Sessions.
        
        Visualization pruned launch use case
        - User opens a structure in Structure Manager (SM)/Multi Structure Manager (MSM)/Manufacturing Process Planner
        (MPP), and configures it
        - User selects some lines they want to send to visualization as a pruned structure
        - System calls createVisSCsFromBOMs to record the selected lines and the configuration of the BOM to send
        
        
        
        Visualization session save use case
        - 1.    User performs Visualization pruned launch use case and loads occurrences into visualization
        - 2.    User creates some authored visualization content (e.g. snapshots, motions, etc)
        - 3.    User saves session to Teamcenter
        - 4.    System calls createRecipesFromBOMs operation to capture the configuration and any pruning information
        as a VisStructureContext object.  UID of object returned.
        - 5.    System writes the VisStructureContext object reference into the visualization session data
        - 6.    System saves the visualiation session dataset to Teamcenter, and relates it to the VisStructureContext
        object created by the service
        
        
        
        Visualization Technical Illustration and 3D Markup save use cases
        Similar to session save use case, except saving a different data type.  Uses this service to create the recipe
        for the authored visualization data in the Teamcenter data model.
        
        Use Case Dependencies: 
        The createVisSCsFromBOMs operation is called with input BOMLines from an existing BOM Window. Therefore, the
        BOMWindow must have already been created and populated with at least a top line.
        """
        return cls.execute_soa_method(
            method_name='createVisSCsFromBOMs',
            library='Visualization',
            service_date='2013_05',
            service_name='StructureManagement',
            params={'info': info, 'options': options},
            response_cls=CreateVisSCsFromBOMsResponse,
        )
