from __future__ import annotations

from tcsoa.gen.BusinessObjects import ListOfValues, ImanQuery
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SavedQueryClause(TcBaseObj):
    """
    Holds the definition of a single saved query clause.  A query clause represents a single attribute that the end
    user can supply as search criteria.
    
    :var attributeName: Name of the attribute.
    :var entryName: The L10N key used when displaying this attribute to the user.
    :var attributeType: Type of attribute as defined in the AttributeDescriptor definition.
    :var entryNameDisplay: The translated version of the L10N key that will be displayed to the user.
    :var logicalOperation: Logical operation used when evaluating the clause.  This can be "AND", "OR" or "".
    :var mathOperation: Math operation to use when evaluating the clause.  This can be "=", "!=", ">", ">=", "<", "<=",
    "IS_NULL" or "IS_NOT_NULL".
    :var defaultValue: Default value used for this attribute.
    :var lov: LOV used with this clause.
    :var attachedSpecifier: The attached specifier for the LOV.
    :var dependentIndexes: All the dependent indexes for this clause.
    :var keyLovId: Id of the key LOV for this attribute.
    """
    attributeName: str = ''
    entryName: str = ''
    attributeType: int = 0
    entryNameDisplay: str = ''
    logicalOperation: str = ''
    mathOperation: str = ''
    defaultValue: str = ''
    lov: ListOfValues = None
    attachedSpecifier: int = 0
    dependentIndexes: List[int] = ()
    keyLovId: int = 0


@dataclass
class SavedQueryDefinition(TcBaseObj):
    """
    Contains the clauses and sort attributes that make up a saved query definition.  Each of the search clauses and
    sort attributes in the definition are order dependent.  The order of the clause attributes indicates how the 'AND'
    and 'OR' logic of the saved query will be evaluated.  The order of the sort attributes indicates the precedence of
    the results sorting.
    
    :var query: Query definition on the server.
    :var clauses: The ordered set of clauses that make up the query definition.  Each clause represents an attribute
    where the user can enter a value.  Each of these values is used to make up the overall query.
    :var sortAttributes: Optional list of attributes to be used for default sorting.  The ascending or descending order
    is included in the definition.  The order that the attributes appear in the vector indicate the order that they
    will impact the sorting.
    """
    query: ImanQuery = None
    clauses: List[SavedQueryClause] = ()
    sortAttributes: List[SavedQuerySortAttribute] = ()


@dataclass
class SavedQuerySortAttribute(TcBaseObj):
    """
    Holds the definition of an attribute to be used for sorting the results of a saved query.  The order to be used in
    the sort is included along with the displayed name.
    
    :var attributeName: Name of the attribute.
    :var entryName: The L10N key used when displaying the attribute to the user.
    :var entryNameDisplay: The translated version of the L10N key.
    :var orderBy: The order to sort by.  This can either be "ASCENDING" or "DESCENDING".
    """
    attributeName: str = ''
    entryName: str = ''
    entryNameDisplay: str = ''
    orderBy: str = ''


@dataclass
class DescribeSavedQueryDefinitionInput(TcBaseObj):
    """
    Contains the input criteria required to find the saved query definition.  The main input here is the saved query
    object.  'true' should be the default substituteKeyword value.
    
    :var query: Saved query whos definition data is being requested.
    :var substituteKeyword: Indicates that keywords should be substituted when returning the definition.  Will return
    the attributes type display name instead of the raw defined default value for the clause. (For object_type and
    type_name attributes)
    """
    query: ImanQuery = None
    substituteKeyword: bool = False


@dataclass
class DescribeSavedQueryDefinitionsResponse(TcBaseObj):
    """
    Holds the detailed definition data for the requested saved queries.  Each saved query definition will include
    search clauses and default sort attributes.  Each search clause attribute will be shown to the user during a query,
    and will allow the user to enter a value.  Each clause can have a default value and operators indicating how the
    value is evaluated.  The sort attributes allow the saved query to define the default sorting to use when this query
    is executed.  This can be altered by the end user from the sort dialog.
    
    :var definitions: Saved query definitions data.  One definition is returned for each ImanQuery passed as input. 
    Each definition includes all the search criteria and sort attributes defined for each saved query.
    :var serviceData: Returned service data.
    """
    definitions: List[SavedQueryDefinition] = ()
    serviceData: ServiceData = None
