from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import Dict, List
from tcsoa.gen.Internal.IcsAw._2018_05.Classification import PropertyInfo, ClassDefinition, ClassParents, KeyLOVDef, ClassChildren
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BlockData(TcBaseObj):
    """
    Structure representing the list of blocks&rsquo; information of a Classification Object.
    
    :var blocks: A list of block information.
    """
    blocks: List[BlockInfo] = ()


@dataclass
class ClassificationObjectInfo2(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObject: The found Classification object.
    :var workspaceObject: The WorkspaceObject that is associated by this Classification object. If this is NULLTAG,
    then the found "clsObject" is a standalone classification object.
    :var properties: List of properties containing, attributes ids and their values.
    :var blockDataMap: A map (string, blockData) of block IRDI to the list of block data. IRDI comprises of
    Registration Authority Identifier, Data Identifier, separator and version identifier. Example of an block IRDI is
    "SPLM-0#01-000806#001".
    """
    clsObject: BusinessObject = None
    workspaceObject: WorkspaceObject = None
    properties: List[PropertyInfo] = ()
    blockDataMap: BlockDataMap = None


@dataclass
class ClassificationObjects2(TcBaseObj):
    """
    Structure representing the Classification Objects of a WorkspaceObject.
    
    :var clsObjects: A list of Classification Objects' information.
    """
    clsObjects: List[ClassificationObjectInfo2] = ()


@dataclass
class BlockInfo(TcBaseObj):
    """
    Structure containing classification block details. Classification block is a class attribute (Cst0ClassAttrute)
    pointing to property definition (Cst0PropertyDefinition) instance which references another classification class
    (Cst0ClassDefinition).
    
    :var classId: The classification class IRDI to which current block ID references. This is used in polymorphic
    blocks.
    :var owningBlocks: List of classification block IRDI to which given block belongs.
    :var cardinalityIndex: The index of a block in a given cardinal structure. Classification blocks can be configured
    as cardinal block in a class; this index is used to identify the location of the block in a given cardinal
    structure.
    :var properties: List of properties containing, attributes ids and their values.
    :var blockDataMap: A map (string, blockData) of block IRDI to the list of block data.
    """
    classId: str = ''
    owningBlocks: List[str] = ()
    cardinalityIndex: int = 0
    properties: List[PropertyInfo] = ()
    blockDataMap: BlockDataMap = None


@dataclass
class FindClassificationInfo2Response(TcBaseObj):
    """
    Structure representing the classification information returned by FindClassificationInfo2 operation.
    
    :var clsObjectDefs: A map (WorkspaceObject, ClassificationObjects2) of workspace objects to a list of
    Classification objects.
    :var keyLOVDescriptors: A map (string, KeyLOVDef) of Classification KeyLOV IDs/IRDIs (International Registration
    Data Identifier) and its definitions pairs.
    :var clsClassDescriptors: A map (string, ClassDefinition) of Classification classes or view IDs/IRDIs and its
    corresponding definition pairs. This map also contains class attribute information.
    :var classParents: A map (string, ClassParents) of Classification classes or view IDs/IRDIs and its parents'
    definition pairs.
    :var classChildren: A map (string, ClassChildren) of Classification classes or view IDs/IRDIs and its children's
    definition pairs.
    :var clsBlockDescriptors: A map (string, ClassDefinition) of Classification classes IRDIs and its corresponding
    definition pairs. This map also contains class attribute information. This map is only used for Classification
    Standard Taxonomy (CST) property block information. This map differs from clsClassDescriptors as it contains the
    information for property blocks that belong to the returned classes.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    clsObjectDefs: ClassificationObjectsDefMap2 = None
    keyLOVDescriptors: KeyLOVDefMap2 = None
    clsClassDescriptors: ClassDefinitionMap2 = None
    classParents: ClassParentsMap2 = None
    classChildren: ClassChildrenMap2 = None
    clsBlockDescriptors: BlockDefinitionMap2 = None
    serviceData: ServiceData = None


@dataclass
class SaveClassificationObjects2Response(TcBaseObj):
    """
    Holds the classification objects returned by the saveClassificationObjects2 operation.
    
    :var classificationObjects: A list of created or updated Classification objects.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    classificationObjects: List[ClassificationObjectInfo2] = ()
    serviceData: ServiceData = None


"""
A map (string, blockData) of block IRDI to the list of block data.
"""
BlockDataMap = Dict[str, BlockData]


"""
The list of Classification Class or View ID / IRDIs and corresponding definition.
"""
ClassDefinitionMap2 = Dict[str, ClassDefinition]


"""
A map of classification class Id / Irdi to a list of its parents.
"""
ClassParentsMap2 = Dict[str, ClassParents]


"""
Map of workspace object to a list of its classification objects or standalone classification objects with a matching ID to that of the WorkspaceObject. If an object is classified then map value will have all its classification's information. If object is not classified, but system found standalone classification objects, then the map values will have standalone classification object's information. In the case of a standalone classification, the standalone classification&rsquo;s WorkspaceObject will be a NULLTAG.
"""
ClassificationObjectsDefMap2 = Dict[WorkspaceObject, ClassificationObjects2]


"""
The list of KeyLOV ids and corresponding KeyLOV definition. KeyLOV id and definition will be stxt business object if the class is a from traditional classification, or from Cst0KeyLOVDefinition business object if it is from Classification Standard Taxonomy (CST).
"""
KeyLOVDefMap2 = Dict[str, KeyLOVDef]


"""
A map of classification class Id / IRDI to a list of block property class definitions. Used by Classification Standard Taxonomy (CST) when a class has block properties.
"""
BlockDefinitionMap2 = Dict[str, ClassDefinition]


"""
A map of classification class Id / Irdi to a list of its children.
"""
ClassChildrenMap2 = Dict[str, ClassChildren]
