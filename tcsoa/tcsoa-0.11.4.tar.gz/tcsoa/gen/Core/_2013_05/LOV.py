from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ListOfValues
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InitialLovData(TcBaseObj):
    """
    Initial LOV Data sent to the server during an LOV query.
    
    :var lov: The ListOfValues that is being evaluated;Use this when the lovInput is not possible to construct and need
    to get the values of specified Lov, otherwise pass as null.
    :var lovInput: This is a container of key-value pairs representing the desired entries for different property
    fields for different operations (Create, SaveAs, Revise, etc.). It is used for context-based evaluation of the LOV
    values where the property values are substituted into query criteria. It is also used for interdependent LOV
    evaluation e.g to evaluate interdependent LOV values at dependent levels given the values at the higher levels that
    are populated on the lovInput
    :var propertyName: The name of the Property for which LOV is being evaluated.
    :var filterData: Filter critieria and other search data.
    """
    lov: ListOfValues = None
    lovInput: LOVInput = None
    propertyName: str = ''
    filterData: LovFilterData = None


@dataclass
class LOVBehaviorData(TcBaseObj):
    """
    Container of data such as LOV usage, Style, Lov Column Names. Additionally it  contains interdependent properties
    that can be used for optimization by the client
    
    :var lovUsage: Indicates if LOV is exhaustive (=1) or suggestive(=2) or Range (=3)
    :var style: Possible values are Standard, Range, Hierarchical, Interdependent and Coordinated
    Standard          - A simple list of values
    Interdependent - An interdependent  list of values, where each value has a  nested list of values. A list of States
    would have a list of Cities for each State. For this style of LOV the dependentProps will have a list of property
    names that are associated with each level of the LOV hierarchy
    Hierarchical      - Same as the Interdependent, but only the last level of values is associated with a property
    Coordinated    - This is similar to Interdependent; however levels 2-N will only
    have a single value. When the user selects a value from the first level LOV,
    the system can then fill property values for all levels
    Range - Subset (ranges) of valid values in terms of upper and lower ranges
    :var columnNames: Names of the columns when displayed in clients
    :var descriptionsAttached: This is a list of Boolean values that indicates if the description for each of the
    column properties is attached
    :var dependendProps: Names of interdependent properties. If the LOV is not an interdependent or coordinated LOV,
    this list will be empty
    :var rangeUpperLimit: Upper limit for Range LOV. This is not applicable to any other style of LOV
    :var rangeLowerLimit: Lower limit for Range LOV. This is not applicable to any other style of LOV
    """
    lovUsage: int = 0
    style: str = ''
    columnNames: LOVColumnNames = None
    descriptionsAttached: List[bool] = ()
    dependendProps: List[str] = ()
    rangeUpperLimit: str = ''
    rangeLowerLimit: str = ''


@dataclass
class LOVColumnNames(TcBaseObj):
    """
    Structure containing column names for the LOV value property, LOV description property and the filter attributes
    
    :var lovValueProp: The attribute on the object to be used as the LOV value. When the user selects a row from the
    list of values in the dynamic LOV widget (an item for example), this configuration point tells the system which
    attribute to use as the LOV value. In case of Static LOVs, the name of the property is returned as "lov_value". In
    case of Dynamic LOVs, it is a name as specified in BMIDE.
    :var lovDescrProp: The attribute on the object to be used as the LOV value description. When the user selects a row
    from the list of values in the dynamic LOV widget (an item for example), this configuration point tells the system
    which attribute to use as the LOV value description. In case of Static LOVs, the name of the property is returned
    as "lov_value_description". In case of Dynamic LOVs, it is a name as specified in BMIDE. It can be have empty value
    if it is not specified by BMIDE administrator.
    :var filterProperties: The filter properties would appear as additional columns along with the LOV Value and LOV
    description in the Dynamic LOV
    :var displayNames: Displayable names for each of lovValueProp, lovDescrProp, filterProperties that clients can use
    to display the same
    :var columnManagementFlags: Specifies the UI characteristics such as sortability and filterability, of the filter
    columns along with the LOV Value and LOV Description columns. The values of these characteristics are provided as
    bit values. At present, only the first two bits are populated, as listed below. Rest of the bits are reserved for
    future use.
    The first bit indicates sortability of the column. Value "0" indicates it is not sortable, while value "1"
    indicates it is sortable.
    The second bit indicates if the column is filterable. Value "0" indicates it is not filterable, while value "1"
    indicates it can be filtered.
    """
    lovValueProp: str = ''
    lovDescrProp: str = ''
    filterProperties: List[str] = ()
    displayNames: StringMap = None
    columnManagementFlags: StringIntMap = None


@dataclass
class LOVData(TcBaseObj):
    """
    This data structure is not for end user consumption. Data in this structure will be used by server for returning
    the next set of LOV values
    
    :var style: Possible values are Standard, Dynamic, Range, Hierarchical, Interdependent and Coordinated
    :var filterData: Filter critieria and other search data.
    :var unProcessedObjects: These are the list of UIDs that will be processed by the server in subsequent calls to get
    next set of LOV values
    :var additionalValuesSkipped: Boolean flag to indicate if additional UIDs (Values in static LOV) are skipped or not
    :var currentIndex: Current index of the LOV results that have been processed.
    :var lovs: LOVs of Dynamic LOV which is being evaluated
    """
    style: str = ''
    filterData: LovFilterData = None
    unProcessedObjects: List[str] = ()
    additionalValuesSkipped: bool = False
    currentIndex: int = 0
    lovs: List[ListOfValues] = ()


@dataclass
class LOVInput(TcBaseObj):
    """
    This represents the operation data.  Operations such as Create, Edit, Revise, Save As, Search or any other
    operation that requires the data to be passed generically to the LOV service operations  have the property values
    represented through the LOVInput for computing a LOV.
    
    :var owningObject: Owning object for the operation in context.
    a. Edit operation - Object being edited.
    b. Save operation - Object being saved.
    c. Revise operation - Object being revised.
    d. SaveAs operation - Object being copied.
    e. Search operation - Saved Query Object for searching.
    f. If an operation does not have an object, specify the value as null and ensure boName is passed for the same. For
    example, during creation, client does not have an object. Therefore specify the business object name of the object
    being created.  For example, if Item object is being created, specify the boName as "Item" and operationName as
    "Create".
    :var boName: Name of the source business object. For example, Item is the source business object for Item
    Descriptors. If the owningObject is not null, then it can be empty. Server can determine the business object name
    from the owningObject. It is mandatory for Create operation where owningObject is null
    :var operationName: Name of the operation  being performed. Valid names are Create, Revise, SaveAs, Edit, Search,
    Save
    :var propertyValues: A map of property names and values (string, vector<string>). The client is responsible for
    converting the values of the different property types (int, float, date .etc) to a string using the appropriate
    toXXXString functions in the SOA client  framework's Property class. Single valued properties will have a single
    value in the value vector, while Multi-valued properties will have multiple values in the value vector.
    """
    owningObject: BusinessObject = None
    boName: str = ''
    operationName: str = ''
    propertyValues: PropertyValues = None


@dataclass
class LOVSearchResults(TcBaseObj):
    """
    This structure contains the LOV results from the getInitialLOVValues or getNextLOVValues operations
    
    :var lovValues: This is a list of LOVValueRow objects. Each LOVValueRow object represents a single row of the LOV
    results. It includes the LOV value property, the description property and all the filter properties (the filter
    properties are the ones whose values are used for filtering the search results based on user input)
    :var moreValuesExist: true indicates there are more values available which will can be retrieved by a call to the
    getNextValues operation
    :var behaviorData: LOV data used to define the UI component behavior. This includes data such as LOV usage, Style,
    Lov Column Names. Additionally it  contains interdependent properties that can be used for optimization by the
    client
    :var lovData: If moreValuesExist is true, this object is passed as input to the getNextValues operation to get the
    next list of LOV search results
    :var serviceData: The ServiceData
    """
    lovValues: List[LOVValueRow] = ()
    moreValuesExist: bool = False
    behaviorData: LOVBehaviorData = None
    lovData: LOVData = None
    serviceData: ServiceData = None


@dataclass
class LOVValueRow(TcBaseObj):
    """
    This represents a row of LOV values. It includes the internal and display values for the various columns for each
    LOV value
    
    :var uid: UID of the object. This applies to dynamic LOVs.  Server sends valid UID for dynamic LOV and empty in
    other LOV cases.. Client can send the same UID when a value is selected to validateLOVValueSelection operation for
    effective validation. This is empty for for non dynamic LOVs
    :var propInternalValues: The internal values of all the properties on a single row of the LOV search results. The
    parseXXX functions in the SOA framework class can be used to retrieve the values for the specific property types
    :var propInternalValueTypes: value type map for each property which has internal values, PROP_untyped (0) No Value
    type PROP_char (1) Value is a single character PROP_date (2) Value is a date PROP_double (3) Value is a double
    PROP_float (4) Value is a float PROP_int (5) Value is an integer PROP_logical (6) Value is a logical PROP_short (7)
    Value is a short PROP_string (8) Value is a character string PROP_typed_reference (9) Value is a typed reference
    PROP_untyped_reference (10) Value is an untyped reference PROP_external_reference (11) Value is an external
    reference PROP_note (12) Value is a note PROP_typed_relation (13) Value is a typed relation PROP_untyped_relation
    (14) Value is an untyped relation
    :var propDisplayValues: The display values of all the properties on a single row of the LOV search results
    :var childRows: Next level of row values in case of hierarchical LOV. This is recursive and can go down multiple
    levels in the hierarchy
    """
    uid: str = ''
    propInternalValues: PropertyValues = None
    propInternalValueTypes: StringIntMap = None
    propDisplayValues: PropertyValues = None
    childRows: List[LOVValueRow] = ()


@dataclass
class LovFilterData(TcBaseObj):
    """
    Filter Data used in InitialLOVData.
    
    :var filterString: The desired string used to filter the search results. For example, if "Green" is entered as a
    filter string, the results returned for LOV values will include the LOV values that match the query criteria AND
    contain the string "Green" in the LOV Description or any of the filter attributes. Case sensitive nature is
    honoured based on TC_ignore_case_on_search preference.
    :var maxResults: Maximum number of LOV results that server should retrieve from the database
    :var numberToReturn: Number of objects to be processed in case of dynamic LOVs to return LOV values and in other
    LOV cases it is to return the number of LOV values from the LOV results. This number must be less than or equal to
    maxResults
    :var sortPropertyName: Property name on which to sort the results. This is optional
    :var order: 1=sort in ascending order, 2=sort in descending order. Ignored if sortPropertyName is null.
    """
    filterString: str = ''
    maxResults: int = 0
    numberToReturn: int = 0
    sortPropertyName: str = ''
    order: int = 0


@dataclass
class ValidateLOVValueSelectionsResponse(TcBaseObj):
    """
    Response structure indicating validity of LOV value selection and containing updated property values and
    interdependent LOV values
    
    :var propHasValidValues: Indicates whether input property has valid values
    :var dependentPropNames: Names of dependent properties server modified to be updated by client as a results of
    dependency with input property selection. This can be empty.
    :var updatedPropValues: Updated property values. It contains both internal and display values of the updated
    properties.  It can be empty.
    :var serviceData: The service data.
    """
    propHasValidValues: bool = False
    dependentPropNames: List[str] = ()
    updatedPropValues: LOVValueRow = None
    serviceData: ServiceData = None


"""
Map (string, vector<string>) that is a generic container that represents property values. The key is the property name and the value is the string representation of the property value.
"""
PropertyValues = Dict[str, List[str]]


"""
Maps string keys to integer values
"""
StringIntMap = Dict[str, int]


"""
Map of Strings
"""
StringMap = Dict[str, str]
