from __future__ import annotations

from tcsoa.gen.Bom._2010_09.StructureManagement import ObjectCoverageResponse, ObjectCoverageInput, TraversedObjectsResponse, TraversedObjectsInput
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getTraversedObjectsByRule(cls, input: TraversedObjectsInput) -> TraversedObjectsResponse:
        """
        This SOA traverses the structure according to supplied filtering rule and returns the full list of resulting
        lines.
        """
        return cls.execute_soa_method(
            method_name='getTraversedObjectsByRule',
            library='Bom',
            service_date='2010_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=TraversedObjectsResponse,
        )

    @classmethod
    def verifyObjectCoverageByRule(cls, input: ObjectCoverageInput) -> ObjectCoverageResponse:
        """
        This SOA verifies whether the received lines fit the supplied filtering rule.
        """
        return cls.execute_soa_method(
            method_name='verifyObjectCoverageByRule',
            library='Bom',
            service_date='2010_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=ObjectCoverageResponse,
        )
