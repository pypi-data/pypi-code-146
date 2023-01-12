from __future__ import annotations

from tcsoa.gen.Query._2010_09.SavedQuery import BusinessObjectQueryInput
from typing import List
from tcsoa.gen.Query._2007_09.SavedQuery import SavedQueriesResponse
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def executeBusinessObjectQueries(cls, inputs: List[BusinessObjectQueryInput]) -> SavedQueriesResponse:
        """
        Execute business object searches (Simple Search) and return search results.
        
        Use cases:
        Execute business object searches (Simple Search).
        """
        return cls.execute_soa_method(
            method_name='executeBusinessObjectQueries',
            library='Query',
            service_date='2010_09',
            service_name='SavedQuery',
            params={'inputs': inputs},
            response_cls=SavedQueriesResponse,
        )
