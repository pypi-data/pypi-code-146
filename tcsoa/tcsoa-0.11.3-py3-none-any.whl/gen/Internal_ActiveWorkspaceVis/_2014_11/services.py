from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0ProductContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceVis._2014_11.OccurrenceManagement import SaveVisBookmarkInfoResponse, SaveVisBookmarkInput, GetVisBookmarkInfoResponse
from typing import List
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def getVisBookmarkInfo(cls, productContextInfos: List[Awb0ProductContextInfo]) -> GetVisBookmarkInfoResponse:
        """
        In order to take the user to the context where he left off, viewer state information (e.g. camera, occurrence
        visibility, etc.) are stored to the current Awb0AutoBookmark for the given Awb0ProductContextInfo.  This
        operation gets the visualization information associated to the  Awb0Autobookmark for the given
        Awb0ProductContextInfo.
        
        Use cases:
        The user searches for a product clicks on the viewer tab from the Active Content  Experience(ACE) location in
        Active Workspace.
        - A launch file(.vvi) containing the Awb0ProductContextInfo information gets created. This file is uploaded to
        the visualization server.
        - Viewer which is running in the visualization server reads this launch file and loads the occurrences for the
        given Awb0ProductContextInfo.
        - Viewer invokes 'getVisBookmarkInfo', downloads the file containing the visualization information using the
        read tickets returned in 'VisBookmarkInfoResponse', reads the file and sets the visualization state that would
        take the user back to where he left off.
        
        """
        return cls.execute_soa_method(
            method_name='getVisBookmarkInfo',
            library='Internal-ActiveWorkspaceVis',
            service_date='2014_11',
            service_name='OccurrenceManagement',
            params={'productContextInfos': productContextInfos},
            response_cls=GetVisBookmarkInfoResponse,
        )

    @classmethod
    def saveVisBookmarkInfo(cls, saveBookmarkInfos: List[SaveVisBookmarkInput]) -> SaveVisBookmarkInfoResponse:
        """
        When a user changes various visibility state (e.g. camera, occurrence visibility, etc) that state need to be
        saved/associated to a bookmark. This operation is used to associate the current visualization state information
        to the current Awb0AutoBookmark for the Awb0ProductContextInfo.
        
        Use cases:
        The user searches for a product clicks on the viewer tab from the Active Content  Experience(ACE) location in
        Active Workspace.
        - A launch file(.vvi) containing the Awb0ProductContextInfo gets created. This file is uploaded to the
        visualization server.
        - Viewer which is running in the visualization server reads this launch file and loads the occurrences for the
        given Awb0ProductContextInfo.
        - User changes occurrence visibility or camera angle, the viewer writes the changed information into a file. 
        - The file is now uploaded by viewer to the transient volume, invokes 'saveVisBookmarkInfo' to save the changed
        viewer information as ImanFile object and associate it to the current Awb0AutoBookmark for the
        Awb0ProductContextInfo.
        
        """
        return cls.execute_soa_method(
            method_name='saveVisBookmarkInfo',
            library='Internal-ActiveWorkspaceVis',
            service_date='2014_11',
            service_name='OccurrenceManagement',
            params={'saveBookmarkInfos': saveBookmarkInfos},
            response_cls=SaveVisBookmarkInfoResponse,
        )
