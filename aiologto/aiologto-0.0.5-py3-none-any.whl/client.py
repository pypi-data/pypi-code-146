import aiohttpx
from typing import Optional, Callable, Dict

from lazyops.types import lazyproperty
from aiologto.schemas import *
from aiologto.types.errors import LogtoApiError

from aiologto.utils.logs import logger
from aiologto.utils.config import LogtoSettings
from aiologto.utils.config import settings as logto_settings
from aiologto.routes import ApiRoutes


class LogtoClient:
    """
    Main Client for all the routes in the API.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        api_path: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        resource: Optional[str] = None,
        oidc_grant_type: Optional[str] = None,

        access_token: Optional[str] = None,
        token_type: Optional[str] = None,

        jwt_algorithms: Optional[str] = None,
        jwt_options: Optional[Dict] = None,
        jwt_issuer: Optional[str] = None,
        on_error: Optional[Callable] = None,
        ignore_errors: Optional[bool] = None,
        debug_enabled: Optional[bool] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        settings: Optional[LogtoSettings] = None,
        **kwargs,
    ):
        """
        :param url: The URL of the API.
        :param scheme: The scheme of the API.
        :param host: The host of the API.
        :param port: The port of the API.
        :param api_path: The path of the API.
        :param app_id: The ID of the application.
        :param app_secret: The secret of the application.
        :param resource: The resource of the application.
        :param oidc_grant_type: The OIDC grant type.
        :param access_token: The access token.
        :param token_type: The token type.

        :param jwt_algorithms: The JWT algorithms.
        :param jwt_options: The JWT options.
        :param jwt_issuer: The JWT issuer.
        :param ignore_errors: Whether to ignore errors.
        :param debug_enabled: Whether to enable debug mode.
        :param timeout: The timeout.
        :param max_retries: The max retries.
        """
        self.settings = settings if settings is not None else logto_settings

        self.api_url = settings.get_api_url(host = host, port = port, scheme = scheme, url = url)
        self.base_url = settings.get_base_api_url(host = host, port = port, scheme = scheme, url = url, api_path = api_path)


        self.app_id = app_id if app_id is not None else self.settings.app_id
        self.app_secret = app_secret if app_secret is not None else self.settings.app_secret
        self.resource = resource if resource is not None else self.settings.resource
        self.oidc_grant_type = oidc_grant_type if oidc_grant_type is not None else self.settings.oidc_grant_type
        self.access_token = access_token if access_token is not None else self.settings.access_token
        self.token_type = token_type if token_type is not None else self.settings.token_type
        self.jwt_algorithms = jwt_algorithms if jwt_algorithms is not None else self.settings.jwt_algorithms
        self.jwt_options = jwt_options if jwt_options is not None else self.settings.jwt_options
        self.jwt_issuer = jwt_issuer if jwt_issuer is not None else self.settings.jwt_issuer

        self.on_error = on_error
        self.ignore_errors = ignore_errors if ignore_errors is not None else self.settings.ignore_errors
        self.debug_enabled = debug_enabled if debug_enabled is not None else self.settings.debug_enabled
        self.timeout = timeout if timeout is not None else self.settings.timeout
        self.max_retries = max_retries if max_retries is not None else self.settings.max_retries

        self._kwargs = kwargs
        self.log_method = logger.info if self.debug_enabled else logger.debug
        self.client = aiohttpx.Client(
            base_url = self.base_url,
            timeout = self.timeout,
        )
        self.routes = ApiRoutes(
            client = self.client,
            debug_enabled = self.debug_enabled,
            on_error = self.on_error,
            ignore_errors = self.ignore_errors,
            timeout = self.timeout,
            max_retries = self.max_retries,
            settings = self.settings,
            **self._kwargs
        )
        logger.info(f"Logto Client initialized: {self.client.base_url}")
        if self.debug_enabled:
            logger.debug(f"Debug Enabled: {self.debug_enabled}")


    @lazyproperty
    def oidc(self) -> OidcRoute:
        """
        Returns the `OidcRoute` class for interacting with `Authorization`.
        """
        return self.routes.oidc
    
    @lazyproperty
    def users(self) -> UserRoute:
        """
        Returns the `UserRoute` class for interacting with `Users`.
        
        Doc: `https://docs.logto.io/api/#tag/Users`
        """
        return self.routes.users
    
    """
    Functions
    """

    def verify_user(
        self,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        ignore_errors: Optional[bool] = False,
        **kwargs
    ) -> Optional[UserResponse]:
        """
        Verify a user.

        :param user_id: The user ID.
        :param token: The JWT token.
        :param ignore_errors: Whether to ignore errors.
        :param kwargs: Additional arguments to pass to the route.
        :return: The user or `None` if `ignore_errors` is True
        """

        assert user_id or token, "Either user_id or token must be passed."
        if token:
            token_obj = self.oidc.decode_token(
                token = token, 
                **kwargs
            )
            user_id = token_obj.user_id
        user = self.users.exists(
            resource_id = user_id,
            **kwargs
        )
        if user or ignore_errors: return user
        raise LogtoApiError(f"User with ID '{user_id}' not found.")

    async def async_verify_user(
        self,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        ignore_errors: Optional[bool] = False,
        **kwargs
    ) -> Optional[UserResponse]:
        """
        Verify a user.

        :param user_id: The user ID.
        :param token: The JWT token.
        :param ignore_errors: Whether to ignore errors.
        :param kwargs: Additional arguments to pass to the route.
        :return: The user or `None` if `ignore_errors` is True
        """
        assert user_id or token, "Either user_id or token must be passed."
        if token:
            token_obj = await self.oidc.async_decode_token(
                token = token, 
                **kwargs
            )
            user_id = token_obj.user_id
        user = await self.users.async_exists(
            resource_id = user_id,
            **kwargs
        )
        if user or ignore_errors: return user
        raise LogtoApiError(f"User with ID '{user_id}' not found.")


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

class LogtoAPI:
    settings: Optional[LogtoSettings] = logto_settings
    _api: Optional[LogtoClient] = None

    """
    The Global Class for Logto API.
    """

    def configure(
        self, 
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        api_path: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        resource: Optional[str] = None,
        oidc_grant_type: Optional[str] = None,

        access_token: Optional[str] = None,
        token_type: Optional[str] = None,

        jwks: Optional['Jwks'] = None,
        jwt_algorithms: Optional[str] = None,
        jwt_options: Optional[Dict] = None,
        jwt_issuer: Optional[str] = None,

        ignore_errors: Optional[bool] = None,
        debug_enabled: Optional[bool] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,

        reset: Optional[bool] = None,
        **kwargs
    ):
        """
        Configure the global Logto client.

        :param url: The URL of the API.
        :param scheme: The scheme of the API.
        :param host: The host of the API.
        :param port: The port of the API.
        :param api_path: The path of the API.
        :param app_id: The ID of the application.
        :param app_secret: The secret of the application.
        :param resource: The resource of the application.
        :param oidc_grant_type: The OIDC grant type.
        :param access_token: The access token.
        :param token_type: The token type.

        :param jwt_algorithms: The JWT algorithms.
        :param jwt_options: The JWT options.
        :param jwt_issuer: The JWT issuer.
        :param ignore_errors: Whether to ignore errors.
        :param debug_enabled: Whether to enable debug mode.
        :param timeout: The timeout.
        :param max_retries: The max retries.
        :param reset: Whether to reset the session.

        """
        self.settings.configure(
            url=url,
            scheme=scheme,
            host=host,
            port=port,
            api_path=api_path,
            app_id=app_id,
            app_secret=app_secret,
            resource=resource,
            oidc_grant_type=oidc_grant_type,
            access_token=access_token,
            token_type=token_type,
            jwks=jwks,
            jwt_algorithms=jwt_algorithms,
            jwt_options=jwt_options,
            jwt_issuer=jwt_issuer,
            ignore_errors=ignore_errors,
            debug_enabled=debug_enabled,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )
        if reset: self._api = None
        if self._api is None:
            self.get_api(**kwargs)
    
    def get_api(self, **kwargs) -> LogtoClient:
        if self._api is None:
            self._api = LogtoClient(
                settings = self.settings,
                **kwargs
            )
        return self._api
    
    @property
    def api(self) -> LogtoClient:
        """
        Returns the inherited Logto client.
        """
        if self._api is None:
            self.configure()
        return self._api

    """
    API Routes
    """

    @lazyproperty
    def oidc(self) -> OidcRoute:
        """
        Returns the `OidcRoute` class for interacting with `Authorization`.
        """
        return self.api.oidc
    
    @lazyproperty
    def users(self) -> UserRoute:
        """
        Returns the `UserRoute` class for interacting with `Users`.
        
        Doc: `https://docs.logto.io/api/#tag/Users`
        """
        return self.api.users
    
    """
    Functions
    """
    def verify_user(
        self,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        ignore_errors: Optional[bool] = False,
        **kwargs
    ) -> Optional[UserResponse]:
        """
        Verify a user.

        :param user_id: The user ID.
        :param token: The JWT token.
        :param ignore_errors: Whether to ignore errors.
        :param kwargs: Additional arguments to pass to the route.
        :return: The user or `None` if `ignore_errors` is True
        """
        return self.api.verify_user(
            token=token,
            user_id=user_id,
            ignore_errors=ignore_errors,
            **kwargs
        )
    
    async def async_verify_user(
        self,
        token: Optional[str] = None,
        user_id: Optional[str] = None,
        ignore_errors: Optional[bool] = False,
        **kwargs
    ) -> Optional[UserResponse]:
        """
        Verify a user.

        :param user_id: The user ID.
        :param token: The JWT token.
        :param ignore_errors: Whether to ignore errors.
        :param kwargs: Additional arguments to pass to the route.
        :return: The user or `None` if `ignore_errors` is True
        """
        return await self.api.async_verify_user(
            token=token,
            user_id=user_id,
            ignore_errors=ignore_errors,
            **kwargs
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


    
Logto: LogtoAPI = LogtoAPI()







