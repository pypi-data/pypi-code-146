from __future__ import annotations

from tcsoa.gen.Internal.Query._2012_02.SavedQuery import DescribeSavedQueryDefinitionsResponse, DescribeSavedQueryDefinitionInput
from typing import List
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def describeSavedQueryDefinitions(cls, requestedQueries: List[DescribeSavedQueryDefinitionInput]) -> DescribeSavedQueryDefinitionsResponse:
        """
        Returns a complete list of all the clauses and sort attributes that make up a saved query.  This provides a
        complete list of information, including that which is internal from the customer.
        """
        return cls.execute_soa_method(
            method_name='describeSavedQueryDefinitions',
            library='Internal-Query',
            service_date='2012_02',
            service_name='SavedQuery',
            params={'requestedQueries': requestedQueries},
            response_cls=DescribeSavedQueryDefinitionsResponse,
        )
