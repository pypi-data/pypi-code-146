from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0Element, Awb0ProductContextInfo
from typing import List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_12.OccurrenceManagement import PackedOccurrenceCSIDsResponse
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def getPackedOccurrenceCSIDs(cls, productContextInfo: Awb0ProductContextInfo, occurrences: List[Awb0Element]) -> PackedOccurrenceCSIDsResponse:
        """
        Retrieves the clone stable ids of packed occurrences for input occurrences and product configuration
        information.
        
        Use cases:
        User has opened the content in Active Workspace in packed mode. If user selects any occurrence in primary work
        area then viewer should display all packed occurrences of the selected occurrence as well.
        """
        return cls.execute_soa_method(
            method_name='getPackedOccurrenceCSIDs',
            library='Internal-ActiveWorkspaceBom',
            service_date='2017_12',
            service_name='OccurrenceManagement',
            params={'productContextInfo': productContextInfo, 'occurrences': occurrences},
            response_cls=PackedOccurrenceCSIDsResponse,
        )
