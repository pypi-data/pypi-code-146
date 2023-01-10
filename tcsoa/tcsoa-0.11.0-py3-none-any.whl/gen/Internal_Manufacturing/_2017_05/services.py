from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Manufacturing._2017_05.DataManagement import GetFutureRevisionsResponse, GetFutureRevisionsIn
from typing import List
from tcsoa.gen.Internal.Manufacturing._2017_05.ImportExport import NamesAndValuesMapAsync
from tcsoa.gen.Internal.Manufacturing._2017_05.StructureManagement import SyncMasterAndAlternativeInputInfo, SyncMasterAndAlternativeResponse
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importFromBriefcaseAsync(cls, fmsTicket: str, optionSetTag: BusinessObject, optionNamesAndValues: NamesAndValuesMapAsync, sessionOptionAndValues: NamesAndValuesMapAsync) -> None:
        """
        This operation is applicable specifically for Manufacturing Process Planner MPP application.
        This operation performs following operation
        Teamcenter::Soa::GlobalMultiSite::_2008_06::ImportExport importObjectsFromOfflinePackage 
        This is asynchronous implementation for the Teamcenter::Soa::Manufacturing::_2017_05::ImportExport
        importFromBriefcase service operation.
        
        Use cases:
        Use Case 1: Importing objects from briefcase asynchronously
        This operation can be used in Manufacturing Process Planner (MPP) application to import Briefcase file into
        Teamcenter in the background. For this operation to be invoked, user has to select the option import in
        background present in import dialog.  Briefcase file is a zipped file containing TC XML and data set files. The
        TC XML file specifies the object to be imported. The import dialog presents various option sets to control the
        objects during import.
        """
        return cls.execute_soa_method(
            method_name='importFromBriefcaseAsync',
            library='Internal-Manufacturing',
            service_date='2017_05',
            service_name='ImportExport',
            params={'fmsTicket': fmsTicket, 'optionSetTag': optionSetTag, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionAndValues': sessionOptionAndValues},
            response_cls=None,
        )

    @classmethod
    def exportToBriefcaseAsync(cls, reason: str, sites: List[BusinessObject], objects: List[BusinessObject], transferOptionSet: BusinessObject, optionNameAndValues: NamesAndValuesMapAsync, sessionOptionNamesAndValues: NamesAndValuesMapAsync) -> None:
        """
        This operation is applicable specifically for Manufacturing Process Planner MPP application.
        This operation performs following operation
        Teamcenter::Soa::GlobalMultiSite::_2008_06::ImportExport exportObjectsToOfflinePackage 
        In addition, it creates internal objects which are helpful in supplier collaboration use cases for
        manufacturing objects. This is asynchronous implementation for the
        Teamcenter::Soa::Manufacturing::_2016_03::ImportExport exportToBriefcase service operation.
        
        Use cases:
        Use Case 1: Exporting objects to the briefcase asynchronously by transferring the ownership to the supplier.
        User wants to export Collaboration Context (CC) object in MPP to the briefcase to be used by the supplier at
        remote site. 
        The CC may contain product structure(s), bill of processes (BOP) such as plant BOP, plant structure etc.
        While exporting, the user wants to transfer ownership of few objects in the CC to the supplier so that the
        supplier can make changes to those objects on the other site.
        A user selects the CC and uses the menu option Tools, Export To, Briefcase...
        Menu option opens a dialog that allows user to set a destination site, a transfer option set, a list of
        traverse options and a list of session options. User has to select export in background option present in
        export dialog for invoking this operation.
        In this case, all the objects which can be traversed by the transfer option set and session options will be
        exported into an output TC XML file. 
        The files and datasets related to exported objects will be downloaded and packed into the briefcase file along
        with the TC XML file.
        
        In addition, the internal object, Appearance Path Node (APN) will be created for the identified BOMLine objects
        in the CC. The BOMLine objects are identified based on the preference MERuleForBriefcaseExport.
        """
        return cls.execute_soa_method(
            method_name='exportToBriefcaseAsync',
            library='Internal-Manufacturing',
            service_date='2017_05',
            service_name='ImportExport',
            params={'reason': reason, 'sites': sites, 'objects': objects, 'transferOptionSet': transferOptionSet, 'optionNameAndValues': optionNameAndValues, 'sessionOptionNamesAndValues': sessionOptionNamesAndValues},
            response_cls=None,
        )


class StructureManagementService(TcService):

    @classmethod
    def syncMasterAndAlternative(cls, syncMasterAndAlternativeInputInfo: SyncMasterAndAlternativeInputInfo) -> SyncMasterAndAlternativeResponse:
        """
        This service operation synchronizes the source and target Collaboration Context (CC). Source and target can be
        either master CC or Alternative (CC with clone structures).Any newly available Study in source CC is
        synchronized with the target CC. During synchronization a new Study is created in target CC. Also, new
        operations in Plant BOP of source CC is synchronized with the Plant BOP of target CC.
        
        Use cases:
        An Alternative is created by cloning Plant Bill Of Process (BOP) and/or Plant structure from the master CC.
        - Use Case 1: User can create a Shared or Isolated Study using a Plant BOP from Alternative, select the
        Alternative in the CC tree view and use the synchronize command from context menu to synchronize the master CC
        with the selected Alternative. As a result a new Study is created in master CC.Based on whether equivalent
        object from source Study is available in Plant BOP of master CC, the object in the newly created Study is
        either copied or cloned from Plant BOP of master CC. If newly created Study is a Isolated Study, then objects
        are always cloned.
        - Use Case 2: User can create new opertaion(s) in Alternative Plant BOP, select the newly added operation(s)
        and use synchronize command to synchronize the master CC Plant BOP. As a result the new operation(s) are
        created in master CC Plant BOP.
        
        """
        return cls.execute_soa_method(
            method_name='syncMasterAndAlternative',
            library='Internal-Manufacturing',
            service_date='2017_05',
            service_name='StructureManagement',
            params={'syncMasterAndAlternativeInputInfo': syncMasterAndAlternativeInputInfo},
            response_cls=SyncMasterAndAlternativeResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def getFutureRevisions(cls, input: List[GetFutureRevisionsIn]) -> GetFutureRevisionsResponse:
        """
        This operation finds future revisions of the revision configured in by the input BOMLine based on the current
        RevisionRule. If the input BOMLine is Mfg0BvrProcess  subtype, it also finds the future revisions of its direct
        children which are of type Mfg0BvrProcess or Mfg0BvrOperation.  For input BOMLine objects not of Mfg0BvrProcess
        type this operation only finds the future revisions for the input line. The future revisions are found based on
        the current RevisionRule date or unit Effectivity. This operation finds future revisions by advancing the
        RevisionRule object&rsquo;s effectivity and looking for new revisions that would be configured in during that
        effectivity interval. The RevisionRule must have either a unit or date Effectivity clause and at least one
        &lsquo;Has Status&rsquo; clause which is configured by effective date or unit.  When using unit effectivity,
        the future revisions&rsquo; end item must match the current RevisionRule end item in order to be considered.
        Currently, multi-unit effectivity is not supported
        
        Use cases:
        Rev Rule: Has Status(Pending, Configured using Unit number).  End item 1.
        Rev A &ndash; Pending 1 &amp;UP, end item 1
        Rev B &ndash; Pending 5-10, end item 1
        Rev C &ndash; Pending 22-23, end item 1
        Revision Rule Unit Effectivity: 5 &ndash; Rev B configured
        
        Current Revision    Future Revisions &hellip;
             5                           11    22    24
             B                           A     C     A
        
        In this use case, this operation will return the following :
        Current Revision B
           Configuring Pending
              Configuring Effectivity 
                 Range:5-10
                 Transition Effectivity:5
        Future Revision A
           Configuring Pending
              Configuring Effectivity 
                 Range:1 &ndash; UP
                 Transition Effectivity:11,24
        Future Revision C
           Configuring Pending
              Configuring Effectivity 
                 Range:22 &ndash; 23
                 Transition Effectivity:22
        """
        return cls.execute_soa_method(
            method_name='getFutureRevisions',
            library='Internal-Manufacturing',
            service_date='2017_05',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetFutureRevisionsResponse,
        )
