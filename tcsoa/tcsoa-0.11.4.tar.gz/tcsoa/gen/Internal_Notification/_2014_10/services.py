from __future__ import annotations

from tcsoa.gen.Internal.Notification._2014_10.SubscriptionManagement import GetSubscriptionConditionsResponse
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):

    @classmethod
    def getSubscriptionConditions(cls) -> GetSubscriptionConditionsResponse:
        """
        This operation returns all the Conditions that can be used with Subscriptions.  For a Condition to be used with
        a Subscription, its signature must contain a POM_object and a UserSession.
        
        The results of this operation will be used with the Subscription Manager UI that will allow the user to select
        a Condition for use with a Subscription.
        
        Use cases:
        The client is searching for a list of all Conditions that have the correct signature to be used with
        Subscriptions.  This list will be displayed to the user from the Subscription Manager UI.
        """
        return cls.execute_soa_method(
            method_name='getSubscriptionConditions',
            library='Internal-Notification',
            service_date='2014_10',
            service_name='SubscriptionManagement',
            params={},
            response_cls=GetSubscriptionConditionsResponse,
        )
