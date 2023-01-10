from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, BusinessObject
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
    
    :var isItemForm: If true, Form associted with Item is to be searched; otherwise, Form associted with ItemRevision
    is searched.
    :var relationType: Relation type object with which the Form is associated with the source Item or ItemRevision.
    :var formType: Form type object to be searched.
    :var attributeName: The attribute of the above Form type to be searched.
    :var attributeType: The type of the attribute to be searched on. The supported AttributeType are: BooleanType,
    IntegerType, DoubleType, StringType, DateType and TagType.
    :var queryOperator: Operator to use for search value comparison .  The supported QueryOperator are: Equal,
    GreaterThan, GreaterThanOrEqual, LessThan, LessThanOrEqual, NotEqual, IsNull, IsNotNull, Like and NotLike.
    :var values: The values of the attribute to be searched.
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
    
    :var inClassClassNames: A list of class names of the classification class used for search.
    :var inClassAttributeIDs: A list of attribute ID(s) of the class selected for classification search on which search
    needs to be performed.
    :var inClassAttributeValues: A list of values specified for search comparison.
    """
    inClassClassNames: List[str] = ()
    inClassAttributeIDs: List[int] = ()
    inClassAttributeValues: List[str] = ()


@dataclass
class AttributeExpression(TcBaseObj):
    """
    AttributeExpression encapsulates information to build a query on the attribute of an Item or ItemRevision or their
    sub-classes in the structure search scope. A set of these attribute expressions is contained inside a
    SearchExpressionInfo object. Search on multiple values specified within one AttributeExpression are combined with a
    logical 'OR' operation.
    
    :var className: Name of class, Item or ItemRevision or any of their sub-classes.
    :var attributeName: The attribute of the above 'className' to be searched on.
    :var attributeType: The type of the attribute to be searched on. The supported AttributeType are: BooleanType,
    IntegerType, DoubleType, StringType, DateType and TagType.
    :var queryOperator: Operator to use for search value comparison . The supported QueryOperator are: Equal,
    GreaterThan, GreaterThanOrEqual, LessThan, LessThanOrEqual, NotEqual, IsNull, IsNotNull, Like and NotLike.
    :var values: Values to be searched.
    """
    className: str = ''
    attributeName: str = ''
    attributeType: AttributeType = None
    queryOperator: QueryOperator = None
    values: AttributeValues = None


@dataclass
class OccurrenceNoteExpression(TcBaseObj):
    """
    OccurrenceNoteExpression contains information to search on a single occurrence note type within a containing
    SearchExpressionInfo object. The search on the multiple values specified within one OccurrenceNoteExpression are
    combined with a logical 'OR' operation.
    
    :var noteType: Occurrence note type to be search.
    :var queryOperator: Operator to use for search value comparison .  The supported QueryOperator are: Equal,
    GreaterThan, GreaterThanOrEqual, LessThan, LessThanOrEqual, NotEqual, IsNull, IsNotNull, Like and NotLike.
    :var values: A list of occurrance note values to be searched.
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
    
    :var boolValues: A list of boolean values that any of the accompanying set of search expressions may use.
    :var intValues: A list of integer values that any of the accompanying set of search expressions may use.
    :var doubleValues: A list of double values that any of the accompanying set of search expressions may use.
    :var stringValues: A list of string values that any of the accompanying set of search expressions may use.
    :var dateValues: Date values that any of the accompanying set of search expressions may use.
    :var tagValues: A list of objects that any of the accompanying set of search expressions may use.
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
    
    :var xValue: X value of the direction unit vector of the plane.
    :var yValue: Y value of the direction unit vector of the plane.
    :var zValue: Z value of the direction unit vector of the plane.
    :var displacement: Plane displacement in metres along the direction vector specified above.
    """
    xValue: float = 0.0
    yValue: float = 0.0
    zValue: float = 0.0
    displacement: float = 0.0


@dataclass
class PlaneZoneExpression(TcBaseObj):
    """
    PlaneZoneExpression represents a 3D plane to search against. It may define a search for all parts that intersect
    with the plane, or a search
    for all parts on one side of the plane.
    
    :var planzeZone: It defines a plane to search against.
    :var planeZoneOperator: Operator to use for expression. The supported PlaneZoneOperator are: PlaneZone_above,
    PlaneZone_below, PlaneZone_intersects, PlaneZone_aboveOrIntersects and PlaneZone_belowOrIntersects.
    """
    planzeZone: PlaneZone = None
    planeZoneOperator: PlaneZoneOperator = None


@dataclass
class ProximityExpression(TcBaseObj):
    """
    ProximityExpression specifies one set of proximity criteria. The search results from each bomLine are combined
    together using an 'OR' operation.
    
    :var bomLines: List of source BOMLine(s) for proximity search
    :var distance: Proximity distance in metres from the outer surface of the BOMLine geometry
    :var includeChildBomLines: If true, all child BOMLines of source bom lines are considered for proximity search
    """
    bomLines: List[BOMLine] = ()
    distance: float = 0.0
    includeChildBomLines: bool = False


@dataclass
class SavedQueryExpression(TcBaseObj):
    """
    SavedQueryExpression defines a search expression encapsulated as a Teamcenter saved-query that returns an Item,
    ItemRevision or any of their sub-types. The saved query may be a pre-defined out of the box saved query or one
    created using the Teamcenter QueryBuilder application.
    
    :var savedQuery: Object of an existing saved query.
    :var entries: A list of attribute entries that needs to be searched.
    :var values: A list of values of the above entries to be searched.
    """
    savedQuery: BusinessObject = None
    entries: List[str] = ()
    values: List[str] = ()


@dataclass
class SearchBox(TcBaseObj):
    """
    SearchBox defines a single box zone to search in. It contains the definition of an axis-aligned box and an
    accompanying transform to describe it orientation.
    
    :var xmin: Point defining the minimum extent along the x-axis.
    :var ymin: Point defining the minimum extent along the y-axis.
    :var zmin: Point defining the minimum extent along the z-axis.
    :var xmax: Point defining the maximum extent along the x-axis.
    :var ymax: Point defining the maximum extent along the y-axis.
    :var zmax: Point defining the maximum extent along the z-axis.
    :var transform: Transform defining the orientation of the box ( empty vector denotes identity transform ).
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
    a specified size.
    
    :var largerThan: If true, it searches for larger than the length specified; otherwise, searches for smaller.
    :var diagonalLength: The length of the largest bounding box diagonal, in metres.
    """
    largerThan: bool = False
    diagonalLength: float = 0.0


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
class SearchScope(TcBaseObj):
    """
    The SearchScope specifies the scope of a search
    
    :var window: BOM window object specifying a structure context within which to perform search
    :var scopeBomLines: List of BOMLine objects, specifying scope of the search
    :var ignoreOccurrenceTypes: List of strings, specifying occurrence types to be ignored from search results
    """
    window: BOMWindow = None
    scopeBomLines: List[BOMLine] = ()
    ignoreOccurrenceTypes: List[str] = ()


@dataclass
class BoxZoneExpression(TcBaseObj):
    """
    BoxZoneExpression specifies one set of Box zone criteria. The search results from each SearchBox are combined
    together using an 'OR' operation.
    
    :var searchBoxes: List of 'SearchBox', specifying box(s) around which to search.
    :var boxOperator: Operator to use for expression. The supported BoxOperator are: Inside, Outside, Intersects,
    InsideOrIntersects and OutsideOrIntersects.
    """
    searchBoxes: List[SearchBox] = ()
    boxOperator: BoxOperator = None


@dataclass
class StructureSearchResultResponse(TcBaseObj):
    """
    StructureSearchResultResponse is the result set received from a single step in a structure search.
    
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during search.
    :var bomLines: A batch of BOMLine(s) that satisfy the search criteria for this search. Not used for 'stopSearch'.
    :var linesDone: The number of lines returned in the response. Not used for 'stopSearch'.
    :var estimatedLinesLeft: An estimate of the number of lines yet to be processed. Not used for 'startSearch',
    'nextSearch 'and' stopSearch'.
    :var percentComplete: Not used for 'startSearch', 'nextSearch' and 'stopSearch'.
    :var searchCursor: Search cursor object that holds the current state of the search in the BOM session. Not used for
    'stopSearch'.
    :var finished: A boolean value 'true' specifies that the search has stopped.
    """
    serviceData: ServiceData = None
    bomLines: List[BOMLine] = ()
    linesDone: int = 0
    estimatedLinesLeft: int = 0
    percentComplete: float = 0.0
    searchCursor: BusinessObject = None
    finished: bool = False


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
    Plane_above = 'Plane_above'
    Plane_below = 'Plane_below'
    Plane_intersects = 'Plane_intersects'
    Plane_aboveOrIntersects = 'Plane_aboveOrIntersects'
    Plane_belowOrIntersects = 'Plane_belowOrIntersects'


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
