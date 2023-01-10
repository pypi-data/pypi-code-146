from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def applyRollupVariantConfiguration(cls, bomlines: List[BOMLine], considerWindowSVR: bool) -> ServiceData:
        """
        The applyRollupVariantConfiguration operation applies overlay product configurator authored configuration on
        the BOM Window by generating the rolled up variant expression from input BOM Lines. If the considerWindowSVR
        input is set to true, it considers the existing Variant Rule applied on the BOM Window along with the rolled up
        expression. BOMWindow must have effective configurator context for this operation to be successful.
        
        Use cases:
        It allows users to work in the context of product structure lines that truly coexist when variants are
        configured.Users won't have to cascade variant conditions from child to parents. This will reduce the
        complexity in variant conditions managed by the customers and at the same time make the overall process more
        efficient.
        """
        return cls.execute_soa_method(
            method_name='applyRollupVariantConfiguration',
            library='Internal-StructureManagement',
            service_date='2019_06',
            service_name='VariantManagement',
            params={'bomlines': bomlines, 'considerWindowSVR': considerWindowSVR},
            response_cls=ServiceData,
        )
