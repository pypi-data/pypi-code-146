from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Internal.ActiveWorkspaceBom._2020_05.OccurrenceManagement import UpdateContentBasedOnRevInput, UpdateWorkingContextInput
from tcsoa.gen.BusinessObjects import WorkspaceObject


class OccurrenceManagementService(TcService):

    @classmethod
    def saveWorkingContext(cls, workingContexts: List[WorkspaceObject]) -> ServiceData:
        """
        The operation provides capability to save pending changes to working contexts e.g. Fnd0AppSession or
        Awb0SavedBookmark for Active Workspace. The configuration and recipe are extracted from Awb0AutoBookmark of
        Working Context.
        """
        return cls.execute_soa_method(
            method_name='saveWorkingContext',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_05',
            service_name='OccurrenceManagement',
            params={'workingContexts': workingContexts},
            response_cls=ServiceData,
        )

    @classmethod
    def updateContentBasedOnRevision(cls, input: UpdateContentBasedOnRevInput) -> ServiceData:
        """
        This operation reconfigures and updates content for impacted occurrence of input WorkspaceObject. As the
        operation is invoked for loaded structure, Awb0Element objects are already created and cached in business
        object registry for opened structure. This operation makes use of BOM event listener mechanism and retrieves
        Awb0Element for corresponding WorkspaceObject from business object registry's cache. The Awb0Element object
        which represents configured revision is returned in ServiceData as updated object. As structure can have
        multiple occurrences configured for input WorkspaceObject, one or more Awb0Element objects may be returned in
        ServiceData.
        """
        return cls.execute_soa_method(
            method_name='updateContentBasedOnRevision',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_05',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def updateWorkingContext(cls, input: List[UpdateWorkingContextInput]) -> ServiceData:
        """
        The operation creates and updates the configuration and recipe on a Fnd0StructureContextData object under the
        Fnd0AppSession of Fnd0TempAppSession working context.
        
        Use cases:
        Case 1: User creates Fnd0AppSession from configured BOM Structure
        User configures structure by applying configuration and recipe. The configured structure is used to create new
        Working Context of type Fnd0AppSession. The operation createRelateAndSubmitObjects is called which creates
        Fnd0AppSession object. Upon successful creation of Fnd0AppSession Active Workspace creates and attaches
        Fnd0StructureContextData. The configuration and recipe of source structure is extracted from Awb0AutoBookmark
        and persisted on newly created Session.
        
        Case 2: User performs SaveAs operation on Fnd0AppSession
        User updated configuration and recipe of Fnd0AppSession. The changes are not automatically persisted to
        Fnd0AppSession but updated in Awb0AutoBookmark associated with Fnd0AppSession. Now user performs SaveAs
        operation on opened Fnd0AppSession.
        saveAsObjectsAndRelate uses deep copy rules to create new copy of Fnd0AppSession. Once new copy of
        Fnd0AppSession is created we have to update configuration and recipe on new copy using unsaved changes to
        original Fnd0AppSession on which SaveAs action was performed.
        """
        return cls.execute_soa_method(
            method_name='updateWorkingContext',
            library='Internal-ActiveWorkspaceBom',
            service_date='2020_05',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ServiceData,
        )
