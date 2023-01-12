from __future__ import annotations

from tcsoa.gen.StructureManagement._2008_05.StructureSearch import OccurrenceNoteExpression, SearchBySizeExpression, FormAttributeExpression, ProximityExpression, BoxZoneExpression, PlaneZone, InClassExpression, SavedQueryExpression, AttributeExpression
from enum import Enum
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PlaneZoneExpression(TcBaseObj):
    """
    PlaneZoneExpression represents a 3D plane to search against. It may define a search for all parts that intersect
    with the plane, or a search for all parts on one side of the plane.
    
    :var planeZone: It defines a plane to search against
    :var planeZoneOperator: Operator to use for expression
    """
    planeZone: PlaneZone = None
    planeZoneOperator: PlaneZoneOperator = None


@dataclass
class SearchExpressionSet(TcBaseObj):
    """
    SearchExpression data structure specifies the full set of search expressions that are to be used to perform a
    single structure search. Each one of the expressions provided are combined together using a logical 'AND' between
    them.
    
    :var itemAndRevisionAttributeExpressions: A collection of Item and ItemRevision attribute search expressions
    :var occurrenceNoteExpressions: A collection of Occurrence Note attribute search expressions
    :var returnScopedSubTreesHit: Specifies whether the search result should return only the sub-set of
    scopeBomLines&#x0A;given as input as part of the SearchScope
    :var formAttributeExpressions: A collection of Form attribute search expressions
    :var proximitySearchExpressions: A collection of spatial proximity search expressions
    :var boxZoneExpressions: A collection of spatial box zone expressions
    :var planeZoneExpressions: A collection of spatial plane zone search expressions
    :var savedQueryExpressions: A collection of saved query search expressions
    :var inClassQueryExpressions: A collection of inclass attribute search expressions
    :var sizeSearchExpression: A collection of spatial size search expressions
    :var doTrushapeRefinement: Specifies whether to perform trushape (use actual geometry rather using bounding box
    covering min and max points) refinement on the spatial search
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


class PlaneZoneOperator(Enum):
    """
    PlaneZoneOperator enumerated type defines the operator to use as part of a plane-zone search expression
    """
    PlaneZone_above = 'PlaneZone_above'
    PlaneZone_below = 'PlaneZone_below'
    PlaneZone_intersects = 'PlaneZone_intersects'
    PlaneZone_aboveOrIntersects = 'PlaneZone_aboveOrIntersects'
    PlaneZone_belowOrIntersects = 'PlaneZone_belowOrIntersects'
