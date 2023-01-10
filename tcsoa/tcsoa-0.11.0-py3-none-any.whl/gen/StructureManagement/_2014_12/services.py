from __future__ import annotations

from tcsoa.gen.StructureManagement._2014_12.StructureSearch import ChangeTrackerInput, StructureChangesResponse
from tcsoa.gen.StructureManagement._2014_12.Effectivity import ReleaseStatusEffectivityInput, CreateOccEffectivityInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def getStructureChanges(cls, changeTrackerInput: List[ChangeTrackerInput]) -> StructureChangesResponse:
        """
        This operation searches for delta changes in the structure based on different search criteria. The BOMLine
        objects directly or indirectly affected by changes done in Incremental Change context or revision effectivity
        context or occurrence effectivity context that are configured in are returned. The caller must supply the
        BOMLine object(s) that determines the scope for the search in addition to search parameters like intent,
        release status names, and one of unit range or date range. The lines returned are those that are configured by
        the current revision rule. All the BOMLines created/found will be returned as part of ServiceData along with
        incremental changes elements ( in case of IncrementalChange context), or ItemRevisions ( in case of Revision
        effectivity/Occurrence effectivity). All partial errors are grouped by the index of the input vector. This
        operation should be consided when the scope will not yield too many expandlines lines below.
        
        Use cases:
        A user wants to find a set of incremental changes of a particular type and with a specific unit effectivity.
        """
        return cls.execute_soa_method(
            method_name='getStructureChanges',
            library='StructureManagement',
            service_date='2014_12',
            service_name='StructureSearch',
            params={'changeTrackerInput': changeTrackerInput},
            response_cls=StructureChangesResponse,
        )


class EffectivityService(TcService):

    @classmethod
    def createOccurrenceEffectivities(cls, input: List[CreateOccEffectivityInput]) -> ServiceData:
        """
        This operation creates a new effectivity object for each BOMLine  in the list. If the isShared flag is true the
        operation applies same effectivity for all BOMLine in the list.
        
        Use cases:
        - User can create and associate the effectivity with one occurrence by selecting appropriate line in the
        structure and choosing Tools->Effectivity->Occurrence Effectivity->View,Create and Edit.
        - User can create and associate the effectivity with several occurrences by selecting appropriate lines in the
        structure and choosing Tools->Effectivity->Occurrence Effectivity->Create on Multiple BOM Lines, ensure the Use
        shared effectivity check box is cleared so the effectivity is not shared between BOMLines.
        - User can create and associate the same effectivity with several occurrences by selecting appropriate lines in
        the structure and choosing Tools->Effectivity->Occurrence Effectivity->Create on Multiple BOM Lines, ensure the
        Use shared effectivity check box is checked so the effectivity can be shared among all occurrences.
        
        """
        return cls.execute_soa_method(
            method_name='createOccurrenceEffectivities',
            library='StructureManagement',
            service_date='2014_12',
            service_name='Effectivity',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def createReleaseStatusEffectivity(cls, input: List[ReleaseStatusEffectivityInput]) -> ServiceData:
        """
        This operation sets new effectivity on a release status.
        
        Use cases:
        User can configure a release status by choosing Tools->Effectivity->Revision Effectivity, then in the
        Effectivity dialog, select the corresponding release status and click create. Define Unit/Date range to set
        effectivity on the release status.
        """
        return cls.execute_soa_method(
            method_name='createReleaseStatusEffectivity',
            library='StructureManagement',
            service_date='2014_12',
            service_name='Effectivity',
            params={'input': input},
            response_cls=ServiceData,
        )
