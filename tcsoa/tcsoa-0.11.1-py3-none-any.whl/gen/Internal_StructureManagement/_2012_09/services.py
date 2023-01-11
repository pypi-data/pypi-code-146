from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2012_09.StructureVerification import ValidCriteriaInput, GetValidCriteriaResponse
from typing import List
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def getValidCriteria(cls, inputscope: List[ValidCriteriaInput]) -> GetValidCriteriaResponse:
        """
        This operation is to be used when comparing two structures, and equivalence criteria is to be obtained. The
        input source scopes target scopes are passed to EquivalenceCriteria objects on the server - which determine if
        they are valid for this scenario or not. The result is a well defined set of keys that uniquely identify the
        EquivalenceCriteria object(s) that are valid.
        """
        return cls.execute_soa_method(
            method_name='getValidCriteria',
            library='Internal-StructureManagement',
            service_date='2012_09',
            service_name='StructureVerification',
            params={'inputscope': inputscope},
            response_cls=GetValidCriteriaResponse,
        )
