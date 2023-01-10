from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import Dict, List
from tcsoa.gen.Internal.IcsAw._2018_05.Classification import PropertyInfo, ClassDefinition, ClassParents, KeyLOVDef, ClassChildren
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.IcsAw._2018_12.Classification import BlockData


@dataclass
class ClassificationObjectInfo3(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObject: The found Classification Object
    :var workspaceObject: The WorkspaceObject that is associated by this Classification object. If this is NULLTAG, the
    the found "clsObject" is a standalone classification object.
    :var properties: List of properties containing, attribute ids and their values.
    :var blockDataMap: A map (string, blockData) of block IRDI to the list of block data. IRDI comprises of
    Registration Authority Identifier, Data Identifier, separator and version identifier. Example of an block IRDI is
    "SPLM-0#01-000806#001".
    """
    clsObject: BusinessObject = None
    workspaceObject: WorkspaceObject = None
    properties: List[PropertyInfo] = ()
    blockDataMap: BlockDataMap2 = None


@dataclass
class ClassificationObjects3(TcBaseObj):
    """
    Structure representing the Classification Objects of a WorkspaceObject.
    
    :var clsObjects: A list of Classification Objects' information.
    """
    clsObjects: List[ClassificationObjectInfo3] = ()


@dataclass
class FindClassificationInfo3Response(TcBaseObj):
    """
    Structure representing the classification information returned by FindClassificationInfo3 operation.
    
    :var clsObjectDefs: A map (WorkspaceObject, ClassificationObjects3) of workspace objects to a list of
    Classification objects.
    :var keyLOVDescriptors: A map (string, KeyLOVDef) of Classification KeyLOV IDs/IRDIs (International Registration
    Data Identifier) and its definitions pairs.
    :var clsClassDescriptors: A map (string, ClassDefinition) of Classification classes or view IDs/IRDIs and its
    corresponding definition pairs. This map also contains class attribute information.
    :var classParents: A map (string, ClassParents) of Classification classes or view IDs/IRDIs and its parents'
    definition pairs.
    :var classChildren: A map (string, ClassChildren) of Classification classes or view IDs/IRDIs and its children's
    definition pairs.
    :var clsBlockDescriptors: A map (String, ClassDefinition) of Classification classes IDDIs and its corresponding
    definition pairs. This map also contains class attribute information. This map is only used for Classification
    Standard Taxonomy (CST) property block information. This map differs from clsClassDescriptors as it contains the
    information for property clocks that belong to the returned classes.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    :var unitMap: A Map that contains all the units of a given measure, such as Length, Time, Power, etc.
    """
    clsObjectDefs: ClassificationObjectsDefMap3 = None
    keyLOVDescriptors: KeyLOVDefMap3 = None
    clsClassDescriptors: ClassDefinitionMap3 = None
    classParents: ClassParentsMap3 = None
    classChildren: ClassChildrenMap3 = None
    clsBlockDescriptors: BlockDefinitionMap3 = None
    serviceData: ServiceData = None
    unitMap: UnitMap = None


@dataclass
class Unit(TcBaseObj):
    """
    An individual unit (ex: Foot, Milimeter, or Watt).
    
    :var unitID: The unit ID.
    :var measure: The measure of the unit (ex: length).
    :var displayName: Unit Display name (Ex: ft /s^2).
    :var systemOfMeasurement: System of unit, (Ex: Metric).
    """
    unitID: str = ''
    measure: str = ''
    displayName: str = ''
    systemOfMeasurement: str = ''


"""
A map (string, blockData) of block IRDI to the list of block data.
"""
BlockDataMap2 = Dict[str, BlockData]


"""
The list of Classification Class or View ID / IRDIs and corresponding definition.
"""
ClassDefinitionMap3 = Dict[str, ClassDefinition]


"""
A map of classification class Id / Irdi to a list of its parents.
"""
ClassParentsMap3 = Dict[str, ClassParents]


"""
Map of workspace object to a list of its classification objects or standalone classification objects with a matching ID to that of the WorkspaceObject. If an object is classified then map value will have all its classification's information. If object is not classified, but system found standalone classification objects, then the map values will have standalone classification object's information. In the case of a standalone classification, the standalone classification&rsquo;s WorkspaceObject will be a NULLTAG.
"""
ClassificationObjectsDefMap3 = Dict[WorkspaceObject, ClassificationObjects3]


"""
The list of KeyLOV ids and corresponding KeyLOV definition. KeyLOV id and definition will be stxt business object if the class is a from traditional classification, or from Cst0KeyLOVDefinition business object if it is from Classification Standard Taxonomy (CST).
"""
KeyLOVDefMap3 = Dict[str, KeyLOVDef]


"""
A map of (String, Unit) describing all the units in a given measure (ex: Length, Power, Time, etc.)
"""
UnitMap = Dict[str, List[Unit]]


"""
A map of classification class Id / IRDI to a list of block property class definitions. Used by Classification Standard Taxonomy (CST) when a class has block properties.
"""
BlockDefinitionMap3 = Dict[str, ClassDefinition]


"""
A map of classification class Id / Irdi to a list of its children.
"""
ClassChildrenMap3 = Dict[str, ClassChildren]
