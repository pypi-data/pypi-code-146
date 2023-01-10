from __future__ import annotations

from tcsoa.gen.Internal.Multisite._2018_06.Search import FetchOdsResponse, StringVectorMap
from typing import List
from tcsoa.base import TcService


class SearchService(TcService):

    @classmethod
    def fetchOdsRecords(cls, odsSiteName: str, searchMode: int, startDate: str, endDate: str, pubrList: List[str], odsSessionInfo: StringVectorMap) -> FetchOdsResponse:
        """
        This operation queries for Object Directory Service (ODS) publication records at the target ODS site based on
        the input criteria and serializes the data into a TCXML file. The search criteria can be date based or a list
        of objects which have been previously published. Read tickets are returned to the generated files.
        
        Use cases:
        This will be used to extract ODS data for indexing purposes. The output will be used to populate a seache
        engine like Solr.
        """
        return cls.execute_soa_method(
            method_name='fetchOdsRecords',
            library='Internal-Multisite',
            service_date='2018_06',
            service_name='Search',
            params={'odsSiteName': odsSiteName, 'searchMode': searchMode, 'startDate': startDate, 'endDate': endDate, 'pubrList': pubrList, 'odsSessionInfo': odsSessionInfo},
            response_cls=FetchOdsResponse,
        )
