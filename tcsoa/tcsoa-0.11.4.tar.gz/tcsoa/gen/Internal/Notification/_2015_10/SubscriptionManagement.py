from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Group, ClosureRule, ImanSubscription, Fnd0SubscriptionTemplate, Role
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAttachEventDataResponse2(TcBaseObj):
    """
    The GetAttachEventDataResponse2 structure represents the output response returning lists of relation objects and
    attachment types. Partial errors will be returned and wrapped in serviceData, if any are specified.
    
    :var relations: A list of relation objects.
    :var attachmentTypes: A list of attachment type business objects.
    :var serviceData: Partial errors will be returned and wrapped in serviceData, if any are specified.
    """
    relations: List[BusinessObject] = ()
    attachmentTypes: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class AttributeCriteria2(TcBaseObj):
    """
    The AttributeCriteria2 used in Fnd0IndirectSubscription object through  Fnd0SubscriptionTemplate object adds
    additional condition as to how a Subscription should be processed. It comprises of logical operators like "AND" or
    "OR" and math operators like "=, !=, <, >, <=, >=". The attribute name and attribute values are property names and
    their applicable values respectively.
    
    :var logicOperators: A list of logic operators
    :var attributeNames: A list of attribute names
    :var mathOperators: A list of math operators
    :var attributeValues: A list of attribute values
    """
    logicOperators: List[str] = ()
    attributeNames: List[str] = ()
    mathOperators: List[str] = ()
    attributeValues: List[str] = ()


@dataclass
class ModifySubscriptionTemplateInput(TcBaseObj):
    """
    The ModifySubscriptionTemplateInput structure holds the data required to modify a Fnd0SubscriptionTemplate object
    
    :var subscriptionTemplate: The Fnd0SubscriptionTemplate object to be modified
    :var templateData: The SubscriptionTemplate structure holds the data required to modify a Fnd0SubscriptionTemplate
    object
    """
    subscriptionTemplate: Fnd0SubscriptionTemplate = None
    templateData: SubscriptionTemplate = None


@dataclass
class SaveAsSubscriptionInputData(TcBaseObj):
    """
    A structure used by saveAsSubscription operation to hold the subscription to be copied and a new name to be given
    to the subscription to be created.
    
    :var subscription: The ImanSubscription to be copied.
    :var name: The name to be given to the new subscription.
    """
    subscription: ImanSubscription = None
    name: str = ''


@dataclass
class SubscriptionTemplate(TcBaseObj):
    """
    The SubscriptionTemplate structure holds the data required to create an Fnd0SubscriptionTemplate object
    
    :var name: Name of the template
    :var description: Description of the template
    :var subscribedObjectType: Subscribed object type which can be any object under WorkspaceObject
    :var subscribedObjectCriteria: A structure to hold the attribute criteria defined on the subscribed object
    :var targetObjectType: Target object type selected, must be a subscribable business object and can be any object
    under WorkspaceObject
    :var targetObjectCriteria: A structure to hold the attribute criteria defined on the target object
    :var closureRule: The closure rule to be used for traversal in the template
    :var validAccessors: The Group and Role objects with an access to the Fnd0SubscriptionTemplate object
    """
    name: str = ''
    description: str = ''
    subscribedObjectType: BusinessObject = None
    subscribedObjectCriteria: AttributeCriteria2 = None
    targetObjectType: BusinessObject = None
    targetObjectCriteria: AttributeCriteria2 = None
    closureRule: ClosureRule = None
    validAccessors: Accessors = None


@dataclass
class SubscriptionTemplateResponse(TcBaseObj):
    """
    A structure to hold the Fnd0SubscriptionTemplate object created or modified through an operation
    
    :var subscriptionTemplates: A list of Fnd0SubscriptionTemplate objects to be returned
    :var serviceData: Partial errors will be returned and wrapped in serviceData, if any are specified.
    """
    subscriptionTemplates: List[Fnd0SubscriptionTemplate] = ()
    serviceData: ServiceData = None


@dataclass
class Accessors(TcBaseObj):
    """
    A structure to hold the lists of Group and Role objects that have an access to the Fnd0SubscriptionTemplate object
    A user who belongs to the listed groups and roles will have an access to view or modify the subscription templates.
    
    :var groups: A list of Group objects with an access to the Fnd0SubscriptionTemplate object
    :var roles: A list of Role objects with an access to the Fnd0SubscriptionTemplate object
    """
    groups: List[Group] = ()
    roles: List[Role] = ()
