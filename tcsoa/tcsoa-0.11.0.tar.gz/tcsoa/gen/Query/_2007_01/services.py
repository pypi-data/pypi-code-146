from __future__ import annotations

from typing import List
from tcsoa.gen.Query._2007_01.SavedQuery import RetrieveQueryCriteriaResponse, SaveQueryCriteriaInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def reorderSavedQueryCriterias(cls, queryCriteriaNames: List[str]) -> ServiceData:
        """
        Reorder the saved Query Criterias in the MySavedSearches List:
          The new order of query criteria names specified in the input list will be stored in the MySavedSearches list. 
          The input list should contain only existing query criteria names 
          If a query criteria name in the list is not located, it will not be stored in the list. 
          The number of entries in the input list should match the number entries in the MySavedSearches list.
        
        Exceptions:
        >- When input argument is not specified
        - When input vector is empty
        
        """
        return cls.execute_soa_method(
            method_name='reorderSavedQueryCriterias',
            library='Query',
            service_date='2007_01',
            service_name='SavedQuery',
            params={'queryCriteriaNames': queryCriteriaNames},
            response_cls=ServiceData,
        )

    @classmethod
    def retrieveQueryCriterias(cls, queryCriteriaNames: List[str]) -> RetrieveQueryCriteriaResponse:
        """
        Retrieve the information on the saved search by the search name.
        """
        return cls.execute_soa_method(
            method_name='retrieveQueryCriterias',
            library='Query',
            service_date='2007_01',
            service_name='SavedQuery',
            params={'queryCriteriaNames': queryCriteriaNames},
            response_cls=RetrieveQueryCriteriaResponse,
        )

    @classmethod
    def saveQueryCriterias(cls, queryCriterias: List[SaveQueryCriteriaInfo]) -> ServiceData:
        """
        Saves a saved search with search name, query name, entry names, and entry values. If search name is not
        provided, the criteria keys or the criteria values size is 0, or the criteria keys size does not equal to the
        criteria values size, or if error happens while creating the saved search, the related error information will
        be added to the error stack. If the search criteria size is no more than 0, ServiceException will throw out of
        this service. The created saved search objects will be returned.
        
        Use cases:
        User selects a query and fills in some criterias, and then save the search from thin client with a search name.
        """
        return cls.execute_soa_method(
            method_name='saveQueryCriterias',
            library='Query',
            service_date='2007_01',
            service_name='SavedQuery',
            params={'queryCriterias': queryCriterias},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteQueryCriterias(cls, queryCriteriaNames: List[str]) -> ServiceData:
        """
        Delete saved searches with given names.
        
        Use cases:
        Delete specified saved searches.
        """
        return cls.execute_soa_method(
            method_name='deleteQueryCriterias',
            library='Query',
            service_date='2007_01',
            service_name='SavedQuery',
            params={'queryCriteriaNames': queryCriteriaNames},
            response_cls=ServiceData,
        )
