from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Notification._2015_03.SubscriptionManagement import GetSubscribableTypesResponse, TransferNotificationInput, GetAssignEventDataResponse, GetEventTypesResponse, FindSubscriptionsInput2, GetAttachEventDataResponse, ModifySubscriptionsInput2, SubscriptionInput2, GetSubscriptionInputResponse, EventObject
from typing import List
from tcsoa.gen.Notification._2014_10.SubscriptionManagement import SubscriptionsResponse
from tcsoa.base import TcService
from tcsoa.gen.Internal.Notification._2015_03.MessageManagement import UserGroupAliasResponse


class SubscriptionManagementService(TcService):

    @classmethod
    def getSubscribableTypes(cls, childTypeOption: str) -> GetSubscribableTypesResponse:
        """
        This operation retrieves types and subtypes of business objects for which notification subscriptions can be
        created. The  types and subtype objects are based on the childTypeOption.
        
        Use cases:
        The client creates a Subscription in order to trigger functionality when a specific event occurs against the
        object. Subscriptions cannot be created for all types of objects. There are only a certain types of objects
        that are subscribable. These subscribable object types are returned.
        """
        return cls.execute_soa_method(
            method_name='getSubscribableTypes',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'childTypeOption': childTypeOption},
            response_cls=GetSubscribableTypesResponse,
        )

    @classmethod
    def getSubscriptionInput(cls, input: BusinessObject) -> GetSubscriptionInputResponse:
        """
        The getSubscriptionInput operation retrieves the valid subscribable events the business object in the input can
        have. When an event is subscribable, that means subscriptions can be created for that event. A list of action
        handlers and attribute criteria is also retrieved. These events and handlers are populated after selection of
        an object that is to be subscribed.
        
        Use cases:
        The client selectes a subscribable business object to be able to create subscriptions on it. The client is
        returned with a list of event types and action handlers applicable on that business object. If there is an
        attribute criteria configuration file specified in the TC_DATA folder, the attribute criteria will be populated
        in the response for the business object type.
        """
        return cls.execute_soa_method(
            method_name='getSubscriptionInput',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=GetSubscriptionInputResponse,
        )

    @classmethod
    def modifySubscriptions(cls, inputs: List[ModifySubscriptionsInput2]) -> SubscriptionsResponse:
        """
        This operation modifies existing ImanSubscription objects.  All values specified in the inputs replace the
        values on the ImanSubscription in the database.  Each modification is verified to insure that a duplicate
        ImanSubscription is not created.
        
        Use cases:
        An existing Subscription needs to have one or more of its values modified.
        """
        return cls.execute_soa_method(
            method_name='modifySubscriptions',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'inputs': inputs},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def transferNotifications(cls, input: TransferNotificationInput) -> SubscriptionsResponse:
        """
        This operation transfers the ownership of a subscription The transfer can be temporary (for a selected date
        range) or permanent.
        """
        return cls.execute_soa_method(
            method_name='transferNotifications',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def createSubscriptions(cls, inputs: List[SubscriptionInput2]) -> SubscriptionsResponse:
        """
        This operation creates multiple object or class based Subscriptions based on the provided inputs. A
        Subscription allows a specified piece of functionality to be executed whenever an event occurs on the target
        object. Inputs to this operation will allow the target object to be specified, along with the event to monitor.
        The functionality the execute is specified by an array of ImanActionHandler objects. These handlers will be
        executed in the order they are specified in the Subscription definition. The most common handler would be
        IMAN_Smtp_Mail_Notify, which is used to send an e-mail when the event is triggered. If this handler is
        specified, the notification object should also be included as input.
        
        This operation also creates class based Subscriptions. This is done by passing a type object as the target
        object.  Class based Subscriptions will apply to all objects of the specified type. These can be filtered down
        at execution time by specifying a condition or attribute criteria as input. The Condition or attribute criteria
        will be evaluated against the object on which the event occurred, and the handler will only be executed if the
        Condition evaluates to TRUE.  Conditions and attribute criteria only apply for class based Subscriptions. 
        Attribute criteria are made up of a list of attributes and the values to compare them against off the target
        object.  Each of these comparisons can be logically combined.
        
        
        Use cases:
        Object Based Subscription:
        The client creates an object based Subscription in order to trigger functionality when a specific event occurs
        against the object. An example of this would be subscribing to the "Check Out" event for a given object. Any
        time the object is checked out, the handler functionality will be executed. Most often, this functionality will
        send the given user an e-mail notification.
        
        Class Based Subscription:
        The client creates a class based Subscription in order to trigger functionality when a specific event occurs
        against any object of the given type. An example of this would be subscribing to the "Check Out" event for an
        ItemRevision objects. Any time the object is checked out, the handler functionality will be executed. Most
        often, this functionality will send the given user an e-mail notification.
        
        Class based subscriptions allow a Condition or attribute criteria to be specified as part of the definition.
        This allows the events to be filtered to a smaller level. Any time the event occurs against the given object of
        the specified type, the Condition will be evaluated against the object. If the Condition or attribute criteria
        evaluate to true, the event is posted and the handlers are executed. An example Condition would only evaluate
        to true if the object is part of a specific Project.  Attribute criteria can also be specified and will be
        evaluated when the Subscription is being processed.  If the attribute criteria values do not match, the
        Subscription will be rejected.  Both attribute criteria and a Condition can not be specified at the same time.
        """
        return cls.execute_soa_method(
            method_name='createSubscriptions',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'inputs': inputs},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def findSubscriptions(cls, input: FindSubscriptionsInput2) -> SubscriptionsResponse:
        """
        This operation queries for all Subscriptions that meet the input criteria. A variety of input parameters are
        allowed, including target, event type, subscriber, condition, handlers, execution time, expiration date,
        notification priority, status and temporary transfer information.
        
        Use cases:
        The client is searching for a previously created Subscription against a given object or type.
        """
        return cls.execute_soa_method(
            method_name='findSubscriptions',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def getAssignEventData(cls) -> GetAssignEventDataResponse:
        """
        Description:
        The getAssignEventData operation retrieves the valid TaskType objects related to the assign event. When an
        event is subscribable, that means subscriptions can be created for that event. The attribute criteria for the
        subscription can be populated on the basis of the data returned using this operation.
        
        Use cases:
        The client selects a subscribable business object to be able to create subscriptions on it. The client is
        returned with a list of event types using the getSubscriptionInput operation. Then, if the user selects assign
        event, the list of TaskType objects is returned.
        """
        return cls.execute_soa_method(
            method_name='getAssignEventData',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={},
            response_cls=GetAssignEventDataResponse,
        )

    @classmethod
    def getAttachEventData(cls, target: BusinessObject) -> GetAttachEventDataResponse:
        """
        The getAttachEventData operation retrieves the lists of ImanRelation objects and attachment types applicable on
        the target object. When an event is subscribable, that means subscriptions can be created for that event. The
        attribute criteria for the subscription can be populated on the basis of the data returned using this operation.
        
        Use cases:
        The client selects a subscribable business object that will be the target object of a subscription. The client
        is returned with a list of event types using the getSubscriptionInput operation. Then, if the user selects
        attach event, the lists of ImanRelation objects and attachment types applicable on the target object are
        returned. 
        """
        return cls.execute_soa_method(
            method_name='getAttachEventData',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'target': target},
            response_cls=GetAttachEventDataResponse,
        )

    @classmethod
    def getEventTypes2(cls, input: List[EventObject]) -> GetEventTypesResponse:
        """
        The operation retrieves the valid auditable and subscribable events for each of the business objects in the
        input EventObject list. When an event is auditable, you can audit actions on Teamcenter objects when that event
        happens on the business object. When an event is subscribable, subscriptions can be created for that event.
        
        Use cases:
        The client selects a subscribable or an auditable business object. Upon selection, a list of applicable event
        types is returned.
        """
        return cls.execute_soa_method(
            method_name='getEventTypes2',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=GetEventTypesResponse,
        )


class MessageManagementService(TcService):

    @classmethod
    def getUserGroupAlias(cls) -> UserGroupAliasResponse:
        """
        This operation retrieves the list of all Teamcenter User, Group, and ImanAliasList objects.
        
        Use cases:
        The client needs a list of the users, groups or addresses to select from, for the notification of an event on
        an object. The user can then select from the populated lists of user, group or alias list objects to send the
        notification to.
        """
        return cls.execute_soa_method(
            method_name='getUserGroupAlias',
            library='Internal-Notification',
            service_date='2015_03',
            service_name='MessageManagement',
            params={},
            response_cls=UserGroupAliasResponse,
        )
