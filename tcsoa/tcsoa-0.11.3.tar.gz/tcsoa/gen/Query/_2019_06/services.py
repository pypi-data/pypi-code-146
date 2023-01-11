from __future__ import annotations

from tcsoa.gen.Query._2019_06.SavedQuery import BusinessObjectQueryInput3
from typing import List
from tcsoa.gen.Query._2007_09.SavedQuery import SavedQueriesResponse
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def executeBOQueriesWithSort(cls, inputs: List[BusinessObjectQueryInput3]) -> SavedQueriesResponse:
        """
        This operation executes business object queries with sorting options.
        """
        return cls.execute_soa_method(
            method_name='executeBOQueriesWithSort',
            library='Query',
            service_date='2019_06',
            service_name='SavedQuery',
            params={'inputs': inputs},
            response_cls=SavedQueriesResponse,
        )
