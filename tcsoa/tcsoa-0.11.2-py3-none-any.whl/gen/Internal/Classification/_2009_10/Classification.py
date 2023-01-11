from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GetClassificationHierarchiesResponse(TcBaseObj):
    """
    Holds the classification hierarchies returned by the  'getClassificationHierarchies()' method.
    
    :var hierarchies: References a map of class names associated with the given WorkspaceObject.
    :var ids: References a map of class IDs found associated with the given WorkspaceObject.
    :var data: Any failures with WorkspaceObject ID mapped to the error message are returned in the ServiceData list of
    partial errors.
    """
    hierarchies: ClassificationHierarchiesMap = None
    ids: ClassificationHierarchiesMap = None
    data: ServiceData = None


@dataclass
class GetClassificationPropertiesResponse(TcBaseObj):
    """
    Holds the classification properties returned by the  'getClassificationProperties()' method.
    
    :var propnames: References a map of classification property names for this WorkspaceObject object, if it is
    classified.
    :var propvalues: References a map of classification property values for this WorkspaceObject object, if it is
    classified.
    :var hierarchies: References a map of class IDs found for this WorkspaceObject object, if it is classified.
    :var propDeprecatedflags: References a map of of deprecated flags for the associated classification property. This
    flag will always be FALSE in case of non-key-LOV type of classification properties
    :var data: Any failures with the WorkspaceObject ID mapped to the error message are returned in the ServiceData
    list of partial errors.
    """
    propnames: ClassificationPropertiesMap = None
    propvalues: ClassificationPropertiesMap = None
    hierarchies: ClassificationPropertiesMap = None
    propDeprecatedflags: DeprecatedFlagsMap = None
    data: ServiceData = None


"""
Structure elements:

- primary key - Alphanumeric attribute ID of the classification property.
- values - Deprecated flags for this classification property.


"""
DeprecatedFlagsMap = Dict[str, List[bool]]


"""
Map that stores the classification hierarchy information.
"""
ClassificationHierarchiesMap = Dict[str, List[str]]


"""
Structure elements:

- primary key - Alphanumeric attribute ID of the classification property.
- values - Values for this classification property.


"""
ClassificationPropertiesMap = Dict[str, List[str]]
