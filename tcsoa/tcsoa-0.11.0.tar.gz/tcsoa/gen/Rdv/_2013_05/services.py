from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Rdv._2013_05.ContextManagement import ContextObjectResponse
from typing import List
from tcsoa.base import TcService


class ContextManagementService(TcService):

    @classmethod
    def getRelatedObjectsInContext(cls, objectList: List[BusinessObject]) -> ContextObjectResponse:
        """
        This operation finds all the business objects that are within the current active context of the list of objects
        sent as input. The objects within context are objects of the types specified below that are related to the
        input object either through reference or relation.
        - Items
        - Processes
        - ChangeRequestRevision
        - StructureContext
        - AppearanceGroup
        
        
        
        
        The RDV module maintains a state that defines the currently active context. A combination of one or more of the
        following objects defines the current active context.
        - WorkpartItem
        - Process
        - ChangeRequestRevision
        - ConfigurationContext
        - StructureContext
        - AppearanceGroup
        
        
        
        
        Every time this operation is invoked, the objects in the current context are refreshed.
        This operation is mainly used for adding work parts, EngChange revisions and processes to the Design Context
        application.
        The following criteria is used to determine the objects related to the inputs:
        
        1) Item objects that are attached with the ChangeRequestRevision, Process objects through the relation type
        mentioned in the preferences listed below.
        
        'PortalDesignContextProcess.WorkPartOrChangeAttachmentTypes'
        'PortalDesignContextECObject.WorkPartRelationships'
        
        
        2) Item objects that are associated with the EPM job where the input object is also a part of the EPM job.
        
        3) Item objects that are part of the same ConfigurationContext object, StructureContext object or an
        AppearanceGroup object as that of the input objects.
        
        Use cases:
        Use Case 1: If user enters an item ID in the WorkParts text field in DesignContext application. The Design
        Context application uses this operation to display the item revision in the WorkParts list, and any changes or
        processes that reference the item revision in the EngChange Revision and Processes lists.
        
        Use Case 2: If user enters a change ID in the EngChange Revision text field DesignContext application. The
        DesignContext application uses this operation to add the change object to the EngChange Revision list, and any
        item revisions or processes referenced by the change object are displayed in the WorkParts and Processes lists.
        If the change references revisions of Product Items, Teamcenter automatically adds them to the Selected Product
        Context list.
        
        Use Case 3: If user enters a process name in Processes test field DesignContext application. The DesignContext
        application uses this operation to add the process object to the Processes list, and any objects targeted by
        the process are displayed in the WorkParts and EngChange lists.
        
        The items in the WorkPart lists can then be selected by the user for carrying out the design validation
        analysis.
        """
        return cls.execute_soa_method(
            method_name='getRelatedObjectsInContext',
            library='Rdv',
            service_date='2013_05',
            service_name='ContextManagement',
            params={'objectList': objectList},
            response_cls=ContextObjectResponse,
        )
