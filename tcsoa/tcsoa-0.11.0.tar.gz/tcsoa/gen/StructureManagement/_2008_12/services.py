from __future__ import annotations

from tcsoa.gen.StructureManagement._2008_12.StructureVerification import AccCheckInput, AccountabilityCheckResponse
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def accountabilityCheck(cls, input: AccCheckInput) -> AccountabilityCheckResponse:
        """
        The operation will call the existing accountability check functions,  which will generate a check result for
        report in the colored display.
        """
        return cls.execute_soa_method(
            method_name='accountabilityCheck',
            library='StructureManagement',
            service_date='2008_12',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=AccountabilityCheckResponse,
        )
