from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanRelation
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MultiRelMultiLevelExpandInput(TcBaseObj):
    """
    Input structure for createRelations operation.
    
    :var object: This is the starting object.
    :var relationships: Relationships used in search.
    """
    object: BusinessObject = None
    relationships: List[MultiRelationMultiLevelExpandRelationship] = ()


@dataclass
class MultiRelationMultiLevelExpandChildNodes(TcBaseObj):
    """
    This structure contains information for the child nodes in the tree structure returned by the multi-level expand.
    
    :var relationship: The relationship.
    :var children: The children found.
    """
    relationship: MultiRelationMultiLevelExpandRelationship = None
    children: List[MultiRelationMultiLevelExpandOutputNode] = ()


@dataclass
class MultiRelationMultiLevelExpandOutputNode(TcBaseObj):
    """
    This contains the tree structure returned by the multi level expand. This starts with the root node. And contains
    all its children based on the input relationships.
    
    :var currentObject: Current object represented by this node.
    :var relation: Relation of current object and children.
    :var relAndChildNodes: A list of the expansion nodes beneath the object
    """
    currentObject: BusinessObject = None
    relation: ImanRelation = None
    relAndChildNodes: List[MultiRelationMultiLevelExpandChildNodes] = ()


@dataclass
class MultiRelationMultiLevelExpandRelationship(TcBaseObj):
    """
    This structure represents the relationship being used and if the input object is the primary or secondary object.
    
    :var relationName: Name of the relationship.
    :var isPrimaryObject: If the object in 'MultiRelMultiLevelExpandInput' is on the primary object in the relationship
    """
    relationName: str = ''
    isPrimaryObject: bool = False


@dataclass
class MultiRelationMultiLevelExpandResponse(TcBaseObj):
    """
    This contains the tree structure returned by the multi-level expand. The node, foundObjects, starts with the input
    node.  It contains all it's children based on the input relationships.
    
    :var serviceData: Service data
    :var foundObjects: Objects found
    """
    serviceData: ServiceData = None
    foundObjects: MultiRelationMultiLevelExpandOutputNode = None


@dataclass
class Relationship(TcBaseObj):
    """
    'Relationship' structure represents all required parameters to create the relation between the primary and
    secondary object.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this 'Relationship' structure.
    :var relationType: Name of the relation type to create, required. This could be an empty string, in which case the
    relation name will be searched in the preference, ParentTypeName_ChildTypeName_default_relation or
    ParentTypeName_default_relation.
    :var primaryObject: The primary object to create the relation from.
    :var secondaryObject: The secondary object to create the relation to.
    :var userData: The user data object used to create the relation. This parameter is optional.
    """
    clientId: str = ''
    relationType: str = ''
    primaryObject: BusinessObject = None
    secondaryObject: BusinessObject = None
    userData: BusinessObject = None


@dataclass
class CreateRelationsOutput(TcBaseObj):
    """
    This structure contains information for 'createRelations' operation.
    
    :var clientId: The unmodified value from the 'Relationship.clientId'. This can be used by the caller to indentify
    this data structure with the source input data.
    :var relation: The newly created relation.
    """
    clientId: str = ''
    relation: ImanRelation = None


@dataclass
class CreateRelationsResponse(TcBaseObj):
    """
    'CreateRelationsResponse' structure represents the relations created between the primary and secondary object and
    errors occurred.
    
    :var output: A list of created relations.
    :var serviceData: Standard 'ServiceData' object to hold the partial errors that the operation encounters.
    """
    output: List[CreateRelationsOutput] = ()
    serviceData: ServiceData = None
