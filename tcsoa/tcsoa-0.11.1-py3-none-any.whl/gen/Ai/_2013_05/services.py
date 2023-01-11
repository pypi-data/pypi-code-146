from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Ai._2013_05.Ai import FindRequestOnAiWithReferencesResponse
from typing import List
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def findRequestOnAiWithReferences(cls, baseRef: List[BusinessObject], requestType: str) -> FindRequestOnAiWithReferencesResponse:
        """
        The operation queries for the latest RequestObjects (by creation date and type) on the latest
        ApplicationInterface Object ( by creation date) that references the input object in the base_refs member.
        Additional filtering based on type of RequestObject is also possible.
        """
        return cls.execute_soa_method(
            method_name='findRequestOnAiWithReferences',
            library='Ai',
            service_date='2013_05',
            service_name='Ai',
            params={'baseRef': baseRef, 'requestType': requestType},
            response_cls=FindRequestOnAiWithReferencesResponse,
        )
