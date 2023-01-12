from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanSubscription
from tcsoa.gen.Internal.Notification._2015_10.SubscriptionManagement import ModifySubscriptionTemplateInput, SubscriptionTemplateResponse, GetAttachEventDataResponse2, SubscriptionTemplate, SaveAsSubscriptionInputData
from typing import List
from tcsoa.gen.Notification._2014_10.SubscriptionManagement import SubscriptionsResponse
from tcsoa.base import TcService
from tcsoa.gen.Internal.Notification._2015_10.MessageManagement import UnreadMessages


class MessageManagementService(TcService):

    @classmethod
    def getUnreadMessages(cls) -> UnreadMessages:
        """
        Get the Fnd0Message object UIDs of the unread messages for the current user. This operation is supported only
        in a 4Tier environment with a asyncronous messaging system installed. If called from a 2Tier client, an empty
        list will be returned.
        
        Use cases:
        The Active Workspace client calls the getUnreadMessages operation in a polling fashion to get the number of
        unread messages for the current user. This number is displayed in the client UI. When the user selects the
        message icon, the client will query the Teamcneter server for the full list of messages complete with details.
        
        Exceptions:
        >78040: The asynchronous messaging system is not installed or configured correctly. Please contact the system
        administrator to configure the Teamcenter server for asynchronous messaging support.
        """
        return cls.execute_soa_method(
            method_name='getUnreadMessages',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='MessageManagement',
            params={},
            response_cls=UnreadMessages,
        )

    @classmethod
    def initializeAsynchMessaging(cls) -> str:
        """
        Register the current user with the Broker , and initialize the list of unread messages for the current user in
        the Broker. The Broker is a component installed as part of the Pool Manager, and marshalls events from the
        Teamcenter server (result of this service operation) and the Subscription Manager  to the Message Cache module
        in the the Teamcenter web tier.
        
        Exceptions:
        >78043 Initialization of the aysnchronous messageing system failed. Please contact the system administrator.
        """
        return cls.execute_soa_method(
            method_name='initializeAsynchMessaging',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='MessageManagement',
            params={},
            response_cls=str,
        )


class SubscriptionManagementService(TcService):

    @classmethod
    def modifySubscriptionTemplates(cls, inputs: List[ModifySubscriptionTemplateInput]) -> SubscriptionTemplateResponse:
        """
        The modifySubscriptionTemplate operation modifies Fnd0SubscriptionTemplate objects.  Subscription templates are
        used to specify predefined criteria and closure rules during the creation of an Fnd0IndirectSubscription object.
        
        Use cases:
        The user wishes to modify an existing Fnd0SubscriptionTemplate instance object.  The user can pass modified
        values such as the name, description, subscribed object criteria, target object criteria or the closure rule. 
        The values from the input will be set on the specified Fnd0SubscriptionTemplate objects.
        """
        return cls.execute_soa_method(
            method_name='modifySubscriptionTemplates',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='SubscriptionManagement',
            params={'inputs': inputs},
            response_cls=SubscriptionTemplateResponse,
        )

    @classmethod
    def saveAsSubscription(cls, input: SaveAsSubscriptionInputData) -> SubscriptionsResponse:
        """
        The saveAsSubscription operation unsubscribes the current user from the input subscription and creates another
        subscription using the input subscription. The current user will be the subscriber, and the input name will be
        the name of the new subscription.
        
        Use cases:
        A user receives a notification for a subscription, but the user wishes to make a modification to the
        subscription and receive notifications on the basis of a new criterion. The user then performs
        saveAsSubscription and provides a new name to the subscription.
        """
        return cls.execute_soa_method(
            method_name='saveAsSubscription',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def unsubscribe(cls, subscriptions: List[ImanSubscription]) -> SubscriptionsResponse:
        """
        The unsubscribe operation takes a list of ImanSubscription objects as input and unsubscribes the user from the
        subscriptions. The current user is removed from the notification list, causing the user to stop receiving
        notification for that subscription.
        
        Use cases:
        A user who is in the notification list of a subscription receives a notification. The user can choose to
        unsubscribe from receiving these notifications by calling unsubscribe.
        """
        return cls.execute_soa_method(
            method_name='unsubscribe',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='SubscriptionManagement',
            params={'subscriptions': subscriptions},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def createSubscriptionTemplates(cls, inputs: List[SubscriptionTemplate]) -> SubscriptionTemplateResponse:
        """
        The createSubscriptionTemplates operation creates multiple Fnd0SubscriptionTemplate objects which are then used
        in the creation of indirect subscriptions. The traversal rule, primary object criteria and the target object
        criteria is used to process the Fnd0IndirectSubscription objects.
        
        Use cases:
        An admin user creates a Closure Rule using the PLMXML UI. Then using the Subscription Template creation UI in
        the Subscription admin application, the admin user picks a subscribed object type and defines the criteria on
        it, if any. Then a target object type is selected and its criteria are defined, if any. Then the user selects
        the TIE closure rule created and saves the template upon which the createSubscriptionTemplate operation is
        called. The template created can then be used for the creation of an Fnd0IndirectSubscription object.
        """
        return cls.execute_soa_method(
            method_name='createSubscriptionTemplates',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='SubscriptionManagement',
            params={'inputs': inputs},
            response_cls=SubscriptionTemplateResponse,
        )

    @classmethod
    def getApplicableSubscriptionTemplates(cls, subscribedObject: BusinessObject) -> SubscriptionTemplateResponse:
        """
        The getApplicableSubscriptionTemplates operation retrieves the applicable Fnd0SubscriptionTemplate objects
        based on the subscribed object data.
        """
        return cls.execute_soa_method(
            method_name='getApplicableSubscriptionTemplates',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='SubscriptionManagement',
            params={'subscribedObject': subscribedObject},
            response_cls=SubscriptionTemplateResponse,
        )

    @classmethod
    def getAttachEventData2(cls, target: BusinessObject) -> GetAttachEventDataResponse2:
        """
        The getAttachEventData2 operation retrieves the lists of relation objects and attachment types applicable on
        the target object. When an event is subscribable, that means subscriptions can be created for that event. The
        attribute criteria for the subscription can be populated on the basis of the data returned using this operation.
        
        Use cases:
        The client selects a subscribable business object that will be the target object of a subscription. The client
        is returned with a list of event types using the getSubscriptionInput operation. Then, if the user selects
        attach event, the lists of relation objects and attachment types applicable on the target object are returned.
        """
        return cls.execute_soa_method(
            method_name='getAttachEventData2',
            library='Internal-Notification',
            service_date='2015_10',
            service_name='SubscriptionManagement',
            params={'target': target},
            response_cls=GetAttachEventDataResponse2,
        )
