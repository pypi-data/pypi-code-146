from __future__ import annotations

from tcsoa.gen.ActiveWorkspaceVis._2015_03.DataManagement import SessionInfo, UserAgentDataInfo, IdInfo, ServerInfo, LaunchInfoResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createLaunchInfo(cls, idInfos: List[IdInfo], serverInfo: ServerInfo, userDataAgentInfo: UserAgentDataInfo, sessionInfo: SessionInfo) -> LaunchInfoResponse:
        """
        This service operation is an extension to the service operation with the same name located in the
        DataManagement Interface of the Visualization service library. This extension allows the support of launching
        ActiveWorkspace specific objects such as Awb0Element and Awb0ProductContextInfo.
        
        This service generates a VVI information which is used to launch Teamcenter Visualization viewers with selected
        objects from Teamcenter and preserve a two way communication link between the viewer and the server.  This
        operation can return the VVI information as a string buffer or as a read file ticket to a vvi/vfz file in the
        FMS transient file volume. The "UseTransientVolume" option passed into the service via the Idinfo structure
        controls how the VVI launch information is returned.
        
        Obtaining the launch information as a string might be usefule to avoid setup and use of the FMS system directly
        by the calling client.  It is the responsibility of the client to determine how to use the returned string
        buffer.  For example, the vvi string buffer(s) can be written out as a vvi or vfz file on the client and passed
        to visualization, or the string buffer can be passed directly to embedded visualization if using the PLMVis
        toolkit.  
        
        If returning the launch information as a FMS transient file ticket then the operation requires the Teamcenter
        File Management System (FMS) to be installed (including FCC and transient volumes) in order to retrieve the VVI
        file from the transient file volume. When operating in this mode, the operation generates the launch file (VFZ
        or VVI), stores it in the FMS transient volume, and returns the FMS ticket. The client that initiated this
        operation is responsible for downloading the transient file (VVI or VFZ) from the transient volume to a local
        file system using the transient ticket. The transient (VVI or VFZ) file is consumed by the Teamcenter
        Visualization client. The viewer establishs a server connection and loads the object(s) specified in the VVI
        file.  Launch on multiple objects will generate a VFZ file (zip of all the vvi files) and transient ticket of
        VFZ file would be sent to client.
        
        NOTE: VVI and VFZ files are not intended to be persisted and should be generated with each launch to Teamcenter
        Visualization. For example, the VVI format is not guaranteed to be supported if the server or viewer is
        updated. VFZ files are used if more than one object is launched at a time, while VVI files are used for single
        objects.
        
        As with the previous createLaunchInfo service operation located in the Visualization library, this service
        supports launch on Teamcenter persistent objects like Dataset, Item, ItemRevision, BOMViewRevision, BOMView. It
        also supports launch of selected BOMLines of a configured structure from Structure Manager or BOPLines from
        Manufacturing Process Planner, but in this case the caller must first create a VisStructureContext object and
        make it the launched object. However with this operation you may also launch objects of type Awb0Element and
        Awb0ProductContextInfo. See description of IdInfo for details.
        
        Valid launch object types and behavior such as priority order can be configured with the Teamcenter Preferences
        VMU_Datasets, VMU_FileSearchOrder and VMU_RelationSearchOrder.
        
        Use cases:
        This operation supports the mechanism of visualizing Teamcenter specific objects in Teamcenter Visualization
        client.
        """
        return cls.execute_soa_method(
            method_name='createLaunchInfo',
            library='ActiveWorkspaceVis',
            service_date='2015_03',
            service_name='DataManagement',
            params={'idInfos': idInfos, 'serverInfo': serverInfo, 'userDataAgentInfo': userDataAgentInfo, 'sessionInfo': sessionInfo},
            response_cls=LaunchInfoResponse,
        )
