from __future__ import annotations

from tcsoa.gen.Query._2010_04.SavedQuery import FindSavedQueriesCriteriaInput, FindSavedQueriesResponse
from typing import List
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def findSavedQueries(cls, inputCriteria: List[FindSavedQueriesCriteriaInput]) -> FindSavedQueriesResponse:
        """
        The user can find the saved queries of interest by passing in the criteria such as query name and description.
        The queries that are matching the input criteria will be returned back to the user.  This operation can be sued
        to find the queries with a given name(s) or description(s) or combination of name(s) and description(s). This
        operation returns the queries matching the input criteria names and descriptions.
        
        Use cases:
        Find saved queries by given saved query name(s) and description(s).
        """
        return cls.execute_soa_method(
            method_name='findSavedQueries',
            library='Query',
            service_date='2010_04',
            service_name='SavedQuery',
            params={'inputCriteria': inputCriteria},
            response_cls=FindSavedQueriesResponse,
        )
