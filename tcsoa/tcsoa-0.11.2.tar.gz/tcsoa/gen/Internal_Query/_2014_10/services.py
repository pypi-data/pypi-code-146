from __future__ import annotations

from tcsoa.gen.Internal.Query._2012_02.SavedQuery import DescribeSavedQueryDefinitionInput
from tcsoa.gen.Internal.Query._2014_10.SavedQuery import DescribeSavedQueryDefnResponse3
from typing import List
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def describeSavedQueryDefinitions3(cls, requestedQueries: List[DescribeSavedQueryDefinitionInput]) -> DescribeSavedQueryDefnResponse3:
        """
        This operation returns detailed information about a saved query, including the search criteria and default sort
        attributes.  The search criteria is made up of a list of attributes and the parameters used to evaluate them. 
        End user running the query will be able to enter a search value for each attribute listed in the search
        criteria.  The criteria will indicate the math operation ("!=", ">", etc) to use when evaluating the users
        input.  Default values are also included.
        The sort attributes are a way to define a default sorting to use whenever the saved query is executed.  For
        each attribute, an "Ascending" or "Descending" sort order will be included.  Any user running the saved query
        will see the results sorted according to the sorting defined on the saved query.  The end user can use the Sort
        dialog to override what is defined.
        All of the attributes in both lists will include the L10N key to be used when displaying the attribute to the
        user. Also all the attributes will be indicated whether a LOVs are attached to them or not. Use this
        information to render LOV UI for the attributes. This requires LOV service operations which can used to
        retrieve the LOV values to display to the end user on request. 
        """
        return cls.execute_soa_method(
            method_name='describeSavedQueryDefinitions3',
            library='Internal-Query',
            service_date='2014_10',
            service_name='SavedQuery',
            params={'requestedQueries': requestedQueries},
            response_cls=DescribeSavedQueryDefnResponse3,
        )
