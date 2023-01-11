from __future__ import annotations

from tcsoa.gen.Requirementsmanagement._2012_09.RequirementsManagement import GetBOMLineInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def getBomlineAfterCreate(cls, inputs: List[GetBOMLineInfo]) -> ServiceData:
        """
        This operation creates a BOMLine for a newly created  Item and adds it to the selected parent BOMLine and
        checks out the latest revision of newly created Item based on a check-out preference. The inputs structure for
        this operation contains selected parent BOMLine and newly created Item (e.g. Functionality or Logical Block).
        """
        return cls.execute_soa_method(
            method_name='getBomlineAfterCreate',
            library='Requirementsmanagement',
            service_date='2012_09',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
