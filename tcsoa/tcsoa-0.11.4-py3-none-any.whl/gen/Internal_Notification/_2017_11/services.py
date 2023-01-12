from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Notification._2017_11.SubscriptionManagement import GetSubscribablePropertiesResponse
from typing import List
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):

    @classmethod
    def getSubscribableProperties(cls, subscribableObjectTypes: List[BusinessObject]) -> GetSubscribablePropertiesResponse:
        """
        This operation returns a list of properties for the given subscribable object type to build subscription
        criteria for class based subscriptions.
        
        Use cases:
        This operation provides the following use case for Subscription:
        
        Use Case1: Display list of configured properties for subscribable object type to build subscription criteria
        for class based subscription.
        Administrator may configure subscription criteria properties for a subscribable object type using Subscription
        Administration Panel in RAC.
        - This operation returns list of configured properties if defined, for selected subscribable object type which
        can be used to build subscription criteria for class based subscription.
        - If the configuration is not defined by the admin for the selected subscribable object type than it will get
        configuration from its parent type up in the hierarchy until it finds one.
        - If configuration is not defined for the subscribable object type and all its parent type than default will
        list all properties for selected subscribable object type.
        
        """
        return cls.execute_soa_method(
            method_name='getSubscribableProperties',
            library='Internal-Notification',
            service_date='2017_11',
            service_name='SubscriptionManagement',
            params={'subscribableObjectTypes': subscribableObjectTypes},
            response_cls=GetSubscribablePropertiesResponse,
        )
