from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2017_06.Finder import ColumnConfig2
from tcsoa.gen.Internal.AWS2._2018_12.Finder import ExportSearchResultsResponse
from tcsoa.gen.Internal.AWS2._2018_12.MultiSite import StringVectorMap, FetchODSResponse
from typing import List
from tcsoa.gen.Internal.AWS2._2018_05.Finder import SearchInput2
from tcsoa.base import TcService


class FinderService(TcService):

    @classmethod
    def exportSearchResults(cls, searchInput: SearchInput2, columnConfig: ColumnConfig2, exportAll: bool, selectedObjectUIDs: List[str], applicationFormat: str) -> ExportSearchResultsResponse:
        """
        This operation exports Teamcenter business objects based on search results to the MSExcelX application. The
        operation allows caller to specify a list of objects to export or to specify if they want to export all objects
        from the search result.
        If the caller chooses to export a list of objects then the object UIDs must be passed along with column
        configuration information. The order of the objects received will be the order of objects exported. 
        If the caller chooses to export all objects, then this operation requires searchInput object parameter to be
        populated which is used to perform a search and the result will be exported. The searchSortCriteria property
        will be used to sort the exported objects.
        
        Use cases:
        Use Case:
        1) The user selects single or multiple objects in Active Workspace client. The user clicks on the Export button
        and selects the option to export the selected objects and clicks on export, then the selected objects are
        exported to MsExcelX. 
        2) The user does not select any objects from list of search results in Active Workspace client. The user clicks
        on the Export button and selects the option to export all search results and clicks on export, then all objects
        are exported to MsExcelX.
        """
        return cls.execute_soa_method(
            method_name='exportSearchResults',
            library='Internal-AWS2',
            service_date='2018_12',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfig': columnConfig, 'exportAll': exportAll, 'selectedObjectUIDs': selectedObjectUIDs, 'applicationFormat': applicationFormat},
            response_cls=ExportSearchResultsResponse,
        )


class MultiSiteService(TcService):

    @classmethod
    def fetchODSRecords(cls, odsSiteName: str, searchMode: int, startDate: str, endDate: str, pubrList: List[str], odsSessionInfo: StringVectorMap) -> FetchODSResponse:
        """
        This operation queries for Object Directory Service (ODS) publication records at the target ODS site based on
        the input criteria and serializes the data into one or more TC XML files. The search criteria can be date based
        or a list of objects which have been previously published. Read tickets are returned for the generated TC XML
        files.
        
        Use cases:
        This will be used to extract ODS data for indexing purposes. The output will be used to populate data to a
        search engine like Solr.
        """
        return cls.execute_soa_method(
            method_name='fetchODSRecords',
            library='Internal-AWS2',
            service_date='2018_12',
            service_name='MultiSite',
            params={'odsSiteName': odsSiteName, 'searchMode': searchMode, 'startDate': startDate, 'endDate': endDate, 'pubrList': pubrList, 'odsSessionInfo': odsSessionInfo},
            response_cls=FetchODSResponse,
        )
