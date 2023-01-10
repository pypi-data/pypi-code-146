from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Core._2012_02.DataManagement import GetViewableDataResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getViewableData(cls, input: List[BusinessObject], configuredViewerIDs: List[str], viewerConfigKey: str) -> GetViewableDataResponse:
        """
        This operation returns the Teamcenter objects, and/or files that may be viewed for each input object.  The
        Teamcenter objects and files that are returned are based on the input object, the optional list of configured
        viewer IDs that are defined in the client, and the rules defined in the defaultViewerConfig.VIEWERCONFIG and
        <viewer config ID>.VIEWERCONFIG preferences. 
        
        - The optional list of configured viewer IDs - This is a list of IDs that uniquely identify a viewer that is
        installed/enabled in the client.  For example, in the rich client there is a viewer that is registered to the
        "MSWordViewer" ID. This viewer renders MSWord files but is only enabled on the Windows platform.  So, when
        running the rich client on Windows, "MSWordViewer" would be in the list of configured viewer IDs, but on Unix
        it would not be in the list, since MSWord isn't supported on Unix.   By giving this listing to the operation,
        only the rules that are legal for the input list of viewer IDs are processed.  If no list is provided, then all
        the rules are processed, and it's up to the client to determine how to handle the data.
        
        
        
        -  For information related to the defaultViewerConfig.VIEWERCONFIG preference, please see the My Teamcenter
        Guide or the Preferences and Environment Variables Reference.
        
        
        
        Common uses for this operation would be to retrieve viewable data for a selected object in the UI in order to
        present the viewable data in the UI.  
        
        For example, the rules may state that when an ItemRevision object is selected, and an MSWord dataset and JT
        dataset are related to that ItemRevision object, the viewable data should be the JT dataset. 
        
        Alternatively, the rules may be configured such that the ItemRevision object itself is viewable, and in that
        case, only the ItemRevision object is returned.
        
        Exceptions:
        >Thrown if the defaultViewerConfig.VIEWERCONFIG  (or the <viewer config id>.VIEWERCONFIG) preference may not be
        loaded in order to process viewable data.  These cases are:
        - 263001 - The viewer configuration preference  does not exist.  Please add it.
        - 263002 - The viewer configuration preference  has no value.  Please add one.
        - 263003 -The viewer configuration preference  is malformed.  Please correct.
        
        """
        return cls.execute_soa_method(
            method_name='getViewableData',
            library='Internal-Core',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input, 'configuredViewerIDs': configuredViewerIDs, 'viewerConfigKey': viewerConfigKey},
            response_cls=GetViewableDataResponse,
        )
