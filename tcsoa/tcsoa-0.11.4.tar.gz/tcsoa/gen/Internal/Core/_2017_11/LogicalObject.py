from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LogicalObjectTypeInput(TcBaseObj):
    """
    Holds the logical object type definition data for the specified logical object type to be created.
    
    :var name: Name of the logical object type. (user supplied name)
    :var displayName: Display name of the logical object type.
    :var description: Description of the logical object type.
    :var rootTypeName: Name of the root business object, , All subtypes of POM_object are supported.
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
    memberPropertyDefinitions: List[MemberPropertyDefinition] = ()
    presentedPropertyDefinitions: List[PresentedPropertyDefinition] = ()


@dataclass
class LogicalObjectTypeResponse(TcBaseObj):
    """
    Holds the list of the created logical object types and partial errors.
    
    :var loTypes: A list of the created logical object types.
    :var serviceData: Returned service data.
    """
    loTypes: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class MemberPropertyDefinition(TcBaseObj):
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
    traversalPath: List[TraversalHop] = ()
    retrieveClassificationData: bool = False


@dataclass
class PresentedPropertyDefinition(TcBaseObj):
    """
    Presented properties represents the actual source properties of a root or member object on the logical object.
    
    :var presentedPropertyName: Name of the presented property.
    :var displayName: Display name of the presented property.
    :var description: Description of the presented property.
    :var rootOrMemberName: Root business object name or member property name.
    :var sourcePropertyName: Name of the source property of root or member business object.
    """
    presentedPropertyName: str = ''
    displayName: str = ''
    description: str = ''
    rootOrMemberName: str = ''
    sourcePropertyName: str = ''


@dataclass
class TraversalHop(TcBaseObj):
    """
    Holds traversal hop information which is represented either as a relation property (GRM, GRMS2P) or reference
    property (REF, REFBY).
    
    :var propertyName: Source object property name.
    :var propertyType: Type of property. Supported values are "relation" or "reference".
    :var destinationType: Type of destination object.
    :var direction: Direction of traversal. Supported values are "forward" or "reverse".
    """
    propertyName: str = ''
    propertyType: str = ''
    destinationType: str = ''
    direction: str = ''


@dataclass
class AddMemberAndPresentedPropsResponse(TcBaseObj):
    """
    Holds the output list of defined member and/or presented properties that were created on the specified logical
    object type and any partial errors, if thrown.
    
    :var memberOrPresentedProps: List of defined member and/or presented properties that were created on the specified
    input logical object type.
    :var serviceData: Returned service data.
    """
    memberOrPresentedProps: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class AddMembersPresentedPropsInput(TcBaseObj):
    """
    Holds the member and presented properties definition data on the specified logical object type.
    
    :var logicalObjectType: An object of logical object type ( subtype of "Fnd0LogicalObject" ) to which members and
    presented properties are to be added.
    :var memberDefinitions: A list of member defintions.
    :var presentedPropertiesDefinitions: A list of presented property defintions.
    """
    logicalObjectType: BusinessObject = None
    memberDefinitions: List[MemberPropertyDefinition] = ()
    presentedPropertiesDefinitions: List[PresentedPropertyDefinition] = ()


@dataclass
class DeleteMembersPresentedPropsInput(TcBaseObj):
    """
    Holds the logical object type and the member and presented properties on the specified logical object type.
    
    :var logicalObject: An object of type "Fnd0LogicalObject" for which members and presented properties are to be
    deleted.
    :var memberIdsOrPresentedProps: A list of member ids or presented property names.
    """
    logicalObject: BusinessObject = None
    memberIdsOrPresentedProps: List[str] = ()
