from __future__ import annotations

from tcsoa.gen.Internal.Visualization._2010_04.DataManagement import GatherUserAgentDataInfo, GatherInputInfo, GatherServerInfo, GatherResponse, GatherSessionInfo
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def gatherMarkups(cls, selectedInputInfos: List[GatherInputInfo], serverInfo: GatherServerInfo, sessionInfo: GatherSessionInfo, userDataAgentInfo: GatherUserAgentDataInfo) -> GatherResponse:
        """
        This operation finds and retrieves all markup objects related to the object of interest.  It creates a list of
        GatherResponse structure (containing Item uid, Item name, ItemRevision uid, ItemRevision name, Dataset uid,
        Dataset name, Dataset named reference, related markup Dataset uid, related markup Dataset name, related markup
        Dataset named reference, markup tool preferences, related control WorkspaceObject, and additional information
        in form of key value pair strings) based on the list of GatherInputInfo input structure (containing
        WorkspaceObject, related Item, related ItemRevision, related control WorkspaceObject, and additional
        information in the form of key value pair strings), structure of server information GatherServerInfo from where
        the operation is initiated, structure of the session information GatherSessionInfo of the client from where the
        operation is initiated, and structure of client information GatherUserAgentDataInfo from where the operation is
        initiated.
        The required input data from the GatherInputInfo structure is any WorkspaceObject (normally this input is the
        subtype of WorkspaceObject such as Item or Item Revision or Dataset) for which the user wishes to gather all
        the related markup objects.    The input structures for server, session, and client information can be empty.  
        If they are available, only server information will be passed back as part of additional information in the sub
        structure GatherBasedDatasetInfo inside the key value pair string DataSegment.
        
        
        Use cases:
        Use Case1: Retrieve markup information for MSWordX dataset
        From the Teamcenter client for Microsoft Office Word, when a user opens a WordX Dataset and clicks the Markup
        button from the Teamcenter ribbon, internally, the client initiates the gatherMarkups operation to retrieve
        markup related information.  When the operation completes and returns the data back to the client, the client
        will process this data and display the markup information in the Markup window pane.
        
        Use Case 2: Visualization
        The viewer integrations have the need to gather up all markup objects related to a given object for display in
        the viewer.  An Item, ItemRevision, or dataset is the typical input object, and the return is a list of markup
        datasets that are related.  The server can choose to filter the return based on certain business logic such as
        user access control rights.  For example, it may not be desireable to allow users that do not own the markup
        actually edit it, so these types of controls can be imposed by this service.  A typical use case is as follows:
        1.    Visualization user locates an object that contains a base image (e.g. the ItemRevision representing a
        part with a drawing attached to it) in the PLM client
        2.    The user launches the base image control object to visualization
        3.    The user can control whether or not to Open with markups, depending on how their load preferences are
        setup.  Assume the open with markups behavior is desired for the remainder of this use case.
        4.    The system calls the gatherMarkups service to find all markups related to the base image object of
        interest.
        5.    The gatherMarkups service imposes the appropriate business rules while gathering the related markup
        objects, and returns the appropriate markup datasets that the user should be able to see to the client
        6.    The visualization client opens the base image and the related markup layers, and enables the appropriate
        level of functionality (such as the markup entity controls if the user has edit access).
        """
        return cls.execute_soa_method(
            method_name='gatherMarkups',
            library='Internal-Visualization',
            service_date='2010_04',
            service_name='DataManagement',
            params={'selectedInputInfos': selectedInputInfos, 'serverInfo': serverInfo, 'sessionInfo': sessionInfo, 'userDataAgentInfo': userDataAgentInfo},
            response_cls=GatherResponse,
        )
