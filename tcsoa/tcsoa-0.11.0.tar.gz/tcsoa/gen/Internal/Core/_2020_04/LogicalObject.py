from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Internal.Core._2018_06.LogicalObject import MemberPropertyDefinition2
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PresentedPropertyDefinition2(TcBaseObj):
    """
    The presented property definitions which contains the root or member object name, source property name and an
    indicator to identify if the presented property is writable.
    
    :var presentedPropertyName: Name of the presented property.
    :var displayName: Display name of the presented property.
    :var description: Description of the presented property.
    :var rootOrMemberName: Root business object name if the presented property is from the root on the Logical Object
    type.  Member property name if the presented property is from the member on the Logical Object type.
    :var sourcePropertyName: Source property name.
    :var isWritable: If true, the presented property is writable
    """
    presentedPropertyName: str = ''
    displayName: str = ''
    description: str = ''
    rootOrMemberName: str = ''
    sourcePropertyName: str = ''
    isWritable: bool = False


@dataclass
class AddMemAndPresentedPropsWriteInput(TcBaseObj):
    """
    Represents the definition data for member and presented properties to be added to an existing logical object type.
    
    :var logicalObjectType: An object of logical object type (Fnd0LogicalObject) to which members and presented
    properties are to be added.
    :var memberPropertiesDefinitions: A list of member defintions.
    :var presentedPropertiesDefinitions: A list of presented property defintions.
    """
    logicalObjectType: BusinessObject = None
    memberPropertiesDefinitions: List[MemberPropertyDefinition2] = ()
    presentedPropertiesDefinitions: List[PresentedPropertyDefinition2] = ()
