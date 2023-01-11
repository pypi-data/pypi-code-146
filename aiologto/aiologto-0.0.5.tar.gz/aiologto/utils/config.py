from typing import Optional, Dict
from lazyops.types import BaseSettings, lazyproperty
from aiologto.version import VERSION
from aiologto.types.oidc import Jwks

class LogtoSettings(BaseSettings):

    url: Optional[str] = None
    scheme: Optional[str] = 'http://'
    host: Optional[str] = None
    port: Optional[int] = 3001

    api_path: Optional[str] = None

    app_id: Optional[str] = None
    app_secret: Optional[str] = None

    resource: Optional[str] = "https://api.logto.io"
    oidc_grant_type: Optional[str] = "client_credentials"

    # Handle this at the `oidc` level
    # authorization: Optional[str] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = "Bearer"
    
    # jwks: Optional[Union[Dict, str]] = None
    jwks: Optional[Jwks] = None # maybe

    jwt_algorithms: Optional[str] = None
    jwt_options: Optional[Dict] = {"verify_at_hash": False}
    jwt_issuer: Optional[str] = None
    
    ignore_errors: Optional[bool] = False
    debug_enabled: Optional[bool] = True

    timeout: Optional[int] = 10
    max_retries: Optional[int] = 3
    
    class Config:
        env_prefix = 'LOGTO_'
        case_sensitive = False

    def get_jwt_issuer(
        self,
        issuer: Optional[str] = None,
        **kwargs,
    ):  
        """
        Returns the JWT issuer
        """
        return issuer if issuer is not None else \
            (self.jwt_issuer or f"{self.base_url}/oidc")

    @lazyproperty
    def api_url(self) -> str:
        if self.url:
            return self.url
        if self.host:
            url = f"{self.scheme}{self.host}"
            if self.port: url += f":{self.port}"
            return url
        
        # Return the official Logto API URL
        return "https://api.logto.io"
    
    @lazyproperty
    def base_url(self) -> str:
        if self.api_path:
            from urllib.parse import urljoin
            return urljoin(self.api_url, self.api_path)
        return self.api_url
    
    @property
    def headers(self):
        _headers = {"Content-Type": "application/json", "User-Agent": f"aiologto/{VERSION}"}
        if self.access_token: 
            _headers['Authorization'] = f'{self.token_type} {self.access_token}'
        return _headers


    def get_headers(
        self, 
        access_token: Optional[str] = None, 
        token_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, str]:

        headers = self.headers.copy()
        if kwargs: headers.update(**kwargs)
        access_token = access_token if access_token is not None else self.access_token
        token_type = token_type if token_type is not None else self.token_type
        if access_token: headers['Authorization'] = f'{token_type} {access_token}'
        return headers

    def get_api_url(
        self, 
        host: Optional[str] = None, 
        port: Optional[int] = None, 
        scheme: Optional[str] = None, 
        url: Optional[str] = None,
        **kwargs
    ) -> str:
        if url: return url
        if host:
            url = f"{scheme or self.scheme}{host}"
            if port: url += f":{port}"
            return url
        return self.api_url

    def get_base_api_url(
        self, 
        host: Optional[str] = None, 
        port: Optional[int] = None, 
        scheme: Optional[str] = None, 
        url: Optional[str] = None,
        api_path: Optional[str] = None,
        **kwargs
    ) -> str:
        api_url = self.get_api_url(
            host=host,
            port=port,
            scheme=scheme,
            url=url,
        )
        api_path = api_path or self.api_path
        if api_path:
            from urllib.parse import urljoin
            return urljoin(api_url, api_path)
        return api_url
    
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

        jwks: Optional[Jwks] = None,
        jwt_algorithms: Optional[str] = None,
        jwt_options: Optional[Dict] = None,
        jwt_issuer: Optional[str] = None,

        ignore_errors: Optional[bool] = None,
        debug_enabled: Optional[bool] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        **kwargs,
    ):
        """
        Configure the Logto API client.

        :param url: The Logto API URL.
        :param scheme: The Logto API scheme.
        :param host: The Logto API host.
        :param port: The Logto API port.
        :param api_path: The Logto API path.
        :param app_id: The Logto application ID.
        :param app_secret: The Logto application secret.
        :param resource: The Logto resource.
        :param oidc_grant_type: The Logto OIDC grant type.
        :param access_token: The Logto access token.
        :param token_type: The Logto token type.

        :param jwks: The Logto JWKS.
        :param jwt_algorithms: The Logto JWT algorithms.
        :param jwt_options: The Logto JWT options.
        :param jwt_issuer: The Logto JWT issuer.

        :param ignore_errors: Ignore Logto API errors.
        :param debug_enabled: Enable debug mode.
        :param timeout: Timeout in seconds.
        :param max_retries: Maximum number of retries.
        """
        if url is not None: self.url = url
        if scheme is not None: self.scheme = scheme
        if host is not None: self.host = host
        if port is not None: self.port = port
        if api_path is not None: self.api_path = api_path
        if app_id is not None: self.app_id = app_id
        if app_secret is not None: self.app_secret = app_secret
        if resource is not None: self.resource = resource
        if oidc_grant_type is not None: self.oidc_grant_type = oidc_grant_type
        if access_token is not None: self.access_token = access_token
        if token_type is not None: self.token_type = token_type

        if jwks is not None: self.jwks = jwks
        if jwt_algorithms is not None: self.jwt_algorithms = jwt_algorithms
        if jwt_options is not None: self.jwt_options = jwt_options
        if jwt_issuer is not None: self.jwt_issuer = jwt_issuer

        if ignore_errors is not None: self.ignore_errors = ignore_errors
        if debug_enabled is not None: self.debug_enabled = debug_enabled
        if timeout is not None: self.timeout = timeout
        if max_retries is not None: self.max_retries = max_retries
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)



settings = LogtoSettings()