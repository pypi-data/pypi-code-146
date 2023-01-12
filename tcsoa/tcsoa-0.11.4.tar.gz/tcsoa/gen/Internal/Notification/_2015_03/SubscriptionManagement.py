from __future__ import annotations

from tcsoa.gen.Notification._2014_10.SubscriptionManagement import AttributeCriteria, NotificationDefinition, ActionHandler
from tcsoa.gen.BusinessObjects import BusinessObject, ImanSubscription, ImanEventType, ImanRelation, Condition, User, ImanActionHandler, TaskType
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExecutionPeriod(TcBaseObj):
    """
    Structure to hold the execution time, frequency and the execution day of the subscription.
    
    :var executionTime: The time of day when the Subscription should be processed. Setting NULL will cause the handlers
    to be run as soon as resources are available.
    :var executionDay: Execution day for the subscription to be created (Sunday, Monday, Tuesday, Wednesday, Thursday,
    Friday, Saturday). 
    :var frequency: Frequency of the subscription to be created (Immediately, Daily, Weekly).
    """
    executionTime: datetime = None
    executionDay: str = ''
    frequency: str = ''


@dataclass
class FindSubscriptionsInput2(TcBaseObj):
    """
    Contains all the input criteria required to search for Subscriptions.
    
    :var target: The object to monitor for the specified event type. This can also be Business Object type for class
    based ImanSubscription. If the value is NULL, search will not be performed on the basis of this field.
    :var subscriber: The User that is subscribing to the event. If the value is NULL, search will not be performed on
    the basis of this field.
    :var isActive: Status of the Subscription object. Valid values are 0, 1 and 2. Default value is 0 which indicates
    active as well as inactive subscription will be searched. 1 indicates active subscriptions and 2 indicates inactive
    subscriptions. Any value other than the valid values will be reinitialized to 0.
    :var frequency: Frequency of the subscription. Valid values are Immediately, Daily and Weekly.
    :var executionDay: Exedution Day of the subscription. Valid values are Sunday, Monday, Tuesday, Wednesday,
    Thursday, Friday or Saturday. If the frequency is Immediately or Daily, then this value may be NULL.
    :var notifier: The User to whom the subscription is transferred. If the value is NULL, search will not be performed
    on the basis of this field.
    :var temporaryNotifierDateRange: From and To date in case of temporary transfer of the subscription. If the value
    is NULLDATE, search will not be performed on the basis of this field.
    
    :var eventType: Type of event that will trigger the subscription. If the value is NULL, search will not be
    performed on the basis of this field.
    :var handlers: The handlers to execute when processing the Subscription. May be an empty list.
    :var condition: The Condition to evaluate when processing this Subscription. Only valid for class based
    Subscriptions. If the value is NULL, search will not be performed on the basis of this field.
    :var name: Name of the subscription object. If the value is NULL, search will not be performed on the basis of this
    field.
    :var executionTimeRange: Upper limit and the lower limit of the Subscription execution time.
    :var expirationDateRange: Upper limit and the lower limit of the Subscription expiration date.
    :var noExpDate: If true, do not search for Subscriptions with an expiration date.
    :var notificationPriority: Notification priority. Valid values are High, Low and Normal.
    """
    target: BusinessObject = None
    subscriber: User = None
    isActive: int = 0
    frequency: str = ''
    executionDay: str = ''
    notifier: User = None
    temporaryNotifierDateRange: DateRange = None
    eventType: ImanEventType = None
    handlers: List[ActionHandler] = ()
    condition: Condition = None
    name: str = ''
    executionTimeRange: DateRange = None
    expirationDateRange: DateRange = None
    noExpDate: bool = False
    notificationPriority: str = ''


@dataclass
class GetAssignEventDataResponse(TcBaseObj):
    """
    The GetAssignEventDataResponse structure represents the output response returning list of TaskType objects with
    partial errors wrapped in serviceData, if any.
    
    :var releaseStatus: A list of release status types.
    :var serviceData: Partial errors will be returned and wrapped in serviceData, if any are specified.
    """
    releaseStatus: List[TaskType] = ()
    serviceData: ServiceData = None


@dataclass
class GetAttachEventDataResponse(TcBaseObj):
    """
    The GetAttachEventDataResponse structure represents the output response returning lists of ImanRelation objects and
    attachment types.  Partial errors will be returned and wrapped in serviceData, if any are specified. 
    
    :var relations: A list of ImanRelation objects.
    :var attachmentTypes: A list of attachment type business objects.
    :var serviceData: Partial errors will be returned and wrapped in serviceData, if any are specified.
    """
    relations: List[ImanRelation] = ()
    attachmentTypes: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class GetEventTypesResponse(TcBaseObj):
    """
    The GetEventTypesResponse structure represents the output response returning a client ID string and lists of
    auditableEventTypes and subscribableEventTypes with partial errors wrapped in serviceData, if any.
    
    :var clientId: The unmodified value from the EventObject.clientId. This can be used by the caller to indentify this
    data structure with the source input data.
    :var auditableEventTypes: A list of auditable ImanEventType elements.
    :var subscribableEventTypes: A list of subscribable ImanEventType elements.
    :var serviceData: Error encountered while processing post event on element in the set is reported as partial errors
    and processing continues for the remaining elements in the input set. 
    """
    clientId: str = ''
    auditableEventTypes: List[ImanEventType] = ()
    subscribableEventTypes: List[ImanEventType] = ()
    serviceData: ServiceData = None


@dataclass
class GetSubscribableTypesResponse(TcBaseObj):
    """
    Contains type objects. Partial errors are returned via serviceData if there are any. 
    
    :var typeInfoList: Business object types.
    :var serviceData: Teamcenter service response data.
    """
    typeInfoList: List[SubscribableTypeInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetSubscriptionInputResponse(TcBaseObj):
    """
    A structure with lists of ImanEventType objects, ImanActionHandler objects and the attribute criteria specified in
    the configuration file for a business object type. Service data contains partial errors if any.
    
    :var eventTypes: A list of ImanEventType objects.
    :var handlers: A list of ImanActionHandler objects.
    :var attributeCriteria: A list of AttributeCriteria values corresponding to an object type.
    :var serviceData: Partial failures will be returned in the ServiceDate for each failed processing. Error
    encountered while processing post event on element in the set is reported as partial errors and processing
    continues for the remaining elements in the input set.
    """
    eventTypes: List[ImanEventType] = ()
    handlers: List[ImanActionHandler] = ()
    attributeCriteria: List[AttributeCriteria] = ()
    serviceData: ServiceData = None


@dataclass
class ModifySubscriptionsInput2(TcBaseObj):
    """
    Contains the Subscription object to modify and all of the input values to set on the Subscription. Supports both
    object and class based Subscriptions.
    
    :var subscriptionObject: ImanSubscription object to be modified.
    :var newSubscriptionValues: Contains all the input criteria required to create a single object or class based
    Subscription. The inputs include the target, subscriber, eventType, handlers, condition, criteria, revisionOption,
    executionPeriod, expirationDate, notification, notificationPriority, name, isActive.
    """
    subscriptionObject: ImanSubscription = None
    newSubscriptionValues: SubscriptionInput2 = None


@dataclass
class SubscribableTypeInfo(TcBaseObj):
    """
    The structure holds the information of subscribable types that need to be returned in the
    GetSubscribableTypesResponse structure.
    
    :var type: The subscribable business object type.
    :var typeName: The name of the subscribable business object type.
    :var parents: The names of all the parents in the heirarchy of the subscribable business object types.
    """
    type: BusinessObject = None
    typeName: str = ''
    parents: List[str] = ()


@dataclass
class SubscriptionInput2(TcBaseObj):
    """
    Contains all the input criteria required to create a single object or class based Subscription. The main inputs
    include the target object, subscriber, event type and action handler list.
    
    The notification should be included if the IMAN_Smtp_Mail_Notify handler is used.
    
    
    :var target: The object to monitor for the specified event type. This can also be Business Object type for class
    based ImanSubscription.
    :var subscriber: The User that is subscribing to the event.
    :var notification: Specifies the parameters to be used when sending the notification e-mail. Should be present for
    notification handlers. Can be NULL for all non-notification handlers.
    :var notificationPriority: Notification priority to be sent as part of the notification email.
    :var isActive: Status of the subscription to be created.
    Values can be true for ACTIVE and false for INACTIVE.
    
    Events are only generated and notified for the ACTIVE and not-expired subscriptions.
    :var name: Name for the subscription to be created.
    :var eventType: Type of event that will trigger the subscription.
    :var handlers: An ordered list of handlers to execute when processing the Subscription. Handlers will be executed
    in the order they appear in this list. Duplicates are not allowed. Each handler specified will also have its own
    set of handler parameters that will be passed to the handler during its execution.
    :var condition: The Condition to evaluate when processing this Subscription. Only valid for class based
    Subscriptions. Can be NULL.
    :var criteria: Attribute criteria to process when the Subscription is being executed. If these attribute values
    match those of the object, the Subscription will apply. Each entry in the list will be compared to the next using
    the logicOperator of the next value. The logicOperator of the first entry will not be used. Can be empty.
    :var revisionOption: Indicates the type of Item-Revision objects that will apply to the Subscription.
    :var executionPeriod: A Structure to hold executionTime, executionDay and frequency of the subscription.
    :var expirationDate: The date when the Subscription expires and will no longer be processed. Setting NULL will
    cause the Subscription to never expire.
    """
    target: BusinessObject = None
    subscriber: User = None
    notification: NotificationDefinition = None
    notificationPriority: str = ''
    isActive: bool = False
    name: str = ''
    eventType: ImanEventType = None
    handlers: List[ActionHandler] = ()
    condition: Condition = None
    criteria: List[AttributeCriteria] = ()
    revisionOption: RevisionOptions2 = None
    executionPeriod: ExecutionPeriod = None
    expirationDate: datetime = None


@dataclass
class TransferNotificationInput(TcBaseObj):
    """
    TransferNotificationInput holds the data needed to have subscriptions transferred to other users temporarily or
    permanently. In case of temporary transfer a range of dates is provided during which the transfer will be take
    place.
    
    :var subscriptions: List of ImanSubscription objects for bulk transfer.
    :var notifier: The User to be notified.
    :var notificationDateRange: The from and to dates in case of temporary transfer of the subscription.
    """
    subscriptions: List[ImanSubscription] = ()
    notifier: User = None
    notificationDateRange: DateRange = None


@dataclass
class DateRange(TcBaseObj):
    """
    Contains the from and to dates required to find a Subscription.
    
    :var fromDate: The date from which Subscriptions are to be found.
    :var toDate: The date till which Subscriptions are to be found.
    """
    fromDate: datetime = None
    toDate: datetime = None


@dataclass
class EventObject(TcBaseObj):
    """
    The EventObject structure represents required parameter to get event type names for the businessObject. 
    
    :var clientId: A unique identifier supplied by the caller. This ID is client's way of identifying event list. This
    is a required parameter. If nothing is to be passed to clientId; assign an empty String object. Assigning NULL to
    clientId is not allowed.
    :var businessObject: The Business Object  for which the valid Auditable and Subscribable event type list is to be
    retrieved. This is a required parameter.
    """
    clientId: str = ''
    businessObject: BusinessObject = None


class RevisionOptions2(Enum):
    """
    Specifies which level of Item Revisions should be considered for Item based Subscriptions. This only applies to
    Assign Status, Attach and New Item Rev events on target objects of type Item. For example, if a New Item Rev
    Subscription is defined with the BaselineRevisions2 option, only new Baseline Item Revisions will trigger the
    Subscription.
    
    NoRevisions is the default value for events other that those listed above.
    """
    NoRevisions2 = 'NoRevisions2'
    AllRevisions2 = 'AllRevisions2'
    ItemRevisions2 = 'ItemRevisions2'
    BaselineRevision2 = 'BaselineRevision2'
