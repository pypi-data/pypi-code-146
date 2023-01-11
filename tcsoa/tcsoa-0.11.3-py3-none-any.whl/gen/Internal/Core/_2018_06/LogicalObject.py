from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Internal.Core._2017_11.LogicalObject import PresentedPropertyDefinition
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LogicalObjectTypeInput2(TcBaseObj):
    """
    Holds the logical object type definition data for the specified logical object type to be created.
    
    :var name: Name of the logical object type. (user supplied name)
    :var displayName: Display name of the logical object type.
    :var description: Description of the logical object type.
    :var rootTypeName: Name of the root business object, All subtypes of POM_object are supported.
    :var parentTypeName: Name of the parent logical object type, It should be a type or subtype of Fnd0LogicalObject.
    (optional)
    :var retrieveClassificationData: If TRUE , classification data will be retrieved for the root business object.
    If FALSE , classification data will not be retrieved for the root business object.
    :var memberPropertyDefinitions: A list of member property defintions. (optional)
    :var presentedPropertyDefinitions: A list of presented property defintions. (optional)
    """
    name: str = ''
    displayName: str = ''
    description: str = ''
    rootTypeName: str = ''
    parentTypeName: str = ''
    retrieveClassificationData: bool = False
    memberPropertyDefinitions: List[MemberPropertyDefinition2] = ()
    presentedPropertyDefinitions: List[PresentedPropertyDefinition] = ()


@dataclass
class MemberPropertyDefinition2(TcBaseObj):
    """
    Member properties represents the objects, which is reached from the root business object via the specified
    traversal paths, in order to present their properties onto the logical object.
    
    :var memberPropertyName: Name of the member property.
    :var displayName: Display name of the member property.
    :var description: Description of the member property.
    :var traversalPath: A list of traversal hops.
    :var retrieveClassificationData: If TRUE , classification data will be retrieved for this member property.
    If FALSE , classification data will not be retrieved for this member property.
    """
    memberPropertyName: str = ''
    displayName: str = ''
    description: str = ''
    traversalPath: List[TraversalHop2] = ()
    retrieveClassificationData: bool = False


@dataclass
class TraversalHop2(TcBaseObj):
    """
    Represents traversal hop definition for "forward" or "reverse" traversal on either a relation property or a
    reference property.
    
    :var propertyName: Source object property name.
    :var propertyType: Type of property. Supported values are "relation" or "reference".
    :var destinationType: Type of destination object. All subtypes of POM_object are supported.
    :var direction: Direction of traversal. Supported values are "forward" or "reverse".
    :var destinationObjectCriteria: It represents the criteria expression. The destination objects that satisfy the
    criteria expression will be returned. By default, destination object criteria expression is empty. Supported values
    are
    1.    $CurrentUserSessionProject, which is a system-defined criteria expression for traversal to the  destination
    objects which are assigned to the current user session project. (optional)
    """
    propertyName: str = ''
    propertyType: str = ''
    destinationType: str = ''
    direction: str = ''
    destinationObjectCriteria: str = ''


@dataclass
class UpdateMemberInput(TcBaseObj):
    """
    Represents the definition data for members that is to be updated on an existing Logical Object Type.
    
    :var logicalObjectType: An object of logical object type ( subtype of "Fnd0LogicalObject" ) to which member
    definitions are being updated.
    :var membersToBeUpdated: A map (string, MemberPropertyDefinition2) of name of member and it's definition which is
    to be updated.
    Key for this map would be a existing "member name" and value a structure which contains the new definition for this
    member.
    """
    logicalObjectType: BusinessObject = None
    membersToBeUpdated: MemberDefinitionMap = None


@dataclass
class AddMembersPresentedPropsInput2(TcBaseObj):
    """
    Represents the definition data for member and presented properties to be added to an existing Logical Object Type.
    
    :var logicalObjectType: An object of logical object type ( subtype of "Fnd0LogicalObject" ) to which members and
    presented properties are to be added.
    :var memberPropertiesDefinitions: A list of member defintions.
    :var presentedPropertiesDefinitions: A list of presented property defintions.
    """
    logicalObjectType: BusinessObject = None
    memberPropertiesDefinitions: List[MemberPropertyDefinition2] = ()
    presentedPropertiesDefinitions: List[PresentedPropertyDefinition] = ()


"""
A map of member and it's member definition information.
"""
MemberDefinitionMap = Dict[str, MemberPropertyDefinition2]
