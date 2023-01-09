import aiohttpx
import datetime
import uuid
import functools

from typing import Optional, Callable, Dict, Union, List

from lazyops.types import lazyproperty
from lazyops.utils import is_coro_func, timer
from aiolago.schemas import *
from aiolago.utils.logs import logger
from aiolago.utils.config import LagoSettings
from aiolago.utils.config import settings as lago_settings

from aiolago.utils.helpers import full_name
from aiolago.routes import ApiRoutes


class LagoClient:
    """
    Main Client for all the routes in the API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        api_path: Optional[str] = None,
        headers: Optional[Dict] = None,
        debug_enabled: Optional[bool] = None,
        on_error: Optional[Callable] = None,
        timeout: Optional[int] = None,
        api_key_header: Optional[str] = None,
        ignore_errors: Optional[bool] = None,
        settings: Optional[LagoSettings] = None,
        **kwargs
    ):
        settings = settings or lago_settings

        self.api_key = api_key if api_key is not None else settings.api_key
        self.api_url = settings.get_api_url(host = host, port = port, scheme = scheme, url = url)
        self.base_url = settings.get_base_api_url(host = host, port = port, scheme = scheme, url = url, api_path = api_path)
        self.debug_enabled = debug_enabled if debug_enabled is not None else lago_settings.debug_enabled
        
        self.timeout = timeout if timeout is not None else settings.timeout
        self.headers = headers if headers is not None else settings.get_headers(api_key = self.api_key, api_key_header = api_key_header)
        self.on_error = on_error
        self.ignore_errors = ignore_errors if ignore_errors is not None else settings.ignore_errors
        self._kwargs = kwargs
        self.log_method = logger.info if self.debug_enabled else logger.debug
        self.client = aiohttpx.Client(
            base_url = self.base_url,
            timeout = self.timeout,
        )

        self.routes = ApiRoutes(
            client = self.client,
            headers = self.headers,
            debug_enabled = self.debug_enabled,
            on_error = self.on_error,
            ignore_errors = self.ignore_errors,
            timeout = self.timeout,
            **self._kwargs
        )
        logger.info(f"Lago Client initialized: {self.client.base_url}")
        if self.debug_enabled:
            logger.debug(f"Debug Enabled: {self.debug_enabled}")


    @lazyproperty
    def add_ons(self) -> AddOnRoute:
        return self.routes.add_ons
    
    @lazyproperty
    def applied_add_ons(self) -> AppliedAddOnRoute:
        return self.routes.applied_add_ons
    
    @lazyproperty
    def applied_coupons(self) -> AppliedCouponRoute:
        return self.routes.applied_coupons
    
    @lazyproperty
    def billable_metrics(self) -> BillableMetricRoute:
        return self.routes.billable_metrics
    
    @lazyproperty
    def coupons(self) -> CouponRoute:
        return self.routes.coupons
    
    @lazyproperty
    def customers(self) -> CustomerRoute:
        return self.routes.customers
    
    @lazyproperty
    def events(self) -> EventRoute:
        return self.routes.events
    
    @lazyproperty
    def invoices(self) -> InvoiceRoute:
        return self.routes.invoices
    
    @lazyproperty
    def organizations(self) -> OrganizationRoute:
        return self.routes.organizations
    
    @lazyproperty
    def plans(self) -> PlanRoute:
        return self.routes.plans
    
    @lazyproperty
    def subscriptions(self) -> SubscriptionRoute:
        return self.routes.subscriptions
    
    @lazyproperty
    def wallets(self) -> WalletRoute:
        return self.routes.wallets
    
    @lazyproperty
    def wallet_transactions(self) -> WalletTransactionRoute:
        return self.routes.wallet_transactions
    
    @lazyproperty
    def webhooks(self) -> WebhookRoute:
        return self.routes.webhooks
    

    """
    Context Managers
    """

    async def async_close(self):
        await self.client.aclose()
    
    def close(self):
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.async_close()


    """
    Function Decorators
    """
    def on_event(
        self,
        customer_id: Optional[Union[str, Callable]] = None,
        metric_id: Optional[Union[str, Callable]] = None,
        transaction_id: Optional[Union[str, Callable]] = None,
        
        properties: Optional[Union[Dict, Callable]] = None,
        timestamp: Optional[float] = None,
        exclude_properties: Optional[List[str]] = None,
        exclude_on: Optional[Callable] = None,
        extra_properties: Optional[Dict] = None,
        extra_properties_func: Optional[Callable] = None,
        include_duration: Optional[bool] = False,

        include_results: Optional[bool] = True,
        include_args_in_properties: Optional[bool] = False,
        include_kwargs_in_properties: Optional[bool] = False,
        usage_callback: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Lago Event Decorator to log events to the Lago API.
        Most params are either _str_ or _Callable_ which will pass the function's arguments 
        and expects a _str_ to be returned. If required parameters are not provided, the 
        event logging will not occur.

        Example:

        >>> @Lago.on_event(customer_id = get_customer_id)
        ... def my_func(headers: Dict, params: Dict):
        ...     ...

        >>> @Lago.on_event(customer_id="1234")
        ... async def async_run_func():
        ...     ...

        >>> @Lago.on_event(customer_id="1234", metric_id="my_event")
        ... def run_func():
        ...     ...

        :param customer_id: The customer_id to log the event to. (required)
        :param metric_id: The `metric_id` which correlates to a `BillableMetrics` to log. [also known as `code`]. defaults to the function name.
        :param transaction_id: Unique identifer of the event in your application. Defaults to a unique uuid.

        :param properties: A dictionary of parameters to log with the event. Defaults 
        to the function's arguments.
        :param created_at: The time the event occurred. Defaults to the current time.

        :param exclude_properties: A list of properties to exclude from the event.
        :param exclude_on: A function that takes validates whether this event should be logged.

        :param extra_properties: A dictionary of extra properties to add to the event.
        :param extra_properties_func: A function that takes the function's arguments and returns
        a dictionary of extra properties to add to the event.
        
        :param include_duration: Whether to include the duration of the function in the event.
        :param include_results: Whether to include the results of the function in the event.
        :param include_args_in_properties: Whether to include the arguments of the function in
        the properties of the event.
        :param include_kwargs_in_properties: Whether to include the keyword arguments of the function in
        the properties of the event.

        :param usage_callback: A function that is the final step of the event logging. 
        It should take all the arguments of the function and results of the function and
        return a dictionary of usage properties to log return to the event.
        It should take the following keyword arguments:
            - result: Any The result of the function.
            - properties: Dict The properties of the event.
            - args: List The arguments of the function.
            - kwargs: Dict The keyword arguments of the function.
            - wrapper_kwargs: Dict The keyword arguments of the decorator.

        """

        wrapper_kwargs = kwargs or {}
        def decorator(func):
            if is_coro_func(func):
                @functools.wraps(func)
                async def wrapper(*args, **kwargs):

                    # validate exclude_on
                    if exclude_on is not None:
                        if is_coro_func(exclude_on) and await exclude_on(*args, **kwargs, **wrapper_kwargs):
                            return await func(*args, **kwargs)
                        elif exclude_on(*args, **kwargs):
                            return await func(*args, **kwargs)

                    # validate customer_id
                    if customer_id is None:
                        logger.error("customer_id is required for event logging.")
                        return await func(*args, **kwargs)
                    
                    _customer_id = customer_id
                    if callable(customer_id):
                        if is_coro_func(customer_id):
                            _customer_id = await customer_id(*args, **kwargs, **wrapper_kwargs)
                        else:
                            _customer_id = customer_id(*args, **kwargs, **wrapper_kwargs)
                    
                    # validate metric_id
                    if metric_id is None:
                        _metric_id = full_name(func)
                    elif callable(metric_id):
                        if is_coro_func(metric_id):
                            _metric_id = await metric_id(*args, **kwargs, **wrapper_kwargs)
                        else:
                            _metric_id = metric_id(*args, **kwargs, **wrapper_kwargs)
                    
                    
                    # validate/handle properties
                    event_properties = {
                        'operation_type': 'add'
                    }
                    if properties is not None:
                        if callable(properties):
                            if is_coro_func(properties):
                                event_properties = await properties(*args, **kwargs, **wrapper_kwargs)
                            else:
                                event_properties = properties(*args, **kwargs, **wrapper_kwargs)
                        else:
                            event_properties = properties
                    
                    if extra_properties:
                        event_properties.update(extra_properties)
                    
                    if extra_properties_func:
                        if is_coro_func(extra_properties_func):
                            event_properties.update(await extra_properties_func(*args, **kwargs, **wrapper_kwargs))
                        else:
                            event_properties.update(extra_properties_func(*args, **kwargs, **wrapper_kwargs))
                    
                    if exclude_properties:
                        for prop in exclude_properties:
                            event_properties.pop(prop, None)
                    
                    duration_s = timer() if include_duration else None
                    result = await func(*args, **kwargs)
                    if include_duration: event_properties['duration_s'] = timer(duration_s)
                    if include_results: event_properties['results'] = result

                    # Handle including args and kwargs in properties
                    if include_args_in_properties:
                        event_properties['args'] = args
                    if include_kwargs_in_properties:
                        event_properties['kwargs'] = kwargs
                    
                    # validate/handle transaction_id
                    if transaction_id is None:
                        _transaction_id = str(uuid.uuid4())
                    elif callable(transaction_id):
                        if is_coro_func(transaction_id):
                            _transaction_id = await transaction_id(*args, **kwargs, **wrapper_kwargs)
                        else:
                            _transaction_id = transaction_id(*args, **kwargs, **wrapper_kwargs)
                    
                    # validate/handle usage_callback
                    if usage_callback is not None:
                        if is_coro_func(usage_callback):
                            event_properties = await usage_callback(args = args, result = result, properties = event_properties, kwargs = kwargs, wrapper_kwargs = wrapper_kwargs)
                        else:
                            event_properties = usage_callback(args = args, result = result, properties = event_properties, kwargs = kwargs, wrapper_kwargs = wrapper_kwargs)

                    try:
                        await self.events.async_create(
                            transaction_id = _transaction_id,
                            external_customer_id = _customer_id,
                            code = _metric_id,
                            properties = event_properties,
                            timestamp = timestamp,
                            **kwargs,
                        )
                    except Exception as e:
                        logger.error(f"Error logging event: {e}")
                    return result
            
            else:
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    # validate exclude_on
                    if exclude_on is not None and exclude_on(*args, **kwargs, **wrapper_kwargs):
                        return func(*args, **kwargs)

                    # validate customer_id
                    if customer_id is None:
                        logger.error("customer_id is required for event logging.")
                        return func(*args, **kwargs)
                    
                    _customer_id = customer_id
                    if callable(customer_id):
                        _customer_id = customer_id(*args, **kwargs, **wrapper_kwargs)
                    
                    # validate event_name
                    if metric_id is None:
                        _metric_id = full_name(func)
                    elif callable(metric_id):
                        _metric_id = metric_id(*args, **kwargs, **wrapper_kwargs)
                    
                    
                    # validate/handle properties
                    event_properties = {
                        'operation_type': 'add'
                    }
                    if properties is not None:
                        if callable(properties):
                            event_properties = properties(*args, **kwargs, **wrapper_kwargs)
                        else:
                            event_properties = properties
                    
                    if extra_properties:
                        event_properties.update(extra_properties)
                    
                    if extra_properties_func:
                        event_properties.update(extra_properties_func(*args, **kwargs, **wrapper_kwargs))
                    
                    if exclude_properties:
                        for prop in exclude_properties:
                            event_properties.pop(prop, None)
                    
                    duration_s = timer() if include_duration else None
                    result = func(*args, **kwargs)
                    
                    if include_duration: event_properties['duration_s'] = timer(duration_s)
                    if include_results: event_properties['results'] = result
                    
                    # Handle including args and kwargs in properties
                    if include_args_in_properties:
                        event_properties['args'] = args
                    if include_kwargs_in_properties:
                        event_properties['kwargs'] = kwargs

                    # validate/handle transaction_id
                    if transaction_id is None:
                        _transaction_id = str(uuid.uuid4())
                    elif callable(transaction_id):
                        _transaction_id = transaction_id(*args, **kwargs, **wrapper_kwargs)
                    
                    # validate/handle usage_callback
                    if usage_callback is not None:
                        event_properties = usage_callback(args = args, result = result, properties = event_properties, kwargs = kwargs, wrapper_kwargs = wrapper_kwargs)


                    try:
                        self.events.create(
                            transaction_id = _transaction_id,
                            external_customer_id = _customer_id,
                            code = _metric_id,
                            properties = event_properties,
                            timestamp = timestamp,
                            **kwargs,
                        )
                    except Exception as e:
                        logger.error(f"Error logging metric: {e}")

                    return result
                
            return wrapper
        return decorator



class LagoAPI:

    settings: Optional[LagoSettings] = lago_settings
    _api: Optional[LagoClient] = None

    """
    The Global Class for Lago API.
    """

    def configure(
        self, 
        api_key: Optional[str] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        api_path: Optional[str] = None,

        debug_enabled: Optional[bool] = None,
        on_error: Optional[Callable] = None,
        timeout: Optional[int] = None,
        api_key_header: Optional[str] = None,
        ignore_errors: Optional[bool] = None,

        reset: Optional[bool] = True,
        **kwargs
    ):
        """
        Configure the global Lago client.
        """
        self.settings.configure(
            api_key=api_key,
            url=url,
            scheme=scheme,
            host=host,
            port=port,
            api_path=api_path,
            debug_enabled=debug_enabled,
            on_error=on_error,
            timeout=timeout,
            api_key_header=api_key_header,
            ignore_errors=ignore_errors,
            **kwargs
        )

        if reset: self._api = None
        if self._api is None:
            self.get_api(**kwargs)
    
    def get_api(self, **kwargs) -> LagoClient:
        if self._api is None:
            self._api = LagoClient(settings = self.settings, **kwargs)
        return self._api
    
    @property
    def api(self) -> LagoClient:
        """
        Returns the inherited Lago client.
        """
        if self._api is None:
            self.configure()
        return self._api
    

    @property
    def add_ons(self) -> AddOnRoute:
        """
        Returns the `AddOnRoute` class for interacting with add-ons.
        
        Doc: `https://doc.getlago.com/docs/api/add_ons/add-on-object`
        """
        return self.api.add_ons
    

    @property
    def applied_add_ons(self) -> AppliedAddOnRoute:
        """
        Returns the `AppliedAddOnRoute` class for interacting with applied add-ons.
        
        Doc: `https://doc.getlago.com/docs/api/add_ons/apply-add-on`
        """
        return self.api.applied_add_ons
    

    @property
    def applied_coupons(self) -> AppliedCouponRoute:
        """
        Returns the `AppliedCouponRoute` class for interacting with applied coupons.

        Doc: `https://doc.getlago.com/docs/api/coupons/coupon-object`
        """
        return self.api.applied_coupons
    

    @property
    def billable_metrics(self) -> BillableMetricRoute:
        """
        Returns the `BillableMetricRoute` class for interacting with billable metrics.

        Doc: `https://doc.getlago.com/docs/api/billable_metrics/billable-metric-object`
        """
        return self.api.billable_metrics
    

    @property
    def coupons(self) -> CouponRoute:
        """
        Returns the `CouponRoute` class for interacting with coupons.

        Doc: `https://doc.getlago.com/docs/api/coupons/coupon-object`
        """
        return self.api.coupons
    

    @property
    def customers(self) -> CustomerRoute:
        """
        Returns the `CustomerRoute` class for interacting with customers.

        Doc: `https://doc.getlago.com/docs/api/customers/customer-object`
        """
        return self.api.customers
    

    @property
    def events(self) -> EventRoute:
        """
        Returns the `EventRoute` class for interacting with events.

        Doc: `https://doc.getlago.com/docs/api/events/event-object`
        """
        return self.api.events
    

    @property
    def invoices(self) -> InvoiceRoute:
        """
        Returns the `InvoiceRoute` class for interacting with invoices.

        Doc: `https://doc.getlago.com/docs/api/invoices/invoice-object`
        """
        return self.api.invoices
    

    @property
    def organizations(self) -> OrganizationRoute:
        """
        Returns the `OrganizationRoute` class for interacting with organizations.

        Doc: `https://doc.getlago.com/docs/api/organizations/organization-object`
        """
        return self.api.organizations
    

    @property
    def plans(self) -> PlanRoute:
        """
        Returns the `PlanRoute` class for interacting with plans.

        Doc: `https://doc.getlago.com/docs/api/plans/plan-object`
        """
        return self.api.plans
    

    @property
    def subscriptions(self) -> SubscriptionRoute:
        """
        Returns the `SubscriptionRoute` class for interacting with subscriptions.

        Doc: `https://doc.getlago.com/docs/api/subscriptions/subscription-object`
        """
        return self.api.subscriptions
    

    @property
    def wallets(self) -> WalletRoute:
        """
        Returns the `WalletRoute` class for interacting with wallets.

        Doc: `https://doc.getlago.com/docs/api/wallets/wallet-object`
        """
        return self.api.wallets
    

    @property
    def wallet_transactions(self) -> WalletTransactionRoute:
        """
        Returns the `WalletTransactionRoute` class for interacting with wallet transactions.

        Doc: `https://doc.getlago.com/docs/api/wallets/wallet-transaction-object`
        """
        return self.api.wallet_transactions
    

    @property
    def webhooks(self) -> WebhookRoute:
        """
        Returns the `WebhookRoute` class for interacting with webhooks.

        Doc: `https://doc.getlago.com/docs/api/webhooks/webhook-object`
        """
        return self.api.webhooks
    
    def on_event(
        self,
        customer_id: Optional[Union[str, Callable]] = None,
        metric_id: Optional[Union[str, Callable]] = None,
        transaction_id: Optional[Union[str, Callable]] = None,
        
        properties: Optional[Union[Dict, Callable]] = None,
        created_at: Optional[datetime.datetime] = None,
        exclude_properties: Optional[List[str]] = None,
        exclude_on: Optional[Callable] = None,
        extra_properties: Optional[Dict] = None,
        extra_properties_func: Optional[Callable] = None,
        include_duration: Optional[bool] = False,
        include_results: Optional[bool] = True,
        include_args_in_properties: Optional[bool] = False,
        include_kwargs_in_properties: Optional[bool] = False,

        usage_callback: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Lago Event Decorator to log events to the Lago API.
        Most params are either _str_ or _Callable_ which will pass the function's arguments 
        and expects a _str_ to be returned. If required parameters are not provided, the 
        event logging will not occur.

        Example:

        >>> @Lago.on_event(customer_id = get_customer_id)
        ... def my_func(headers: Dict, params: Dict):
        ...     ...

        >>> @Lago.on_event(customer_id="1234")
        ... async def async_run_func():
        ...     ...

        >>> @Lago.on_event(customer_id="1234", metric_id="my_event")
        ... def run_func():
        ...     ...

        :param customer_id: The customer_id to log the event to. (required)
        :param metric_id: The `metric_id` which correlates to a `BillableMetrics` to log. [also known as `code`]. defaults to the function name.
        :param transaction_id: Unique identifer of the event in your application. Defaults to a unique uuid.

        :param properties: A dictionary of parameters to log with the event. Defaults 
        to the function's arguments.
        :param created_at: The time the event occurred. Defaults to the current time.

        :param exclude_properties: A list of properties to exclude from the event.
        :param exclude_on: A function that takes validates whether this event should be logged.

        :param extra_properties: A dictionary of extra properties to add to the event.
        :param extra_properties_func: A function that takes the function's arguments and returns
        a dictionary of extra properties to add to the event.
        
        :param include_duration: Whether to include the duration of the function in the event.
        :param include_results: Whether to include the results of the function in the event.
        :param include_args_in_properties: Whether to include the arguments of the function in
        the properties of the event.
        :param include_kwargs_in_properties: Whether to include the keyword arguments of the function in
        the properties of the event.
        :param usage_callback: A function that is the final step of the event logging. 
        It should take all the arguments of the function and results of the function and
        return a dictionary of usage properties to log return to the event.
        It should take the following keyword arguments:
            - result: Any The result of the function.
            - properties: Dict The properties of the event.
            - args: List The arguments of the function.
            - kwargs: Dict The keyword arguments of the function.
            - wrapper_kwargs: Dict The keyword arguments of the decorator.


        """
        return self.api.on_event(
            customer_id=customer_id,
            metric_id=metric_id,
            transaction_id=transaction_id,
            properties=properties,
            created_at=created_at,
            exclude_properties=exclude_properties,
            exclude_on=exclude_on,
            extra_properties=extra_properties,
            extra_properties_func=extra_properties_func,
            include_duration=include_duration,
            include_results=include_results,
            include_args_in_properties=include_args_in_properties,
            include_kwargs_in_properties=include_kwargs_in_properties,
            usage_callback=usage_callback,
            **kwargs,
        )

    """
    Context Managers
    """

    async def async_close(self):
        if self._api is not None:
            await self._api.async_close()
    
    def close(self):
        if self._api is not None:
            self._api.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.async_close()


    
Lago: LagoAPI = LagoAPI()







