from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_02.StructureVerification import CompareNetEffectivityResponse, EquivalentSetElement, GetPropertyComparisonDetailsResponse, GetDescendentComparisonDetailsResponse, PropagationResponse, GetPartitionComparisonDetailsResponse, EquivalentLines, ACInput, GetPredecessorComparisonDetailsResponse, AsyncACInput, PropagationInput, BatchDetails, AsyncDetails, GetAssignmentComparisonDetailsResponse
from tcsoa.gen.StructureManagement._2010_09.StructureVerification import AccountabilityCheckResponse
from tcsoa.gen.StructureManagement._2012_02.IncrementalChange import BomLineInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def getPropertyComparisonDetails(cls, equivalentObjects: List[EquivalentSetElement]) -> GetPropertyComparisonDetailsResponse:
        """
        method to retrieve details for supplied properties on the provided equivalent sets of lines.
        """
        return cls.execute_soa_method(
            method_name='getPropertyComparisonDetails',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects},
            response_cls=GetPropertyComparisonDetailsResponse,
        )

    @classmethod
    def compareNetEffectivity(cls, lines: List[EquivalentLines], ignoreOverlapErrors: bool, useStructureConfiguration: bool, returnOnFirstMismatch: bool) -> CompareNetEffectivityResponse:
        """
        effectivity of 2 sets of lines that are deemed equivalent in some form.
        """
        return cls.execute_soa_method(
            method_name='compareNetEffectivity',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'lines': lines, 'ignoreOverlapErrors': ignoreOverlapErrors, 'useStructureConfiguration': useStructureConfiguration, 'returnOnFirstMismatch': returnOnFirstMismatch},
            response_cls=CompareNetEffectivityResponse,
        )

    @classmethod
    def propagateProperties(cls, input: List[PropagationInput]) -> PropagationResponse:
        """
        method to propagate properties.
        """
        return cls.execute_soa_method(
            method_name='propagateProperties',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=PropagationResponse,
        )

    @classmethod
    def accountabilityCheck(cls, input: ACInput, batchDetails: BatchDetails) -> AccountabilityCheckResponse:
        """
        The operation will call the existing accountability check functions, which will generate a check result for
        report in the colored display.
        """
        return cls.execute_soa_method(
            method_name='accountabilityCheck',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'input': input, 'batchDetails': batchDetails},
            response_cls=AccountabilityCheckResponse,
        )

    @classmethod
    def accountabilityCheckAsync(cls, acinput: AsyncACInput, asyncDetails: AsyncDetails) -> None:
        """
        asynchronous implementation for the accountabilityCheck.
        """
        return cls.execute_soa_method(
            method_name='accountabilityCheckAsync',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'acinput': acinput, 'asyncDetails': asyncDetails},
            response_cls=None,
        )

    @classmethod
    def getAssignmentComparisonDetails(cls, equivalentObjects: List[EquivalentLines], partRelationTypes: List[str], toolRelationTypes: List[str], compareLA: int, compareManual: bool) -> GetAssignmentComparisonDetailsResponse:
        """
        get the details of any differences between assignments for the supplied src and target objects.
        """
        return cls.execute_soa_method(
            method_name='getAssignmentComparisonDetails',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'partRelationTypes': partRelationTypes, 'toolRelationTypes': toolRelationTypes, 'compareLA': compareLA, 'compareManual': compareManual},
            response_cls=GetAssignmentComparisonDetailsResponse,
        )

    @classmethod
    def getDescendentComparisonDetails(cls, input: List[EquivalentLines], ignoreStructureSpecific: bool) -> GetDescendentComparisonDetailsResponse:
        """
        for each input equivalent set capture the response of getDescendentComparisonDetails method. Has the list of
        details for each input set and serviceData to capture partial errors.
        """
        return cls.execute_soa_method(
            method_name='getDescendentComparisonDetails',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'input': input, 'ignoreStructureSpecific': ignoreStructureSpecific},
            response_cls=GetDescendentComparisonDetailsResponse,
        )

    @classmethod
    def getPartitionComparisonDetails(cls, input: List[EquivalentLines]) -> GetPartitionComparisonDetailsResponse:
        """
        service to get details on a mismatch of parititions.
        """
        return cls.execute_soa_method(
            method_name='getPartitionComparisonDetails',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=GetPartitionComparisonDetailsResponse,
        )

    @classmethod
    def getPredecessorComparisonDetails(cls, input: List[EquivalentLines], ignoreStructureSpecific: bool) -> GetPredecessorComparisonDetailsResponse:
        """
        for a given equivalent set of lines/object, compute and return the list of predecessor detail elements and flag
        if different.
        """
        return cls.execute_soa_method(
            method_name='getPredecessorComparisonDetails',
            library='StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'input': input, 'ignoreStructureSpecific': ignoreStructureSpecific},
            response_cls=GetPredecessorComparisonDetailsResponse,
        )


class IncrementalChangeService(TcService):

    @classmethod
    def carryOver(cls, bomLineInfos: List[BomLineInfo]) -> ServiceData:
        """
        This operation carries the IncrementalChangeElement (ICE) object(s) from the source line to the corresponding
        target line by cloning them. 
        There are two BMIDE constants that were introduced for this functionality
          
        Type Constant Fnd0EnableIceCarryOver
        Property Constant Fnd0AttrIcesToExclude
        
        - New IncrementalChangeElement object(s) are attached to the original incremental change revision.
        
        - Add changes on the occurrence are ignored - It does not make sense to have two occurrences appearing at the
        same time at different locations.
        
        - GDELine objects are not supported.
        
        - For attribute changes the context of the absolute occurrence data is the new parent BOMView Revision.
        
        - If there is no write access on incremental change revision, the carryover is allowed with a programmatic
        bypass.
        - If there is any failure while cloning any IncrementalChangeElement object that is being carried over, the
        entire operation will rollback.
        
        - Carryover is not possible if we have the following two conditions:
        - Both source and target BomView Revision item type are not available in the BMIDE Type Constant
        Fnd0EnableIceCarryOver.
        - BOM-BOP case - If the source line is a BOMLine and the target line is a BOP (Bill of Process) line or vice
        versa
        
        
        
        Use cases:
        User wants to carry over IncrementalChangeElement object(s) when doing a Copy-Paste or a Cut-Paste of a BOMLine
        having IncrementalChangeElement object(s), from one structure partition to another partition within the Plant
        BOP.
        User wants to carry over IncrementalChangeElement object(s) when doing a Copy-Paste or a Cut-Paste of a BOMLine
        having IncrementalChangeElement object(s), from Product BOP and to another partition in the Plant BOP.
        
        """
        return cls.execute_soa_method(
            method_name='carryOver',
            library='StructureManagement',
            service_date='2012_02',
            service_name='IncrementalChange',
            params={'bomLineInfos': bomLineInfos},
            response_cls=ServiceData,
        )
