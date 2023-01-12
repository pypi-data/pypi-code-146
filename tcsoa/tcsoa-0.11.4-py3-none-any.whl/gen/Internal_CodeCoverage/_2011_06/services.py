from __future__ import annotations

from typing import List
from tcsoa.base import TcService


class CodeCoverageManagementService(TcService):

    @classmethod
    def performOperation(cls, opType: str, arguments: List[str]) -> str:
        """
        Service for CodeCoverage integration. This service allows users to start/stop the tcserver code coverage hit
        countering process from the RAC UI.
        
        Use cases:
        From the RAC UI, before users start a test to collect test-to-SOA interface information, the user can click to
        start button to start the tcserver code coverage countering process. And after the test completed, users can
        click stop button and stop the tcserver code coverage countering process, and the hit information will be saved
        to a local file specified by users.
        """
        return cls.execute_soa_method(
            method_name='performOperation',
            library='Internal-CodeCoverage',
            service_date='2011_06',
            service_name='CodeCoverageManagement',
            params={'opType': opType, 'arguments': arguments},
            response_cls=str,
        )
