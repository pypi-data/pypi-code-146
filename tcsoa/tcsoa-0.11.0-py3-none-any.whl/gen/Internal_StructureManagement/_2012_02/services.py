from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.StructureManagement._2012_02.StructureVerification import PartialMatchCriteria2, GetActivitiesComparisonDetailsResponse, EquivalentLines2, ToolRequirementComparisonResult
from typing import List
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def getToolRequirementComparisonDetails(cls, sourceObjects: List[BusinessObject], targetObjects: List[BusinessObject]) -> ToolRequirementComparisonResult:
        """
        Compares the tool requirements and fetches their comparison data. Refer to the complete documentation of
        ToolRequirementComparisonData on the data that are compared and how they are represented.
        """
        return cls.execute_soa_method(
            method_name='getToolRequirementComparisonDetails',
            library='Internal-StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'sourceObjects': sourceObjects, 'targetObjects': targetObjects},
            response_cls=ToolRequirementComparisonResult,
        )

    @classmethod
    def getActivitiesComparisonDetails(cls, equivalentObjects: List[EquivalentLines2], comparisonCriteria: PartialMatchCriteria2) -> GetActivitiesComparisonDetailsResponse:
        """
        Returns the details of any differences between activities for the supplied source and target objects.
        """
        return cls.execute_soa_method(
            method_name='getActivitiesComparisonDetails',
            library='Internal-StructureManagement',
            service_date='2012_02',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'comparisonCriteria': comparisonCriteria},
            response_cls=GetActivitiesComparisonDetailsResponse,
        )
