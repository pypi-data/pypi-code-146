from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TableDefinition, Dataset, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetItemFromAttributeInfo(TcBaseObj):
    """
    Input parameters for retrieving Item and ItemRevision objects based on attribute keys
    
    :var itemAttributes: A map of attribute names and values ('string/string') used to peform the search. Typical keys
    are "item_id", "object_type", "object_name", "owning_organization", and "date_released".  A special key, "rev_id",
    may also be used to specify a single related ItemRevision object to retrieve. This "rev_id" key is effective only
    if the nRev parameter equals zero.
    :var revIds: A list of revision ID strings specifying ItemRevison objects to retrieve. This parameter only takes
    effect if the 'nRev' parameter equals zero. This list of revision IDs can be used independent of the "rev_id" key
    value in 'itemAttributes'
    """
    itemAttributes: GetItemAttributeMap = None
    revIds: List[str] = ()


@dataclass
class GetItemFromAttributeItemOutput(TcBaseObj):
    """
    This data structure contains an Item and a list of related ItemRevision objects retrieved by a
    'getItemFromAttribute' operation.
    
    :var item: The retrieved Item object
    :var itemRevOutput: The list of related ItemRevision objects
    """
    item: Item = None
    itemRevOutput: List[GetItemFromAttributeItemRevOutput] = ()


@dataclass
class GetItemFromAttributeItemRevOutput(TcBaseObj):
    """
    Contains a single ItemRevision retrieved by the getItemFromAttribute operation
    
    :var itemRevision: The retrieved ItemRevision
    :var datasets: list of Datasets associated with the ItemRevision
    """
    itemRevision: ItemRevision = None
    datasets: List[Dataset] = ()


@dataclass
class GetItemFromAttributeResponse(TcBaseObj):
    """
    The return structure from from 'getItemFromAttribute' operation. Contains a list of
    'GetItemFromAttributeItemOutput' structures.
    
    :var output: A list of found Item and ItemRevision objects
    :var serviceData: Standard 'ServerData' member with any returned error codes and messages
    """
    output: List[GetItemFromAttributeItemOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetTablePropertiesResponse(TcBaseObj):
    """
    Structure holds response from getTableProperties.
    
    :var tableInfo: This vector contains a list of TableInfo, and each TableInfo contains information pertaining to the
    specific Table it references.
    :var serviceData: The ServiceData structure is used to return the updated Table objects in the update section and
    also any errors encountered during this operation call.
    """
    tableInfo: List[TableInfo] = ()
    serviceData: ServiceData = None


@dataclass
class TableCellInfo(TcBaseObj):
    """
    This structure contains Table Cell Info.
    
    :var row: This specifies the row number of the cell in the Table.
    :var column: This specifies the column number of the cell in the Table.
    :var desc: This is a string which can be used to capture a description for the cell.
    :var value: This is a structure which contains information pertaining to a value on the cell.
    """
    row: int = 0
    column: int = 0
    desc: str = ''
    value: TableCellValueTypeInfo = None


@dataclass
class TableCellValueTypeInfo(TcBaseObj):
    """
    This structure contains table cell value type info.
    
    :var type: This specifies the data type that the cell of the table can hold. The type specified in this string,
    should be one of the below supported type:
    - TableCellInt
    - TableCellString
    - TableCellDouble
    - TableCellLogical
    - TableCellHex
    - TableCellSED
    - TableCellBCD
    - TableCellDate
    
    
    :var strValues: A list of values
    """
    type: str = ''
    strValues: List[str] = ()


@dataclass
class TableDefInfo(TcBaseObj):
    """
    This structure contains Table Definition Info.
    
    :var rows: This specifies the number of rows in the Table.
    :var columns: This specifies the number of columns in the Table.
    :var rowLabels: This is a vector of strings, each string representing the labels corresponding to a row in the
    Table.
    :var colLabels: This is a vector of strings, each string representing the labels corresponding to a column in the
    Table.
    :var tableDef: tableDef is of type TableDefinition
    """
    rows: int = 0
    columns: int = 0
    rowLabels: List[str] = ()
    colLabels: List[str] = ()
    tableDef: TableDefinition = None


@dataclass
class TableInfo(TcBaseObj):
    """
    Table Info
    
    :var tableObject: The Business Object corresponding to the Table
    :var tableDefInfo: Meta information about the Table such as the row labels, columns labels, and its size are
    contained in this structure.
    :var tableCells: This is a vector of the structures that contain information pertaining to each of the cells in the
    Table.
    """
    tableObject: BusinessObject = None
    tableDefInfo: TableDefInfo = None
    tableCells: List[TableCellInfo] = ()


"""
A hash map containing the key-value pairs specifying the Item objects to search for. Used by the 'GetItemFromAttributeInfo' structure to store the Item search criteria.
"""
GetItemAttributeMap = Dict[str, str]
