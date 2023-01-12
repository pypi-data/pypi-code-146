from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchFilterField, ObjectsGroupedByProperty
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ColumnConfig2(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that was used to finalize the columns to be returned back. Supported values are:
    "Intersection", "Union" and "Configured".
    :var columns: List of column details.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo2] = ()


@dataclass
class SearchFilter3(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Supported values are "StringFilter", "DateFilter",
    "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var colorValue: The color of the Search Filter.
    :var stringDisplayValue: The display value for a string filter. This field is applicable only if the
    "searchFilterType" field is set to "StringFilter".
    :var startDateValue: The starting value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter"
    :var endDateValue: The ending value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter"
    :var startNumericValue: The starting value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var endNumericValue: The ending value for a numeric filter. This field is applicable only if the searchFilterType
    is set to "NumericFilter".
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: If true, the Search Filter was previously selected; otherwise, the Search Filter was not previously
    selected.
    :var startEndRange: The interval used to generate a range facets. E.g for Date range facets, +1DAY, +1WEEK, +1MONTH
    , +1YEAR are acceptable values. Note: Currently this value is not being used. To be supported in the future.
    """
    searchFilterType: str = ''
    stringValue: str = ''
    colorValue: str = ''
    stringDisplayValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


@dataclass
class SearchResponse3(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var searchResults: List of ViewModel business objects obtained after performing a search.
    :var totalFound: Total number of ViewModel business objects found.
    :var propDescriptors: List of ViewModelPropertyDescriptors required to render the object properties in stylesheet.
    :var totalLoaded: Total number of ViewModel business objects loaded.
    :var searchFilterMap3: A map (string, list of SearchFilter2) containing the list of search filters for each search
    filter field based on the search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var objectsGroupedByProperty: The structure containing an internal property name and a map of objects to the
    property group id. It also contains a list of unmatched objects which do not match any group.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The service data object.
    :var endIndex: Cursor end position for the results returned so far. This value, 'endIndex', correlates with
    'startindex' in SearchInput.
    """
    searchResults: List[ViewModelObject] = ()
    totalFound: int = 0
    propDescriptors: List[ViewModelPropertyDescriptor] = ()
    totalLoaded: int = 0
    searchFilterMap3: SearchFilterMap3 = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig2 = None
    serviceData: ServiceData = None
    endIndex: int = 0


@dataclass
class ViewModelObject(TcBaseObj):
    """
    Service operation output structure to store the Teamcenter BusinessObject and its associated View model properties
    to be displayed in the view.
    
    :var modelObject: Teamcenter BusinessObject that was searched for and to be rendered in the view.
    :var viewModelProperties: List of ViewModelProperty structures
    """
    modelObject: BusinessObject = None
    viewModelProperties: List[ViewModelProperty] = ()


@dataclass
class ViewModelProperty(TcBaseObj):
    """
    ViewModelProperty represents a property that is displayed in the view, it can be simple property, runtime property,
    compound property or dynamic compound property.
    
    :var propertyName: Property name
    :var values: Real value for the property, the values are converted to strings for other value types such as date,
    double, Boolean or referenced objects.
    :var displayValues: Display values for the property
    :var intermediateObjectUids: List of UID's of intermediate objects across the property traversal path.
    :var srcObjLsd: Last saved date of source object
    :var isModifiable: The flag that indicates if the property is modifiable
    """
    propertyName: str = ''
    values: List[str] = ()
    displayValues: List[str] = ()
    intermediateObjectUids: List[str] = ()
    srcObjLsd: datetime = None
    isModifiable: bool = False


@dataclass
class ViewModelPropertyDescriptor(TcBaseObj):
    """
    Represents the property descriptor details for a ViewModelProperty, the definition of ViewModelPropertyDescriptor
    is taken from the property descriptor of the source object property.
    
    :var srcObjectTypeName: Business object type name of the source object on which the property is defined.
    :var propertyName: Name of the property, it includes the traversal path for dynamic compound property. It is same
    as the propertyName in ViewModelProperty.
    :var valueType: Indicates the value type for the property, valid values are: 
     value - type 
     0 . PROP_untyped -  No Value type  
     1 . PROP_char - Value is a single character * 
     2 . PROP_date - Value is a date  
     3 . PROP_double - Value is a double  
     4 . PROP_float - Value is a float  
     5 . PROP_int -  Value is an integer  
     6 . PROP_logical -  Value is a logical  
     7 . PROP_short - Value is a short  
     8 . PROP_string - Value is a character string  
     9 . PROP_typed_reference - Value is a typed reference  
    10 . PROP_untyped_reference - Value is an untyped reference  
    11 . PROP_external_reference - Value is an external reference  
    12 . PROP_note - Value is a note  
    13 . PROP_typed_relation - Value is a typed relation  
    14 . PROP_untyped_relation - Value is an untyped relation etc. 
    This is from the source object property descriptor.
    :var isArray: Indicates if the property is a single value property or an array, this is from the source object
    property descriptor.
    :var propConstants: Map ( string, /string ) consisting of propertyConstant name and value pairs, this is from the
    source object property descriptor.
    :var displayName: Display name of the property, if columnDisplayNameKey is defined in column config, the display
    name is the values corresponds to it in text server; otherwise, the displayName is the source object property
    display name.
    :var lovCategory: Indicates the LOV category, if the property is attached to LOV.
    :var lov: LOV reference associated with the property, this is from the source object property descriptor.
    :var maxArraySize: Maximum number of elements allowed in case of array property, this is from the source object
    property descriptor.
    :var maxLength: Max allowed length for the property if property is string property.
    :var propertyType: Indicates the value type for the property, valid values are:
    value - type 
    0 . PROP_unknown  - Property type is Unknown  
    1 . PROP_attribute  - Based on a POM Attribute (int, string, ...)  
    2 . PROP_reference -  Based on a POM Reference  
    3 . PROP_relation - Based on an ImanRelation  
    4 . PROP_compound - Based on a property from another Type  
    5 . PROP_runtime - Based on a computed value  
    6 . PROP_operationinput - Based on the source property on a BO  
    This is from the source object property descriptor.
    """
    srcObjectTypeName: str = ''
    propertyName: str = ''
    valueType: int = 0
    isArray: bool = False
    propConstants: ViewModelPropertyConstantsMap = None
    displayName: str = ''
    lovCategory: int = 0
    lov: BusinessObject = None
    maxArraySize: int = 0
    maxLength: int = 0
    propertyType: int = 0


@dataclass
class ColumnDefInfo2(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be hidden and the column
    sort order.
    
    :var displayName: The display name for the value displayed in the column header.
    :var typeName: The business object type for the value displayed in the column. This can be any valid Teamcenter
    business object type.
    :var propertyName: The property name for the value displayed in the column.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var hiddenFlag: If true, the column should be hidden on the client user interface.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    """
    displayName: str = ''
    typeName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap3 = Dict[str, List[SearchFilter3]]


"""
Map to store the Property constant name and value pair
"""
ViewModelPropertyConstantsMap = Dict[str, str]
