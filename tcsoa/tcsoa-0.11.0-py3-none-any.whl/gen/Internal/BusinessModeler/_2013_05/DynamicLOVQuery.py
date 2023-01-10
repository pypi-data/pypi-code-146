from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LOVData(TcBaseObj):
    """
    This structure is used to store the LOV information (valueProperty and descriptionProperty) as well as the filter
    properties.This structure is used to provide the property names as input and in the result this same structure used
    to store the values of the input properties.
    
    :var valueProperty: The property name which is used as dynamic LOV value
    :var descriptionProperty: The property name which is used as dynamic LOV Value description.
    :var filterProperties: A list of property names which are used as a filter property.
    """
    valueProperty: str = ''
    descriptionProperty: str = ''
    filterProperties: List[str] = ()


@dataclass
class LOVSearchResults(TcBaseObj):
    """
    This structure contains the LOV results from the executeDynamicLOVQuery operation as well as the list of
    unprocessed UIDs.
    
    :var lovValues: The list of LOV Values, their description and values of all filter attributes.
    :var unprocessedUIDs: This is a list of unprocessed UIDs. The LOV ITK returns the number of results defined in the
    LovFilterData:: maxResult variable but out of these results LovFilterData:: numberToLoad number of results get
    processed and the rest of the result get stored in the list and sent back to the client. These unprocessed UIDs
    will be set as input in the next consecutive call of service operation to process next set of data.
    :var serviceData: The Service Data.
    """
    lovValues: List[LOVData] = ()
    unprocessedUIDs: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class LovFilterData(TcBaseObj):
    """
    This structure contains the information based on which the query results will be displayed in the test
    functionality. This structure contains the user entered filter string based on which query results will be filtered
    out as well as the property name based on which the result will be sorted.
    
    :var filterString: The filter string which is used to filter out the query output.
    :var maxResult: The maximum number of result to be processed.
    :var numberToLoad: The number of result to be loaded in a single processing.
    :var sortPropertyName: The name of the property the LOV search result will be sorted.
    :var sortOrder: The sorting order. A value of 1 indicates sort property values to be in ascending order. A value of
    2 indicates sort property values to be in descending order. 0 is to indicate no sort.
    """
    filterString: str = ''
    maxResult: int = 0
    numberToLoad: int = 0
    sortPropertyName: str = ''
    sortOrder: int = 0


@dataclass
class QueryData(TcBaseObj):
    """
    This structure contains the query string formed by query criteria, LOVData object which contains the LOV object
    name (valueProperty), LOV object description (descriptionProperty), list of filter properties provided by user and
    number of objects to be processed. This structure defines the input to the service operation
    executeDynamicLOVQuery. It contains LOV information as lovInputData, query definition as queryClass and
    queryString. This data structure contains a list of unprocessed UIDs. This list will be empty while a new query is
    going to be executed through the service operation. As an output service operation returns back the list of
    unprocessed UIDs to client which is eventually passed as an input parameter while displaying next set of LOV
    information.
    
    :var queryClass: This the business object class name on which the query will be generated. This represents the
    table name in database on which the query will be executed.
    :var queryString: This is a SQL style query string  formed by query criteria. This query string will contain query
    clauses as well as the table name on which the query will be executed.
    :var lovInputData: This variable stores the LOV information like the property name to represent LOV value and LOV
    description and a list of property name which is used as a filter property.
    :var filterData: It contains the user entered search string, number of result to be processed and sorting property
    name.
    :var unprocessedUIDs: This is a list of unprocessed UIDs. This list will be empty while the service operation is
    going to execute a query(in case of change in any other information in QueryData structure) and it will contain the
    list of unprocessed UIDs from the previous call of the service operation if the service operation is called only to
    process next set of unprocessed UIDs.
    """
    queryClass: str = ''
    queryString: str = ''
    lovInputData: LOVData = None
    filterData: LovFilterData = None
    unprocessedUIDs: List[str] = ()
