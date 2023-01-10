from __future__ import annotations

from tcsoa.gen.StructureManagement._2008_05.StructureSearch import OccurrenceNoteExpression, SearchBySizeExpression, FormAttributeExpression, ProximityExpression, BoxZoneExpression, InClassExpression, SavedQueryExpression, AttributeExpression
from typing import Dict, List
from tcsoa.gen.StructureManagement._2010_04.StructureSearch import PlaneZoneExpression
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import Item


@dataclass
class SearchExpressionSet(TcBaseObj):
    """
    SearchExpression data structure specifies the full set of search expressions that are to be used to perform a
    single structure search. Each one of the expressions provided are combined together using a logical 'AND' between
    them.
    
    :var itemAndRevisionAttributeExpressions: A collection of Item and ItemRevision attribute search expressions
    :var occurrenceNoteExpressions: A collection of Occurrence Note attribute search expressions
    :var returnScopedSubTreesHit: Specifies whether the search result should return only the subset of 'scopeBomLines'
    given as input as part of the 'SearchScope'
    :var executeVOOFilter: If true, Valid Overlays Only (VOO) filter is applied prior to returning results from the
    server.
    :var executeRemoteSearch: Specifies whether the search should include results from the remote site in response.
    :var remoteSiteID: The remote site id to search from. By default, if the site id is not specified, the search will
    use the site id that is configured by the admin in Teamcenter.
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
class BoundingBoxInfo(TcBaseObj):
    """
    Contains the six Coordinates of the Bbox
    
    :var xmin: Minimum 'x' coordinate value for bounding box.
    :var ymin: Minimum 'y' coordinate value for bounding box.
    :var zmin: Minimum 'z' coordinate value for bounding box.
    :var xmax: Maximum 'x' coordinate value for bounding box.
    :var ymax: Maximum 'y' coordinate value for bounding box.
    :var zmax: Maximum 'z' coordinate value for bounding box.
    """
    xmin: float = 0.0
    ymin: float = 0.0
    zmin: float = 0.0
    xmax: float = 0.0
    ymax: float = 0.0
    zmax: float = 0.0


@dataclass
class BoundingBoxInfoResponse(TcBaseObj):
    """
    A map of Item passed in the input list to the 'BoundingBoxInfo' object, for the corresponding Item.
    
    :var boundingBoxes: Map of(Item/ 'BoundingBoxInfo') for each input Item and corresponding bounding box coordinates.
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during getting bounding box.
    """
    boundingBoxes: BoundingBoxs = None
    serviceData: ServiceData = None


"""
Item and corresponding bbox coordinates are mapped
"""
BoundingBoxs = Dict[Item, BoundingBoxInfo]
