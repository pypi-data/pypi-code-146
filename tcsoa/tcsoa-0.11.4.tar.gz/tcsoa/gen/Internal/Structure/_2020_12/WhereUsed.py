from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RevisionRule
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ColumnConfig(TcBaseObj):
    """
    Output Column configuration computed by server
    
    :var columnConfigId: Column configuration ID.
    :var operationType: Operation type used for determining columns. Supported values are: "Union" and "Intersection".
    :var columns: List of available columns
    :var typesForArrange: The valid Teamcenter types used for fetching the columns.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()
    typesForArrange: List[str] = ()


@dataclass
class ColumnConfigInput(TcBaseObj):
    """
    Input required to compute column configuration information
    
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database. This value must match the value of fnd0ClientName property. For example: The client name for Active
    Workspace is "AWClient".
    :var hostingClientName: Specifies the name of a hosting client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases. This value must match a value of the fnd0ClientName property. For example:
    If client A is integrated with client B and the user can invoke client B commands from within client A, the input
    would specify client A as hosting client and client B as the client. If the caller wanted native commands for
    client A, client A would be specified as client and hosting client would be empty.
    :var clientScopeURI: The unique name of the client scope containing column configurations.
    :var operationType: The operation that needs to be applied to finalize the columns to be returned. Valid values are:
    "Intersection" - Gets the intersection of the columns for the types found in search results.         
    "Union" - Gets all the columns for the types found in search results.
    :var columnsToExclude: List of columns which should be excluded from the final list being returned. The
    value provided should be in the format "TypeName.PropertyName". Both type name and property name should be internal
    values. For example: ItemRevision.sequence_id, where '.' is the delimiter.
    """
    clientName: str = ''
    hostingClientName: str = ''
    clientScopeURI: str = ''
    operationType: str = ''
    columnsToExclude: List[str] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Detailed information about individual columns
    
    :var displayName: The display name for the property to be displayed in the column header.
    :var assosiatedTypeName: The business object type for the value displayed in the column. This can be any valid
    Teamcenter business object type.
    :var propertyName: The internal property name for the value displayed in the column
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500
    :var columnOrder: The column order value is used to arrange the columns in order
    :var hiddenFlag: If true, the column to be hidden on the client user interface
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    """
    displayName: str = ''
    assosiatedTypeName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''


@dataclass
class Cursor(TcBaseObj):
    """
    This gives information about returned page.
    
    :var resultsReturned: Number of results returned so far
    :var endReached: If true, end is reached; otherwise, end is not yet reached and there are more results to be
    returned.
    :var startUIDLevel: The startUIDLevel helps where used to determine the previous page to return
    :var endUIDLevel: The endUIDLevel helps where used to determine the next page to return
    :var startObjectUid: The startObject helps where used to determine the previous page to return. null allowed.
    :var endObjectUid: The endObject helps where used to determine the next page to return. null allowed
    """
    resultsReturned: int = 0
    endReached: bool = False
    startUIDLevel: int = 0
    endUIDLevel: int = 0
    startObjectUid: str = ''
    endObjectUid: str = ''


@dataclass
class ResultNode(TcBaseObj):
    """
    Contains parent UID and boolean indicating if parent is further parents.
    
    :var resultObject: BusinessObject under which input ItemRevision is created as child component.
    :var hasParent: If true, there are parents for this node; otherwise, this node does not have parents and is a root
    node.
    """
    resultObject: BusinessObject = None
    hasParent: bool = False


@dataclass
class WhereUsedInput(TcBaseObj):
    """
    Input required for getWhereUsedInfo SOA operation
    
    :var inputObject: The ItemRevision object for which &lsquo;where used&rsquo; information is to be retrieved.  This
    is mandatory input.
    :var revisionRule: The RevisionRule object to configure parents. If null, default RevisionRule object is used from
    preference: "TC_config_rule_name".
    :var additionalInfo: Additional set of information required by operation in key value pair. Future scope.  This
    would be a map of string to vector of string.
    :var cursorInfo: A map (BusinessObject, Cursor) of child BusinessObject to its cursor information.
    :var pageSize: Number of parent BusinessObjects to be returned.
    :var columnConfigInput: Column configuration input
    """
    inputObject: BusinessObject = None
    revisionRule: RevisionRule = None
    additionalInfo: AdditionalInfo = None
    cursorInfo: CursorMap = None
    pageSize: int = 0
    columnConfigInput: ColumnConfigInput = None


@dataclass
class WhereUsedOutput(TcBaseObj):
    """
    Output from getWhereUsedInfo SOA operation
    
    :var childToParentMap: A map (BusinessObject, list of ResultNode) of child BusinessObject as key and list of its
    parent ResultNodes as value.
    :var cursorInfo: A map (BusinessObject, Cursor) of Child BusinessObject to its Cursor information like, number of
    results returned for that child and if end has reached for that child.
    :var additionalInfo: Additional set of information SOA operation wants to send to client
    :var columnConfigOutput: Column configuration containing  BusinessObject type, property internal name, display
    name, column width based input column configuration.
    :var serviceData: ServiceData containing added, updated, deleted objects along with partial errors, if any.
    """
    childToParentMap: ChildToParentMap = None
    cursorInfo: CursorMap = None
    additionalInfo: AdditionalInfo = None
    columnConfigOutput: ColumnConfig = None
    serviceData: ServiceData = None


"""
Additional set of information SOA operation wants to send to client
"""
AdditionalInfo = Dict[str, List[str]]


"""
A map (BusinessObject, list of ResultNode) of child BusinessObject as key and list of its parent ResultNodes as value.
"""
ChildToParentMap = Dict[BusinessObject, List[ResultNode]]


"""
A map (BusinessObject, Cursor) of Child BusinessObject to its Cursor information like, number of results returned for that child and if end has reached for that child.
"""
CursorMap = Dict[str, Cursor]
