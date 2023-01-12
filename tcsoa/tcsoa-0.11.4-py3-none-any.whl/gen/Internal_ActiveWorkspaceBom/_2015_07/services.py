from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import FindMatchingFilterResponse, FindMatchingFilterInput
from typing import List
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def findMatchingFilters(cls, input: List[FindMatchingFilterInput]) -> FindMatchingFilterResponse:
        """
        This operation retrieves filters matching input search string.
        """
        return cls.execute_soa_method(
            method_name='findMatchingFilters',
            library='Internal-ActiveWorkspaceBom',
            service_date='2015_07',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=FindMatchingFilterResponse,
        )
