from typing import Optional, Type, Dict, Union, List, Type, Any
from aiolago.types.base import BaseRoute, BaseResource, lazyproperty
from aiolago.types.errors import LagoApiError
from aiolago.schemas.customer import CustomerUsageResponse

__all__ = [
    'Subscription',
    'SubscriptionResponse',
    'SubscriptionRoute',
    'SubscriptionUsageResponse',
]


class Subscription(BaseResource):
    plan_code: Optional[str]
    external_customer_id: Optional[str]
    name: Optional[str]
    external_id: Optional[str]
    subscription_date: Optional[str]
    billing_time: Optional[str]


class SubscriptionResponse(BaseResource):
    lago_id: str
    lago_customer_id: Optional[str]
    external_customer_id: Optional[str]
    canceled_at: Optional[str]
    created_at: Optional[str]
    plan_code: Optional[str]
    started_at: Optional[str]
    status: Optional[str]
    name: Optional[str]
    external_id: Optional[str]
    billing_time: Optional[str]
    terminated_at: Optional[str]
    subscription_date: Optional[str]
    previous_plan_code: Optional[str]
    next_plan_code: Optional[str]
    downgrade_plan_date: Optional[str]


class SubscriptionUsageResponse(SubscriptionResponse):
    usage: Optional[CustomerUsageResponse]


class SubscriptionRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Subscription
    response_model: Optional[Type[BaseResource]] = SubscriptionResponse
    usage_model: Optional[Type[BaseResource]] = None

    @lazyproperty
    def api_resource(self):
        return 'subscriptions'

    @lazyproperty
    def root_name(self):
        return 'subscription'
    
    def find(
        self, 
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> SubscriptionUsageResponse:
        """
        GET a Single Subscription

        :param resource_id: The ID of the Resource to GET [or external_subscription_id]
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param params: Optional Query Parameters
        """
        # So this is a bit different since we need to fetch all subscriptions first
        # and then fetch the usage information
        subscriptions: List[SubscriptionResponse] = self.find_all(
            external_customer_id = external_customer_id,
            params = params,
            with_index = False,
        )
        external_subscription_id = external_subscription_id or resource_id
        subscription: SubscriptionResponse = next(
            (
                sub
                for sub in subscriptions
                if (sub.external_id == external_subscription_id or sub.lago_id == external_subscription_id)
            ),
            None,
        )
        if subscription is None:
            raise LagoApiError(f'Could not find subscription with external_customer_id: {external_subscription_id}')

        api_resource = f'customers/{subscription.external_customer_id}/current_usage'
        if not params: params = {}
        params['external_subscription_id'] = subscription.external_id
        api_response = self._send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = self.headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json().get("customer_usage")
        usage = self.prepare_response(data, response_object = CustomerUsageResponse)
        return SubscriptionUsageResponse(**subscription.dict(), usage = usage)


    async def async_find(
        self, 
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    )  -> SubscriptionUsageResponse:
        """
        GET a Single Subscription

        :param resource_id: The ID of the Resource to GET [or external_subscription_id]
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param params: Optional Query Parameters
        """
        subscriptions: List[SubscriptionResponse] = await self.async_find_all(
            external_customer_id = external_customer_id,
            params = params,
            with_index = False,
        )
        external_subscription_id = external_subscription_id or resource_id
        subscription: SubscriptionResponse = next(
            (
                sub
                for sub in subscriptions
                if (sub.external_id == external_subscription_id or sub.lago_id == external_subscription_id)
            ),
            None,
        )
        if subscription is None:
            raise LagoApiError(f'Could not find subscription with external_customer_id: {external_subscription_id}')

        api_resource = f'customers/{subscription.external_customer_id}/current_usage'
        if not params: params = {}
        params['external_subscription_id'] = subscription.external_id
        api_response = await self._async_send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = self.headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json().get("customer_usage")
        usage = self.prepare_response(data, response_object = CustomerUsageResponse)
        return SubscriptionUsageResponse(**subscription.dict(), usage = usage)

    
    def get(
        self, 
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> SubscriptionUsageResponse:
        """
        GET a Single Subscription

        :param resource_id: The ID of the Resource to GET [or external_subscription_id]
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param params: Optional Query Parameters
        """
        return self.find(external_subscription_id = external_subscription_id, external_customer_id = external_customer_id, resource_id = resource_id, params = params, **kwargs)
    
    async def async_get(
        self,
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> SubscriptionUsageResponse:
        """
        GET a Single Subscription

        :param resource_id: The ID of the Resource to GET [or external_subscription_id]
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param params: Optional Query Parameters
        """
        return await self.async_find(external_subscription_id = external_subscription_id, external_customer_id = external_customer_id, resource_id = resource_id, params = params, **kwargs)

    
    def find_all(
        self, 
        resource_id: Optional[str] = None,
        external_customer_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        with_index: Optional[bool] = False,
        **kwargs
    ) -> Union[Dict[str, Union[List[SubscriptionResponse], Dict[str, Any]]], List[SubscriptionResponse]]:
        """
        GET all available subscriptions for a customer

        :param resource_id: The ID of the Resource to GET [or external_customer_
        :param external_customer_id: The customer ID
        :param params: Optional Query Parameters
        :param with_index: If set to true, the index of the resource will be returned

        :return: Dict[str, Union[List[Type[SubscriptionResponse]], Dict[str, Any]]]
        """
        if params is None: params = {}
        params['external_customer_id'] = external_customer_id or resource_id
        api_response = self._send(
            method = 'GET',
            url = self.api_resource,
            params = params,
            headers = self.headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        result = self.prepare_index_response(data)
        if not with_index: result = result.get(self.api_resource)
        return result

    async def async_find_all(
        self, 
        resource_id: Optional[str] = None,
        external_customer_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        with_index: Optional[bool] = False,
        **kwargs
    ) -> Union[Dict[str, Union[List[SubscriptionResponse], Dict[str, Any]]], List[SubscriptionResponse]]:
        """
        GET all available subscriptions for a customer

        :param resource_id: The ID of the Resource to GET [or external_customer_
        :param external_customer_id: The customer ID
        :param params: Optional Query Parameters
        :param with_index: If set to true, the index of the resource will be returned

        :return: Dict[str, Union[List[Type[SubscriptionResponse]], Dict[str, Any]]]
        """
        if params is None: params = {}
        params['external_customer_id'] = external_customer_id or resource_id
        api_response = await self._async_send(
            method = 'GET',
            url = self.api_resource,
            params = params,
            headers = self.headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        result = self.prepare_index_response(data)
        if not with_index: result = result.get(self.api_resource)
        return result
    
    def get_all(
        self,
        resource_id: Optional[str] = None,
        external_customer_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        with_index: Optional[bool] = False,
        **kwargs
    ) -> Union[Dict[str, Union[List[SubscriptionResponse], Dict[str, Any]]], List[SubscriptionResponse]]:
        """
        GET all available subscriptions for a customer

        :param resource_id: The ID of the Resource to GET [or external_customer_
        :param external_customer_id: The customer ID
        :param params: Optional Query Parameters
        :param with_index: If set to true, the index of the resource will be returned

        :return: Dict[str, Union[List[Type[SubscriptionResponse]], Dict[str, Any]]]
        """
        return self.find_all(resource_id = resource_id, external_customer_id = external_customer_id, params = params, with_index = with_index, **kwargs)
    
    async def async_get_all(
        self,
        resource_id: Optional[str] = None,
        external_customer_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        with_index: Optional[bool] = False,
        **kwargs
    ) -> Union[Dict[str, Union[List[SubscriptionResponse], Dict[str, Any]]], List[SubscriptionResponse]]:
        """
        GET all available subscriptions for a customer

        :param resource_id: The ID of the Resource to GET [or external_customer_
        :param external_customer_id: The customer ID
        :param params: Optional Query Parameters
        :param with_index: If set to true, the index of the resource will be returned

        :return: Dict[str, Union[List[Type[SubscriptionResponse]], Dict[str, Any]]]
        """
        return await self.async_find_all(resource_id = resource_id, external_customer_id = external_customer_id, params = params, with_index = with_index, **kwargs)
    

    """
    Extra Methods
    """

    def exists(
        self,
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[SubscriptionUsageResponse, bool]:
        """
        See whether a Subscription Exists

        :param resource_id: The ID of the Resource to GET [or external_subscription_id]
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param params: Optional Query Parameters
        """
        try:
            return self.find(external_customer_id = external_customer_id, resource_id = resource_id, external_subscription_id = external_subscription_id, params = params,  **kwargs)
        except Exception:
            return False
    
    async def async_exists(
        self,
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[SubscriptionUsageResponse, bool]:
        """
        See whether a Resource Exists

        :param resource_id: The ID of the Resource to GET [or external_subscription_id]
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param params: Optional Query Parameters
        """
        try:
            return await self.async_find(external_customer_id = external_customer_id, resource_id = resource_id, external_subscription_id = external_subscription_id, params = params, **kwargs)
        except Exception:
            return False
    
    def upsert(
        self,
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        input_object: Optional[Type[Subscription]] = None,
        update_existing: bool = False, 
        overwrite_existing: bool = False,
        **kwargs
    ):
        """
        Upsert a Subscription
        Validates whether the Subscription exists, and if it does, updates it. 
        If it doesn't, creates it.
        If update_existing is True, it will always update the Resource
        If overwrite_existing is True, it will re-create the Resource

        :resource_id: The ID of the Resource to Upsert
        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :param input_object: Input Object to Upsert
        :param update_existing (bool): Whether to update the Resource if it exists
        :overwrite_existing (bool): Whether to overwrite the Resource if it exists
        """
        resource = self.exists(external_customer_id = external_customer_id, resource_id = resource_id, external_subscription_id = external_subscription_id, **kwargs)
        if resource is not None:
            if update_existing:
                return self.update(input_object = input_object, identifier = (external_subscription_id or resource_id), **kwargs)
            if overwrite_existing:
                self.destroy(resource_id = (external_subscription_id or resource_id), **kwargs)
                return self.create(
                    input_object = input_object, 
                    external_id = kwargs.pop('external_id', (external_subscription_id or resource_id)),
                    external_customer_id = external_customer_id,
                    **kwargs
                )
            return resource
        return self.create(
            input_object = input_object, 
            external_id = kwargs.pop('external_id', (external_subscription_id or resource_id)),
            external_customer_id = external_customer_id,
            **kwargs
        )
    
    async def async_upsert(
        self,
        external_customer_id: str,
        resource_id: Optional[str] = None,
        external_subscription_id: Optional[str] = None,
        input_object: Optional[Type[Subscription]] = None,
        update_existing: bool = False, 
        overwrite_existing: bool = False,
        **kwargs
    ):
        """
        Upsert a Resource
        Validates whether the Resource exists, and if it does, updates it. 
        If it doesn't, creates it.
        If update_existing is True, it will always update the Resource
        If overwrite_existing is True, it will re-create the Resource

        :param external_subscription_id: The ID of the External Subscription [or resource_id]
        :param external_customer_id: The ID of the External Customer
        :resource_id: The ID of the Resource to Upsert
        :param input_object: Input Object to Upsert
        :param update_existing (bool): Whether to update the Resource if it exists
        :overwrite_existing (bool): Whether to overwrite the Resource if it exists
        """
        resource = await self.async_exists(external_customer_id = external_customer_id, resource_id = resource_id, external_subscription_id = external_subscription_id, **kwargs)
        if resource is not None:
            if update_existing:
                return self.async_update(input_object = input_object, identifier = (external_subscription_id or resource_id), **kwargs)
            if overwrite_existing:
                await self.async_destroy(resource_id = (external_subscription_id or resource_id), **kwargs)
                return await self.async_create(
                    input_object = input_object, 
                    external_id = kwargs.pop('external_id', (external_subscription_id or resource_id)),
                    external_customer_id = external_customer_id,
                    **kwargs
                )
            return resource
        return await self.async_create(
            input_object = input_object, 
            external_id = kwargs.pop('external_id', (external_subscription_id or resource_id)),
            external_customer_id = external_customer_id,
            **kwargs
        )
