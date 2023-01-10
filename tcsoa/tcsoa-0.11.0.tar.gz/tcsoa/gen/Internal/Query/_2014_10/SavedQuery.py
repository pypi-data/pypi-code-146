from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanQuery
from typing import List
from tcsoa.gen.Internal.Query._2012_02.SavedQuery import SavedQuerySortAttribute
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SavedQueryClause3(TcBaseObj):
    """
    Holds the definition of a single saved query clause.  A query clause represents a single attribute that the end
    user can supply as search criteria.  Each saved query is made up of any number of ordered clauses.  Each attribute
    in this list is displayed to the end user allowing them to enter a search value.  Information about an attribute is
    attached with LOV or not also specified.  More common information includes the L10N key to be used when converting
    the attribute name for display to the user.  Also included is the logical operation to be used when evaluating this
    attribute in the saved query, and the comparison to be made between the user entered value and the value in the
    database.
    
    :var attributeName: Name of the attribute.
    :var entryL10NKey: The L10N key used when displaying this attribute to the user.
    :var entryNameDisplay: The translated version of the L10N key that will be displayed to the user.
    :var logicalOperator: Logical operator used when evaluating the clause.  This can be "AND", "OR" or "".
    :var mathOperator: Math operation to use when evaluating the clause.  This can be "=", "!=", ">", ">=", "<", "<=",
    "IS_NULL" or "IS_NOT_NULL".
    :var defaultInternalValue: Default internal value used for this attribute.
    :var defaultDisplayValue: Default display value used for this attribute.
    :var hasLOV: Indicates whether a LOV is attached to this attribute or not.
    :var keyLovId: Id of the key LOV for this attribute.
    :var attributeType: Type of attribute as defined in the AttributeDescriptor definition. Currently used to determine
    the correct attribute type to decide how the particular clause should be handled in the search form.
    """
    attributeName: str = ''
    entryL10NKey: str = ''
    entryNameDisplay: str = ''
    logicalOperator: str = ''
    mathOperator: str = ''
    defaultInternalValue: str = ''
    defaultDisplayValue: str = ''
    hasLOV: bool = False
    keyLovId: int = 0
    attributeType: int = 0


@dataclass
class SavedQueryDefinition3(TcBaseObj):
    """
    Contains the clauses and sort attributes that make up a saved query definition.  Each of the search clauses and
    sort attributes in the definition are order dependent.  The order of the clause attributes indicates how the 'AND'
    and 'OR' logic of the saved query will be evaluated.  The order of the sort attributes indicates the precedence of
    the results sorting.
    
    :var query: ImanQuery definition on the server.
    :var clauses: A list of ordered set of clauses that make up the query definition.  Each clause represents an
    attribute where the user can enter a value.  Each of these values is used to make up the overall query.
    :var sortAttributes: Optional list of attributes to be used for default sorting.  The ascending or descending order
    is included in the definition.  The order that the attributes appear in the vector indicate the order that they
    will impact the sorting.
    """
    query: ImanQuery = None
    clauses: List[SavedQueryClause3] = ()
    sortAttributes: List[SavedQuerySortAttribute] = ()


@dataclass
class DescribeSavedQueryDefnResponse3(TcBaseObj):
    """
    Holds the detailed definition data for the requested saved queries.  Each saved query definition will include
    search clauses and default sort attributes.  Each search clause attribute will be shown to the user during a query,
    and will allow the user to enter a value.  Each clause can have a default value and operators indicating how the
    value is evaluated.  The sort attributes allow the saved query to define the default sorting to use when this query
    is executed.  This can be altered by the end user from the sort dialog.
    
    :var definitions: A list of Saved query definitions data.  One definition is returned for each ImanQuery passed as
    input.  Each definition includes all the search criteria and sort attributes defined for each saved query.
    :var serviceData: Returned service data
    """
    definitions: List[SavedQueryDefinition3] = ()
    serviceData: ServiceData = None
