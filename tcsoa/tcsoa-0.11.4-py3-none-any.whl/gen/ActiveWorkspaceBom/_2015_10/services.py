from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0ProductContextInfo, Awb0SavedBookmark
from typing import List
from tcsoa.gen.ActiveWorkspaceBom._2015_10.OccurrenceManagementCad import SavedBookmarksBOMWindowsResponse, ProductContextBOMWindowResponse
from tcsoa.base import TcService


class OccurrenceManagementCadService(TcService):

    @classmethod
    def createBOMWindowsFromBookmarks(cls, savedBookmarks: List[Awb0SavedBookmark], expandToSelection: bool) -> SavedBookmarksBOMWindowsResponse:
        """
        This operation creates BOM windows (BOMWindow objects) from Active Workspace saved bookmarks (Awb0SavedBookmark
        objects).  A BOM window will be created for each product contained within each saved bookmark.  With each
        BOMwindow there will be a corresponding list of BOMLline objects that identify any selections included in the
        saved bookmark.  The product of the Awb0ProductContextInfo that is associated with each saved bookmark will be
        set as the top line of the BOMWindow.  The product contexts also contain information that will be set on the
        BOM window when it is created.  This information may include:
        
        - Revision rule
        - End item
        - Effective date
        - Effective unit
        - Saved Variant rule
        
        
        
        Use cases:
        The user has found a saved bookmark in the Active Context Experience.  The user wants to open the contents of
        the bookmark in the CAD application.  The Active Workspace Client communicates saved bookmark details to the
        CAD application, which then uses it as an input to this operation to create BOM windows.
        
        When BOMWindow objects are needed but only Awb0SavedBookmark objects are accessible, this operation will use
        the necessary information from the Awb0SavedBookmark objects to provide corresponding BOMWindow objects.
        """
        return cls.execute_soa_method(
            method_name='createBOMWindowsFromBookmarks',
            library='ActiveWorkspaceBom',
            service_date='2015_10',
            service_name='OccurrenceManagementCad',
            params={'savedBookmarks': savedBookmarks, 'expandToSelection': expandToSelection},
            response_cls=SavedBookmarksBOMWindowsResponse,
        )

    @classmethod
    def createBOMWindowsFromContexts(cls, productContextInfos: List[Awb0ProductContextInfo], expandToSelection: bool) -> ProductContextBOMWindowResponse:
        """
        This operation creates BOM windows (BOMWindow objects) from Active Workspace product contexts
        (Awb0ProductContextInfo objects).  One BOM window will be created for each product context.  The product of the
        Awb0ProductContextInfo will be set as the top line of the BOMWindow.  With each BOMWindow there will be a
        corresponding list of BOMLine objects that identify any selections included in the product context information.
         The product context contains configuration data that will be set on the BOM Window when it is created.  This
        information may include:
        
        - Revision rule
        - End item
        - Effective date
        - Effective unit
        - Saved Variant rule
        
        
        
        Use cases:
        The user opens an Item-BVR assembly in the Active Content Experience and makes changes to the RevisionRule or
        other configuration parameters.  Then, the user opens it in the CAD application.  The Active Workspace client
        communicates the Awb0ProductContextInfo to the CAD application, which then uses it as an input to this
        operation to create the BOMWindow.
        
        When BOMWindow objects are needed but only Awb0ProductContextInfo objects are accessible, this operation will
        use the necessary information from the Awb0ProductContextInfo objects to create corresponding BOMWindow objects.
        """
        return cls.execute_soa_method(
            method_name='createBOMWindowsFromContexts',
            library='ActiveWorkspaceBom',
            service_date='2015_10',
            service_name='OccurrenceManagementCad',
            params={'productContextInfos': productContextInfos, 'expandToSelection': expandToSelection},
            response_cls=ProductContextBOMWindowResponse,
        )
