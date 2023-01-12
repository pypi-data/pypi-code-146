from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Internal.Core._2018_06.LogicalObject import TraversalHop2
from dataclasses import dataclass


@dataclass
class IncludedLogicalObjectDefinition(TcBaseObj):
    """
    An included logical object definition consists of included logical object ID, display name, description and the
    navigation path, which specifies the path to reach the destination logical object.
    
    :var includedLogicalObjectID: ID of the included logical object property
    :var displayName: Display name of the included logical object property.
    :var description: Description of the included logical object property.
    :var traversalPath: A list of traversal hops.
    :var applyConfigurationContext: If TRUE , The destination objects that satisfy the configuration context criteria
    expression will be returned.
    """
    includedLogicalObjectID: str = ''
    displayName: str = ''
    description: str = ''
    traversalPath: List[TraversalHop2] = ()
    applyConfigurationContext: bool = False


@dataclass
class AddIncludedLOInput(TcBaseObj):
    """
    Represents the definition data for included logical objects to be added to a Logical Object Type.
    
    :var logicalObjectType: An object of logical object type ( subtype of "Fnd0LogicalObject" ) to which included
    logical objects are to be added.
    :var includedLODefinitions: A list of included logical object defintions.
    """
    logicalObjectType: BusinessObject = None
    includedLODefinitions: List[IncludedLogicalObjectDefinition] = ()


@dataclass
class AddIncludedLogicalObjectsResponse(TcBaseObj):
    """
    Holds the output list of included logical objects that were created on the specified logical object type and any
    partial errors, if thrown.
    
    :var includedLogicalObjects: List of included logical objects that were created on the specified input logical
    object type.
    :var serviceData: Returned service data.
    """
    includedLogicalObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None
