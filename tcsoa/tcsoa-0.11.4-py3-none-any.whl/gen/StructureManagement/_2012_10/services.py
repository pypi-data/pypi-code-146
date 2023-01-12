from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_10.Structure import CutItemParam
from tcsoa.gen.StructureManagement._2012_02.StructureVerification import EquivalentLines
from tcsoa.gen.StructureManagement._2012_10.StructureVerification import StringToPartialMatchCriteria, GetAssignmentComparisonDetailsResponse, GetComparisonSummariesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def cutItems(cls, input: List[CutItemParam]) -> ServiceData:
        """
        Cut lines of the selected Item Revisions in a window and delete the Item Revisions.
        If the selected Item Revision is the last revision of the Item , then the Item will be deleted.
        
        Use cases:
        Use case1: Simple Cut
        A user wants to delete some Item Revisions in a structure which are not referenced anywhere else. The user
        calls the operation with the BOMWindow and the Item Revisions. The BOMLine for the selected Item Revisions will
        be removed from the structure and the Item Revisions will be deleted.
        
        Use case2: Cut with partial errors
        A user wants to delete some Item Revisions in a structure which are referenced in My Teamcenter and lines of
        some of the Item Revisions are in released structure. The user calls the operation with the BOMWindow and the
        Item revisions. The Item Revisions for the lines that are in released structure will fail to be deleted but the
        other Item Revisions will be deleted and the entries in My Teamcenter will also be removed.
        
        Use case3: Cut the last revision of the item
        A user wants to delete an Item Revision, which is the last revision of the Item. The user calls the operation
        with the BOMWindow and the Item Revision. The BOMLine for the selected Item Revision will be removed from the
        structure and the Item will be deleted
        
        """
        return cls.execute_soa_method(
            method_name='cutItems',
            library='StructureManagement',
            service_date='2012_10',
            service_name='Structure',
            params={'input': input},
            response_cls=ServiceData,
        )


class StructureVerificationService(TcService):

    @classmethod
    def getAssignmentComparisonDetails(cls, equivalentObjects: List[EquivalentLines], partialMatchCriteria: List[StringToPartialMatchCriteria]) -> GetAssignmentComparisonDetailsResponse:
        """
        This operation returns the details of any differences between assignments for the supplied source and target
        BOMLine objects. Assignments can be parts or tools, manual or resolved by logical assignments. The operation
        takes the source and target BOMLine objects and compares their assignments according to their types - manual
        assignments are compared with manual, resolved with resolved, parts with parts and tools with tools. The source
        and target assignments are returned by this operation in the form of a table that is created by the output
        structures.
        """
        return cls.execute_soa_method(
            method_name='getAssignmentComparisonDetails',
            library='StructureManagement',
            service_date='2012_10',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'partialMatchCriteria': partialMatchCriteria},
            response_cls=GetAssignmentComparisonDetailsResponse,
        )

    @classmethod
    def getComparisonSummaries(cls, equivalentObjects: List[EquivalentLines], partialMatchCriteria: List[StringToPartialMatchCriteria]) -> GetComparisonSummariesResponse:
        """
        This operation retrieves comparison summaries for supplied extensions on the provided equivalent sets of
        objects. The source objects in each set can be BOMLines, Cpd0DesignElements or Cpd0DesignFeatures. The target
        objects in each set can be only BOMLines. For each received extension on each received equivalent set it
        performs comparison of objects in the equivalent set for this extension according to received criteria. For
        each such comparison only the result is returned - a flag indicating whether the input objects were determined
        different or not. This operation returns comparison results for any number of extensions simultaneously.
        """
        return cls.execute_soa_method(
            method_name='getComparisonSummaries',
            library='StructureManagement',
            service_date='2012_10',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'partialMatchCriteria': partialMatchCriteria},
            response_cls=GetComparisonSummariesResponse,
        )
