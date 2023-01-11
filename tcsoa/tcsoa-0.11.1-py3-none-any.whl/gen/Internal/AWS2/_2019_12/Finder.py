from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2019_06.Finder import FilterCriteriaInput
from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchSortCriteria
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.AWS2._2017_12.Finder import SearchFilter4


@dataclass
class PropertyInfo(TcBaseObj):
    """
    A structure containing the internal and display names of a property.
    
    :var internalName: The internal name of the property.
    :var displayName: The display name of the property.
    """
    internalName: str = ''
    displayName: str = ''


@dataclass
class SearchInput4(TcBaseObj):
    """
    A structure containing input search criteria.
    
    :var providerName: The name of the search provider.
    :var searchCriteria: A map (string, string) used to define the search criteria to be performed by the provider.
    This is the same as the searchCriteria map in SearchInput structure used in Awp0::Soa::Internal::AWS2::_2016_03::
    Finder::performSearch operation.
    :var searchFilterMap: A map (string, list of SearchFilter4) containing the list of search filters for each search
    filter field. The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". For example: WorkspaceObject.release_statuses. The value in the map is the value of the
    search filter.
    :var columnFilters: A list of filters (FilterCriteriaInput) to be applied on the columns.
    :var searchSortCriteria: The criteria to use to sort the results.
    """
    providerName: str = ''
    searchCriteria: StringMap4 = None
    searchFilterMap: SearchFilterMap7 = None
    columnFilters: List[FilterCriteriaInput] = ()
    searchSortCriteria: List[SearchSortCriteria] = ()


@dataclass
class ExportObjectsToFileResponse(TcBaseObj):
    """
    This structure contains the file ticket of exported file.
    
    :var serviceData: Partial errors are returned in the Service Data.
    :var fileTickets: A list of file tickets for the exported files.
    """
    serviceData: ServiceData = None
    fileTickets: List[str] = ()


@dataclass
class FilterFacetInput(TcBaseObj):
    """
    A structure containing input facet search criteria.
    
    :var columnName: The column name for which we need to obtain possible filter values (facets).
    :var providerName: The name of the data provider. This is the RuntimeBusinessObject type name.
    :var startIndex: The start index to return the facet values search results.
    :var maxToReturn: The maximum number of unique facet values to return.
    :var searchCriteria: A map (string, string) used to define the search criteria to be performed by the provider.
    This is the same as the searchCriteria map in SearchInput structure used in performSearch operation.
    :var columnFilters: A list of filters (FilterCriteriaInput) to be applied on the columns.
    :var searchFilterMap: A map (string, list of SearchFilter4) containing the list of search filters for each search
    filter field. The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". For example: WorkspaceObject.release_statuses, the value in the map is the value of the
    search filter.
    """
    columnName: str = ''
    providerName: str = ''
    startIndex: int = 0
    maxToReturn: int = 0
    searchCriteria: StringMap4 = None
    columnFilters: List[FilterCriteriaInput] = ()
    searchFilterMap: SearchFilterMap7 = None


@dataclass
class FilterFacetResponse(TcBaseObj):
    """
    Structure containing the filter facet values and partial errors, if any.
    
    :var facetValues: A JSON string of the sorted list of unique facet values based on the query results from the data
    provider and the total unique facet values found in the search results. 
    The JSON will be in the following format, where "values" represents the sorted facet values for the given column
    and "totalFound" represents the total number of facet values found:
    {
        "values": [
            "facetValue1",
            "facetValue2",
            &hellip;
            "facetValueN"
        ],
        "totalFound": N
    }
    :var serviceData: Partial errors are returned in the Service Data.
    """
    facetValues: str = ''
    serviceData: ServiceData = None


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap7 = Dict[str, List[SearchFilter4]]


"""
Map from string to string.
"""
StringMap4 = Dict[str, str]
