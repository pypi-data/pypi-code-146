from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_02.StructureVerification import ACInput, BatchDetails, EquivalentLines
from tcsoa.gen.StructureManagement._2016_05.StructureVerification import AccountabilityCheckResponse
from tcsoa.gen.StructureManagement._2013_05.StructureVerification import AttributeGroupAndFormComparisonResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def accountabilityCheck2(cls, input: ACInput, batchDetails: BatchDetails) -> AccountabilityCheckResponse:
        """
        The operation will call the existing accountability check functions, which will generate a check result for
        report in the colored display
        """
        return cls.execute_soa_method(
            method_name='accountabilityCheck2',
            library='StructureManagement',
            service_date='2016_05',
            service_name='StructureVerification',
            params={'input': input, 'batchDetails': batchDetails},
            response_cls=AccountabilityCheckResponse,
        )

    @classmethod
    def getAttrGrpsAndFormsComparisonDetail(cls, equivalentObjects: List[EquivalentLines], attributeGroupsNames: List[str], sourceConfigContext: BusinessObject, targetConfigContext: BusinessObject) -> AttributeGroupAndFormComparisonResponse:
        """
        This operation returns the details of differences between the supplied Attribute Groups for the supplied
        equivalent objects (that can be Cpd0DesignElement, Cpd0DesignFeature, or BOMLine objects) and the supplied
        configuration contexts for source equivalent object and target equivalent object respectively.For 4gd to 4gd
        compare, attribute group names includes attribute groups and managed attribute groups.Source and target
        configuration context is needed if the attribute group names include Managed attribute group properties.For
        each supplied attribute group the operation returns the list of its attributes, the attributes values for each
        supplied source and target, and the result of comparing each attribute on all supplied sources and targets.
        """
        return cls.execute_soa_method(
            method_name='getAttrGrpsAndFormsComparisonDetail',
            library='StructureManagement',
            service_date='2016_05',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'attributeGroupsNames': attributeGroupsNames, 'sourceConfigContext': sourceConfigContext, 'targetConfigContext': targetConfigContext},
            response_cls=AttributeGroupAndFormComparisonResponse,
        )
