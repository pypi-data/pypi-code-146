import aiohttpx

from typing import Optional, Callable
from aiologto.schemas import *
from aiologto.utils.config import LogtoSettings
from aiologto.utils.config import settings as logto_settings

RouteClasses = {
    # 'oidc': OidcRoute,
    'users': UserRoute,
}

class ApiRoutes:

    """
    Container for all the routes in the API.
    """
    oidc: OidcRoute = None
    users: UserRoute = None
    
    def __init__(
        self,
        client: aiohttpx.Client,
        debug_enabled: Optional[bool] = False,
        on_error: Optional[Callable] = None,
        ignore_errors: Optional[bool] = False,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        settings: Optional[LogtoSettings] = None,
        **kwargs
    ):
        self.client = client
        self.settings = settings or logto_settings

        self.debug_enabled = debug_enabled
        self.on_error = on_error
        self.ignore_errors = ignore_errors
        self.timeout = timeout
        self.max_retries = max_retries
        self.kwargs = kwargs or {}
        self.init_routes()


    def init_routes(self):
        """
        Initialize the API Routes
        """
        # Manually initialize oidc first
        # so that its header func can be passed to the 
        # other routes.
        self.oidc = OidcRoute(
            client = self.client,
            debug_enabled = self.debug_enabled,
            on_error = self.on_error,
            ignore_errors = self.ignore_errors,
            timeout = self.timeout,
            max_retries = self.max_retries,
            settings = self.settings,
            **self.kwargs
        )
        for route, route_class in RouteClasses.items():
            setattr(self, route, route_class(
                client = self.client,
                debug_enabled = self.debug_enabled,
                on_error = self.on_error,
                ignore_errors = self.ignore_errors,
                timeout = self.timeout,
                max_retries = self.max_retries,
                settings = self.settings,
                _get_headers = self.oidc.get_headers,
                _async_get_headers = self.oidc.async_get_headers,
                **self.kwargs
            ))
    
