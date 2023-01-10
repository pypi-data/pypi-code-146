from __future__ import annotations

from tcsoa.gen.Internal.BusinessModeler._2013_05.DynamicLOVQuery import LOVSearchResults, QueryData
from tcsoa.base import TcService


class DynamicLOVQueryService(TcService):

    @classmethod
    def executeDynamicLOVQuery(cls, queryData: QueryData) -> LOVSearchResults:
        """
        This operation queries for a subset of LOV values based on the desired query constraints. The dynamic LOV
        definition including the query string, query class and the properties representing the value and description
        are passed to this operation. Apart from this filter information (LOVFilterData) are passed to this service
        which is used to define the output (no of output, order of output information) of this service operation. This
        service operation executes the LOV query to database every time when the QueryData:: unprocessedUIDs list is
        empty otherwise it process the next set of UIDs from the list of unprocessed UIDs and send it back to the
        client.
        
        Exceptions:
        >ServiceException :
        - 226576 - The query for the dynamic LOV has failed to execute. Please refer to the Teamcenter server syslog
        file for details, and check the query attributes.
        - 226577 - An error has occurred while retrieving properties values. Please contact your Teamcenter
        administrator.
        
        """
        return cls.execute_soa_method(
            method_name='executeDynamicLOVQuery',
            library='Internal-BusinessModeler',
            service_date='2013_05',
            service_name='DynamicLOVQuery',
            params={'queryData': queryData},
            response_cls=LOVSearchResults,
        )
