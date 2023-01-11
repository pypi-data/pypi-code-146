from __future__ import annotations

from tcsoa.gen.StructureManagement._2008_05.StructureSearch import OccurrenceNoteExpression, SearchBySizeExpression, FormAttributeExpression, BoxZoneExpression, InClassExpression, SavedQueryExpression, AttributeExpression
from tcsoa.gen.BusinessObjects import BOMWindow, BusinessObject, RuntimeBusinessObject
from typing import List
from tcsoa.gen.StructureManagement._2010_04.StructureSearch import PlaneZoneExpression
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProximityExpression(TcBaseObj):
    """
    ProximityExpression specifies one set of proximity criteria. The search results for each lines are combined
    together using an 'OR' operation.
    
    :var srcLines: A list of source Fnd0BOMLineLite or BOMLine objects to be used in the proximity search.
    :var distance: Proximity distance in metres from the outer surface of the Fnd0BOMLineLite or BOMLine geometry.
    :var includeChildLines: If true, all child Fnd0BOMLineLite objects or BOMLine of source srcLines are considered in
    the proximity search.
    """
    srcLines: List[RuntimeBusinessObject] = ()
    distance: float = 0.0
    includeChildLines: bool = False


@dataclass
class SearchExpressionSet(TcBaseObj):
    """
    The full set of search expressions that are to be used to perform a single structure search. Each of the
    expressions provided are combined using a logical 'AND' operator.
    
    :var itemAndRevisionAttributeExpressions: A list of Item and ItemRevision attribute search expressions.
    :var occurrenceNoteExpressions: A list of Occurrence Note attribute search expressions.
    :var returnScopedSubTreesHit: If true, return only the subset of 'scopeBomLines' provided in input as part of
    'SearchScope'.
    :var executeVOOFilter: If true, Valid Overlays Only (VOO) filter is applied prior to returning the results from the
    server.
    :var executeRemoteSearch: If true, the search includes results from local and remote site(s) in response otherwise
    search results from local site are returned.
    :var remoteSiteID: The remote site ID to search from. By default, if the site ID is not specified, the search will
    use the site id that is configured by the admin in Teamcenter.
    :var formAttributeExpressions: A list of Form attribute search expressions.
    :var proximitySearchExpressions: A list of spatial proximity search expressions.
    :var boxZoneExpressions: A list of spatial box zone expressions.
    :var planeZoneExpressions: A list of spatial plane zone search expressions.
    :var savedQueryExpressions: A list of saved query search expressions.
    :var inClassQueryExpressions: A list of class attribute search expressions.
    :var sizeSearchExpression: A list of spatial size search expressions.
    :var doTrushapeRefinement: If true, Trueshape is perform. (use actual geometry rather using bounding box covering
    min and max points) refinement on the spatial search.
    """
    itemAndRevisionAttributeExpressions: List[AttributeExpression] = ()
    occurrenceNoteExpressions: List[OccurrenceNoteExpression] = ()
    returnScopedSubTreesHit: bool = False
    executeVOOFilter: bool = False
    executeRemoteSearch: bool = False
    remoteSiteID: str = ''
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
    SearchScope specifies the scope of a search.
    
    :var window: The BOMWindow object specifying a structure context within which to perform search.
    :var scopeLines: A list of Fnd0BOMLineLite or BOMLine objects, specifying scope of the search.
    :var ignoreOccurrenceTypes: A list of occurrence types that are to be ignored from search results.
    """
    window: BOMWindow = None
    scopeLines: List[RuntimeBusinessObject] = ()
    ignoreOccurrenceTypes: List[str] = ()


@dataclass
class StructureSearchResultResponse(TcBaseObj):
    """
    The result set received from a single step in a structure search.
    
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during performing search.
    :var outLines: A batch of Fnd0BOMLineLite or BOMLine objects that satisfy the search criteria for this search.
    :var linesDone: The number of lines returned in the response.
    :var searchCursor: Search cursor object that holds the current state of the search in the BOM session.
    :var finished: If true, the search is complete; otherwise, call 'nextSearch2' to get next set of results.
    """
    serviceData: ServiceData = None
    outLines: List[RuntimeBusinessObject] = ()
    linesDone: int = 0
    searchCursor: BusinessObject = None
    finished: bool = False
