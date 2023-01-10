from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FormAttributeExpression(TcBaseObj):
    """
    FormAttributeExpression contains information to search
    on a single Form Attribute within a containing SearchExpressionInfo
    object.
    The search on the multiple values specified within one FormAttributeExpression are
    combined with a logical 'OR' operation.
    
    :var isItemForm: Item or ItemRevision form
    :var relationType: The Form relation type
    :var formType: Form type to be searched
    :var attributeName: The attribute of the above Form type
    to be searched
    :var attributeType: The type of the attribute to be searched on
    :var queryOperator: operator to use for search value comparison
    :var values: The values to test for
    """
    isItemForm: bool = False
    relationType: BusinessObject = None
    formType: BusinessObject = None
    attributeName: str = ''
    attributeType: AttributeType = None
    queryOperator: QueryOperator = None
    values: AttributeValues = None


@dataclass
class InClassExpression(TcBaseObj):
    """
    InClassExpression
    
    :var inClassClassNames: inClassClassNames
    :var inClassAttributeIDs: inClassAttributeIDs
    :var inClassAttributeValues: inClassAttributeValues
    """
    inClassClassNames: List[str] = ()
    inClassAttributeIDs: List[int] = ()
    inClassAttributeValues: List[str] = ()


@dataclass
class LogicalDesignatorAttribute(TcBaseObj):
    """
    an object that represents a single LD attribute.
    This type will be used in a vector that will represent a Logical Designator .
    
    :var name: the attribute name
    :var value: the attribute value
    """
    name: str = ''
    value: str = ''


@dataclass
class MFGSearchCriteria(TcBaseObj):
    """
    TBD
    
    :var objectTypes:  the types of objects to search
    :var logicalDesignator: logical designator data
    :var refinements: refinements on the search
    """
    objectTypes: List[BusinessObject] = ()
    logicalDesignator: List[LogicalDesignatorAttribute] = ()
    refinements: List[MFGSearchRefinementSet] = ()


@dataclass
class MFGSearchRefinement(TcBaseObj):
    """
    refinement on the search
    
    :var relatedScopes: a vector of additional scopes. These are not the scopes in which we expect to find the results.
    These are the scopes from which we start to impose the limitations.
    :var relations: a vector specifying the list of relations between the related scopes to the "searched" objects
    """
    relatedScopes: List[BusinessObject] = ()
    relations: List[RelationInfo] = ()


@dataclass
class MFGSearchRefinementSet(TcBaseObj):
    """
    TBD
    
    :var refinements: a vector of refinements. The refinements are combined with logical 'OR' between them
    """
    refinements: List[MFGSearchRefinement] = ()


@dataclass
class AttributeExpression(TcBaseObj):
    """
    AttributeExpression encapsulates information to build a query on
    the attribute of an Item or ItemRevision or their sub-classes in the structure search scope.
    * A set of these attribute expressions is contained
    inside a SearchExpressionInfo object.
    Search on multiple values specified within one AttributeExpression are
    combined with a logical 'OR' operation.
    
    :var className: Item or ItemRevision or their sub-classes
    :var attributeName: The attribute of the above 'className'
    to be searched on
    :var attributeType: The type of the attribute to be searched on
    :var queryOperator: operator to use for search value comparison
    :var values: values
    """
    className: str = ''
    attributeName: str = ''
    attributeType: AttributeType = None
    queryOperator: QueryOperator = None
    values: AttributeValues = None


@dataclass
class OccurrenceNoteExpression(TcBaseObj):
    """
    OccurrenceNoteExpression contains information to search
    on a single occurrence note type within a containing SearchExpressionInfo
    object.
    The search on the multiple values specified within one OccurrenceNoteExpression are
    combined with a logical 'OR' operation.
    
    :var noteType: Occurrence note type to search
    :var queryOperator: operator to use for search value comparison
    :var values: The list of values to search for
    """
    noteType: str = ''
    queryOperator: QueryOperator = None
    values: List[str] = ()


@dataclass
class AttributeValues(TcBaseObj):
    """
    AttributeValues data structure specifies data values to be bound to the various search expressions for
    execution of the search. It encapsulates the values to be specified for each of the data types that
    can occur in any of the attribute search expressions.
    
    :var boolValues: boolean values that any of the accompanying set of search expressions may use
    :var intValues: integer values that any of the accompanying set of search expressions may use
    :var doubleValues: double values that any of the accompanying set of search expressions may use
    :var stringValues: string values that any of the accompanying set of search expressions may use
    :var dateValues: date values that any of the accompanying set of search expressions may use
    :var tagValues: tag values that any of the accompanying set of search expressions may use
    """
    boolValues: List[bool] = ()
    intValues: List[int] = ()
    doubleValues: List[float] = ()
    stringValues: List[str] = ()
    dateValues: datetime = None
    tagValues: List[BusinessObject] = ()


@dataclass
class PlaneZone(TcBaseObj):
    """
    Planezone defines a single plane to search against.
    
    :var xvalue: X value of the direction unit vector of the plane
    :var yvalue: Y value of the direction unit vector of the plane
    :var zvalue: Z value of the direction unit vector of the plane
    :var displacement: Plane displacement in metres along the direction vector specified above
    """
    xvalue: float = 0.0
    yvalue: float = 0.0
    zvalue: float = 0.0
    displacement: float = 0.0


@dataclass
class PlaneZoneExpression(TcBaseObj):
    """
    PlaneZoneExpression represents a 3D plane to search against. It may define a search for all parts that intersect
    with the plane, or a search
    for all parts on one side of the plane.
    
    :var planzeZone: planzeZone
    :var planeZoneOperator: Operator to use for expression
    """
    planzeZone: PlaneZone = None
    planeZoneOperator: PlaneZoneOperator = None


@dataclass
class ProximityExpression(TcBaseObj):
    """
    ProximityExpression specifies one set of proximity criteria. The search
    results from each bomLine are combined together using an 'OR' operation.
    
    :var bomLines: BOM lines around which to search
    :var distance: Proximity distance in metres from the outer surface of the BomLine geometry
    :var includeChildBomLines: includeChildBomLines
    """
    bomLines: List[BOMLine] = ()
    distance: float = 0.0
    includeChildBomLines: bool = False


@dataclass
class RelationInfo(TcBaseObj):
    """
    information about the relation
    
    :var relationName: the name of the relation
    :var matchType: the match type
    :var objectClass: the class from which the relation starts (e.g. MfgOperation)
    """
    relationName: str = ''
    matchType: MatchType = None
    objectClass: str = ''


@dataclass
class SavedQueryExpression(TcBaseObj):
    """
    SavedQueryExpression defines a search expression encapsulated as a Teamcenter saved-query that returns an Item,
    ItemRevision
    or any of their sub-types. The saved query may be a pre-defined out of the box saved query or one created using
    the Teamcenter QueryBuilder application
    
    :var savedQuery: Tag of an existing saved query
    :var entries: Attribute entries that are to be searched for
    :var values: Values of the above entries to be searched for
    """
    savedQuery: BusinessObject = None
    entries: List[str] = ()
    values: List[str] = ()


@dataclass
class SearchBox(TcBaseObj):
    """
    SearchBox defines a single box zone to search in. It contains the definition of an axis-aligned box
    and an accompanying transform to describe it orientation.
    
    :var xmin: Plane defining the minimum extent along the x-axis
    :var ymin: Plane defining the minimum extent along the y-axis
    :var zmin: Plane defining the minimum extent along the z-axis
    :var xmax: Plane defining the maximum extent along the x-axis
    :var ymax: Plane defining the maximum extent along the y-axis
    :var zmax: Plane defining the maximum extent along the z-axis
    :var transform: Transform defining the orientation of the box ( empty vector denotes identity transform )
    """
    xmin: float = 0.0
    ymin: float = 0.0
    zmin: float = 0.0
    xmax: float = 0.0
    ymax: float = 0.0
    zmax: float = 0.0
    transform: List[float] = ()


@dataclass
class SearchBySizeExpression(TcBaseObj):
    """
    SearchBySizeExpression defines a search for parts with bounding boxes that are larger than or smaller than
    a specified size
    
    :var largerThan: Search for larger than if this is set to true, smaller than if set to false
    :var diagonalLength: Length of the largest bounding box diagonal in metres
    """
    largerThan: bool = False
    diagonalLength: bool = False


@dataclass
class SearchExpressionSet(TcBaseObj):
    """
    SearchExpression data structure specifies the full set of search expressions that are to be used to perform a
    single structure search. Each one of the expressions provided are combined together using a logical 'AND' between
    them.
    
    :var itemAndRevisionAttributeExpressions: itemAndRevisionAttributeExpressions
    :var occurrenceNoteExpressions: A collection of Occurrence Note attribute search expressions
    :var returnScopedSubTreesHit: Specifies whether the search result should return only the sub-set of scopeBomLines
    given as input as part of the SearchScope
    :var formAttributeExpressions: A collection of Form attribute search expressions
    :var proximitySearchExpressions: A collection of spatial proximity search expressions
    :var boxZoneExpressions: A collection of spatial box zone expressions
    :var planeZoneExpressions: A collection of spatial plane zone search expressions
    :var savedQueryExpressions: A collection of saved query search expressions
    :var inClassQueryExpressions: inClassQueryExpressions
    :var sizeSearchExpression: sizeSearchExpression
    :var doTrushapeRefinement: Specifies whether to perform trueshape refinement on the spatial search or not
    """
    itemAndRevisionAttributeExpressions: List[AttributeExpression] = ()
    occurrenceNoteExpressions: List[OccurrenceNoteExpression] = ()
    returnScopedSubTreesHit: bool = False
    formAttributeExpressions: List[FormAttributeExpression] = ()
    proximitySearchExpressions: List[ProximityExpression] = ()
    boxZoneExpressions: List[BoxZoneExpression] = ()
    planeZoneExpressions: List[PlaneZoneExpression] = ()
    savedQueryExpressions: List[SavedQueryExpression] = ()
    inClassQueryExpressions: List[InClassExpression] = ()
    sizeSearchExpression: SearchBySizeExpression = None
    doTrushapeRefinement: bool = False


@dataclass
class BoxZoneExpression(TcBaseObj):
    """
    BoxZoneExpression specifies one set of Box zone criteria. The search
    results from each SearchBox are combined together using an
    'OR' operation. The spatial search returns a match with the
    search expression if a object either lies inside or intersects the
    search boxes
    
    :var searchBoxes: Boxes around which to search
    :var boxOperator: Operator to use for expression
    """
    searchBoxes: List[SearchBox] = ()
    boxOperator: BoxOperator = None


@dataclass
class StructureSearchResultResponse(TcBaseObj):
    """
    StructureSearchResultResponse is the result set received from a single step in a structure search.
    
    :var serviceData: serviceData
    :var objects: A batch of Objects that satisfy the search criteria for this search
    :var objectDone: The number of objects in the structure that have been processed so far
    :var estimatedObjectsLeft: An estimate of the number of lines yet to be processed
    :var percentComplete: percentComplete
    :var searchCursor: Search cursor object that holds the current state of the search in the BOM session
    :var finished: A boolean value which when 'true' specifies the search is finished
    """
    serviceData: ServiceData = None
    objects: List[BusinessObject] = ()
    objectDone: int = 0
    estimatedObjectsLeft: int = 0
    percentComplete: float = 0.0
    searchCursor: BusinessObject = None
    finished: bool = False


class MatchType(Enum):
    """
    Example: Find all found welds points connected to parts in a given scope with a full match between the weld point
    connected parts and the selected parts list, i.e. all the parts the weld is connected to were selected by the user .
    """
    NotApplicableMatch = 'NotApplicableMatch'
    FullMatch = 'FullMatch'
    PartialMatch = 'PartialMatch'
    NoMatch = 'NoMatch'


class AttributeType(Enum):
    """
    AttributeType enumerated type defines the type of data passed in an attribute search expression
    """
    BooleanType = 'BooleanType'
    IntegerType = 'IntegerType'
    DoubleType = 'DoubleType'
    StringType = 'StringType'
    DateType = 'DateType'
    TagType = 'TagType'


class PlaneZoneOperator(Enum):
    """
    PlaneZoneOperator enumerated type defines the operator to use as part of a plane-zone search expression
    """
    PlaneAbove = 'PlaneAbove'
    PlaneBelow = 'PlaneBelow'
    PlaneIntersects = 'PlaneIntersects'
    PlaneAboveOrIntersects = 'PlaneAboveOrIntersects'
    PlaneBelowOrIntersects = 'PlaneBelowOrIntersects'


class QueryOperator(Enum):
    """
    QueryOperator  enumerated type defines the operator to be used for comparison in a attribute search expression
    """
    Equal = 'Equal'
    GreaterThan = 'GreaterThan'
    GreaterThanOrEqual = 'GreaterThanOrEqual'
    LessThan = 'LessThan'
    LessThanOrEqual = 'LessThanOrEqual'
    NotEqual = 'NotEqual'
    IsNull = 'IsNull'
    IsNotNull = 'IsNotNull'
    Like = 'Like'
    NotLike = 'NotLike'


class BoxOperator(Enum):
    """
    BoxOperator defines the operator to apply as part of a box-zone search expression.
    """
    Inside = 'Inside'
    Outside = 'Outside'
    Intersects = 'Intersects'
    InsideOrIntersects = 'InsideOrIntersects'
    OutsideOrIntersects = 'OutsideOrIntersects'
