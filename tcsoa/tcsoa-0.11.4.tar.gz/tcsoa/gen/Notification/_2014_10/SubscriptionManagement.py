from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanSubscription, ImanEventType, Condition, User, ImanActionHandler
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindSubscriptionsCriteriaInput(TcBaseObj):
    """
    Contains all the input criteria required to search for Subscriptions.
    
    :var target: The object to monitor for the specified event type.  This can also be Business Object type for class
    based Subscriptions.
    :var subscriber: The User that is subscribing to the event.
    :var eventType: Type of event that will trigger the subscription.
    :var handlers: An ordered list of handlers to execute when processing the Subscription.
    :var condition: The Condition to evaluate when processing this Subscription.  Only valid for class based
    Subscriptions.  Can be NULL.
    """
    target: BusinessObject = None
    subscriber: User = None
    eventType: ImanEventType = None
    handlers: List[ImanActionHandler] = ()
    condition: Condition = None


@dataclass
class GetSubscriptionsCriteriaInput(TcBaseObj):
    """
    Contains all the input criteria required to search for Subscriptions.
    
    :var target: The object to monitor for the specified event type.  This can also be Business Object type for class
    based ImanSubscription.  May be NULL.
    :var subscriber: The User that is subscribing to the event.  May be NULL.
    :var eventType: Type of event that will trigger the subscription.  May be NULL.
    :var handlers: The handlers to execute when processing the Subscription.  May be an empty list.
    :var execTimeBefore: Upper limit of the Subscription execution time.
    :var execTimeAfter: Lower limit of the Subscription execution time.
    :var execImmediately: If true, do not search for Subscriptions with an execution time.
    :var expDateBefore: Upper limit of the Subscription expiration date.
    :var expDateAfter: Lower limit of the Subscription expiration date.
    :var noExpDate: If true, do not search for Subscriptions with an expiration date.
    """
    target: BusinessObject = None
    subscriber: User = None
    eventType: ImanEventType = None
    handlers: List[ImanActionHandler] = ()
    execTimeBefore: datetime = None
    execTimeAfter: datetime = None
    execImmediately: bool = False
    expDateBefore: datetime = None
    expDateAfter: datetime = None
    noExpDate: bool = False


@dataclass
class AttributeComparison(TcBaseObj):
    """
    The overall attribute criteria for a Subscription can be made up of multiple individual attribute comparisons. 
    Each attribute comparison specifies the attribute on the target object to check, the value to compare it against
    and how to do the comparison.
    
    :var mathOperator: The math operator to use when comparing the attribute to the specified value. The MathOperators
    enum comprises of these values: EqualTo, NotEqualTo, GreaterThan, LessThan, GreaterThanEqualTo, LessThanEqualTo.
    :var attributeName: The name of the attribute on the target object to compare against.
    :var attributeValue: The string value to compare against.
    """
    mathOperator: MathOperators = None
    attributeName: str = ''
    attributeValue: str = ''


@dataclass
class AttributeCriteria(TcBaseObj):
    """
    If attribute criteria are specified on a Subscription, these criteria will be evaluated when the Subscription is
    being processed.  This processing involves comparing values in the criteria to the attribute values on the target
    object using a math operator, such as >, < or =.  Multiple attribute comparisons are then grouped using logic
    operators such as AND and OR.  Each AttributeCriteria represents a single attribute comparison and the logical
    operator to use when comparing it to the previous AttributeCriteria entry.
    
    :var logicOperator: The logic operator to use when comparing each AttributeCriteria to the next.  Processing will
    be done in order.  The first value in this list will be ignored.
    :var attributeComparison: A single attribute comparison.
    """
    logicOperator: LogicOperators = None
    attributeComparison: AttributeComparison = None


@dataclass
class ModifySubscriptionInput(TcBaseObj):
    """
    Contains the Subscription object to modify and all of the input values to set on the Subscription.  Supports both
    object and class based Subscriptions.
    
    :var subscription: The ImanSubscription object to modify.
    :var newSubscriptionValues: The new values to set on the Subscription.
    """
    subscription: ImanSubscription = None
    newSubscriptionValues: SubscriptionInput = None


@dataclass
class NotificationDefinition(TcBaseObj):
    """
    For e-mail notification handlers, a NotificationDefinition must be specified.  This structure describes the content
    of the e-mail to be sent as part of the notification Subscription.  This includes the subject, message and object
    properties to display in the message.  The recipients of the message are included in the HandlerParameters
    specified in the Subscription definition.
    
    :var subject: The subject of the notification e-mail.
    :var message: The message body of the notification e-mail.
    :var propertyNames: List of properties to include in the notification e-mail.  The values of these properties will
    be taken from the target object at the time the handler is executed.  These properties are not required.
    """
    subject: str = ''
    message: str = ''
    propertyNames: List[str] = ()


@dataclass
class SubscriptionInput(TcBaseObj):
    """
    Contains all the input criteria required to create a single object or class based Subscription.  The main inputs
    include the target object, subscriber, event type and action handler list.
    
    The notification should be included if the IMAN_Smtp_Mail_Notify handler is used.
    
    
    :var target: The object to monitor for the specified event type.  This can also be Business Object type for class
    based ImanSubscription.
    :var subscriber: The User that is subscribing to the event.
    :var eventType: Type of event that will trigger the subscription.
    :var handlers: An ordered list of handlers to execute when processing the Subscription.  Handlers will be executed
    in the order they appear in this list.  Duplicates are not allowed.  Each handler specified will also have its own
    set of handler parameters that will be passed to the handler during its execution.
    :var condition: The Condition to evaluate when processing this Subscription.  Only valid for class based
    Subscriptions.  Can be NULL.
    :var criteria: Attribute criteria to process when the Subscription is being executed.  If these attribute values
    match those of the object, the Subscription will apply.  Each entry in the list will be compared to the next using
    the logicOperator of the next value.  The logicOperator of the first entry will not be used.  Can be empty.
    :var revisionOption: Indicates the type of Item Revision objects that will apply to the Subscription.
    :var executionTime: The time of day when the Subscription should be processed.  Setting NULLDATE will cause the
    handlers to be run as soon as resources are available.
    :var expirationDate: The date when the Subscription expires and will no longer be processed.  Setting NULLDATE will
    cause the Subscription to never expire.
    :var notification: Specifies the parameters to be used when sending the notification e-mail.  Should be present for
    notification handlers.  Can be NULL for all non-notification handlers.
    """
    target: BusinessObject = None
    subscriber: User = None
    eventType: ImanEventType = None
    handlers: List[ActionHandler] = ()
    condition: Condition = None
    criteria: List[AttributeCriteria] = ()
    revisionOption: RevisionOptions = None
    executionTime: datetime = None
    expirationDate: datetime = None
    notification: NotificationDefinition = None


@dataclass
class SubscriptionsResponse(TcBaseObj):
    """
    List of the ImanSubscription objects from the operation.
    
    :var subscriptions: List of the Subscription objects from the operation.
    :var serviceData: Returned service data.
    """
    subscriptions: List[ImanSubscription] = ()
    serviceData: ServiceData = None


@dataclass
class ActionHandler(TcBaseObj):
    """
    Each handler will have an ImanActionHandler that describes the function to execute, and its own set of parameters. 
    These parameters are made up as a list of strings.  Not all handlers require parameters, but they should be present
    in the correct format if the handler expects them.  There will be no validation of the parameters when the
    Subscription is being created or modified.
    In the case of the default notification handler, the parameters should contain a list of the users to receive the
    e-mail.
    
    :var handler: The ImanActionHandler functionality to execute when the Subscription is processed.
    :var parameters: List of values to be passed to the handler during execution.
    """
    handler: ImanActionHandler = None
    parameters: List[str] = ()


class LogicOperators(Enum):
    """
    This enumeration lists the logic operators available when comparing multiple attribute comparisons as part of an
    attribute criteria on a Subscription.
    """
    LogicalAnd = 'LogicalAnd'
    LogicalOr = 'LogicalOr'


class MathOperators(Enum):
    """
    This enumeration lists the math operators available when comparing an attribute value to a specified string as part
    of an attribute criteria on a Subscription.
    """
    EqualTo = 'EqualTo'
    NotEqualTo = 'NotEqualTo'
    GreaterThan = 'GreaterThan'
    LessThan = 'LessThan'
    GreaterThanEqualTo = 'GreaterThanEqualTo'
    LessThanEqualTo = 'LessThanEqualTo'


class RevisionOptions(Enum):
    """
    Specifies which level of Item Revisions should be considered for Item  based Subscriptions.  This only applies to
    Assign Status, Attach and New Item Rev events on target objects of type Item.  For example, if a New Item Rev
    Subscription is defined with the BaselineRevisions option, only new Baseline Item Revisions will trigger the
    Subscription.
    
    NoRevisions is the default value for events other that those listed above.
    """
    NoRevisions = 'NoRevisions'
    AllRevisions = 'AllRevisions'
    ItemRevisions = 'ItemRevisions'
    BaselineRevisions = 'BaselineRevisions'
