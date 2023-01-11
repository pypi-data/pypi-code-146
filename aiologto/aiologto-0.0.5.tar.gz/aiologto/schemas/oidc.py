import time
import aiohttpx
from typing import Optional, Type, Dict, Union
from aiokeydb import KeyDBClient
from jose.exceptions import JWTError

from aiologto.types.base import BaseRoute, Field, BaseResource, lazyproperty
from aiologto.types.oidc import Jwks, TokenResponse
from aiologto.utils.config import LogtoSettings
from aiologto.utils.logs import logger
from aiologto.utils.caching import NO_CACHE, cache_invalidator

__all__ = [
    'Token',
    'OidcAuthorization',
    'TokenResponse',
    'Jwks',
    'OidcRoute',
]

class Token(BaseResource):
    access_token: Optional[str]
    expires_in: Optional[int]
    id_token: Optional[str]
    refresh_token: Optional[str]
    scope: Optional[str]
    token_type: Optional[str]

class OidcAuthorization(BaseResource):
    access_token: Optional[str]
    expires_in: Optional[int]
    token_type: Optional[str]

    issued_at: Optional[int] = Field(default_factory = time.time)

    @lazyproperty
    def headers(self):
        return {
            'Authorization': f'{self.token_type} {self.access_token}',
        }
    
    @property
    def is_expired(self):
        """
        Checks whether the token has expired with a 90.0s buffer
        """
        return self.expires_in is not None \
            and time.time()> (self.issued_at + self.expires_in + 90.0)


class OidcRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = Token
    response_model: Optional[Type[BaseResource]] = TokenResponse
    usage_model: Optional[Type[BaseResource]] = None
    settings: Optional[LogtoSettings] = None
    authorization: Optional[OidcAuthorization] = None
    jwks: Optional[Jwks] = None

    @lazyproperty
    def api_resource(self):
        return 'oidc'

    @lazyproperty
    def methods_enabled(self):
        return []

    @KeyDBClient.cachify(cache_ttl=3600*24, _no_cache=NO_CACHE, _cache_invalidator=cache_invalidator)
    def get_jwks(self, **kwargs) -> Union[Dict, str]:
        """
        Fetches the JWT from the OIDC serer
        """
        api_response = self._send("GET", url=f"{self.api_resource}/jwks")
        data = self.handle_response(api_response)
        return data.json()

    @KeyDBClient.cachify(cache_ttl=3600*24, _no_cache=NO_CACHE, _cache_invalidator=cache_invalidator)
    async def async_get_jwks(self, **kwargs) -> Union[Dict, str]:
        """
        Fetches the JWT from the OIDC serer
        """
        api_response = await self._async_send(
            "GET",
            url = f"{self.api_resource}/jwks"
        )
        data = self.handle_response(api_response)
        return data.json()

    def decode_token(
        self,
        token: str,
        key: Optional[Union[Dict, str]] = None,
        algorithms: Optional[str] = None,
        audience: Optional[str] = None,
        issuer: Optional[str] = None,
        options: Optional[Dict] = None,
        overwrite: Optional[bool] = None,
        **kwargs,
    ):
        """
        Decodes the token using JWT
        """
        if self.jwks is None or overwrite:
            key = key if key is not None else self.get_jwks()
            algorithms = algorithms if algorithms is not None else self.settings.jwt_algorithms
            audience = audience if audience is not None else self.settings.resource
            issuer = self.settings.get_jwt_issuer(issuer=issuer)
            options = options if options is not None else self.settings.jwt_options

            self.jwks = Jwks(
                key=key,
                algorithms=algorithms,
                audience=audience,
                issuer=issuer,
                options=options,
            )
            # Configure the settings
            # so that it's accessible by other APIs
            self.settings.configure(jwks=self.jwks)

        try:
            return self.jwks.decode_token(token)
        except JWTError:
            self.jwks.key = self.get_jwks(invalidate_local_cache=True)
            return self.jwks.decode_token(token)

    async def async_decode_token(
        self,
        token: str,
        key: Optional[Union[Dict, str]] = None,
        algorithms: Optional[str] = None,
        audience: Optional[str] = None,
        issuer: Optional[str] = None,
        options: Optional[Dict] = None,
        overwrite: Optional[bool] = None,
        **kwargs,
    ) -> TokenResponse:
        """
        Decodes the token using JWT
        """
        if self.jwks is None or overwrite:
            key = key if key is not None else await self.async_get_jwks()
            algorithms = algorithms if algorithms is not None else self.settings.jwt_algorithms
            audience = audience if audience is not None else self.settings.resource
            issuer = self.settings.get_jwt_issuer(issuer=issuer)
            options = options if options is not None else self.settings.jwt_options
            self.jwks = Jwks(
                key=key,
                algorithms=algorithms,
                audience=audience,
                issuer=issuer,
                options=options,
            )
            # Configure the settings
            # so that it's accessible by other APIs
            self.settings.configure(jwks=self.jwks)

        try:
            return self.jwks.decode_token(token)
        except JWTError:
            self.jwks.key = await self.async_get_jwks(invalidate_local_cache=True)
            return self.jwks.decode_token(token)
    
    def get_headers(
        self,
        headers: Optional[Dict] = None,
        **kwargs,
    ):
        """
        Fetches the headers with auth, checking
        for expired token
        """
        if self.authorization is None or self.authorization.is_expired:
            self.configure(**kwargs)
        _headers = self.settings.get_headers(**kwargs)
        if headers: _headers.update(headers)
        return _headers
    
    async def async_get_headers(
        self,
        headers: Optional[Dict] = None,
        **kwargs,
        ) -> Dict:
        """
        Fetches the headers with auth, checking
        for expired token
        """
        if self.authorization is None or self.authorization.is_expired:
            await self.async_configure(**kwargs)
        _headers = self.settings.get_headers(**kwargs)
        if headers: _headers.update(headers)
        return _headers

    def configure(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        grant_type: Optional[str] = None,
        resource: Optional[str] = None,
        refresh: Optional[bool] = False,
        configure: Optional[bool] = True,
        **kwargs,
    ):
        """
        Configure the OIDC

        Args:
            app_id: The application id
            app_secret: The application secret
            grant_type: The grant type
            resource: The resource
            configure: Whether to configure the token in global settings
            **kwargs: Additional arguments
        """
        if (self.authorization is not None and not self.authorization.is_expired) and not refresh:
            return self.authorization
        
        app_id = app_id if app_id is not None else self.settings.app_id
        app_secret = app_secret if app_secret is not None else self.settings.app_secret
        grant_type = grant_type if grant_type is not None else self.settings.oidc_grant_type
        resource = resource if resource is not None else self.settings.resource

        if self.debug_enabled:
            logger.info(f'Fetching Authorization for app_id: {app_id}, grant: {grant_type}, resource: {resource}')
        
        api_response = self._send(
            method = "POST",
            url = f"{self.api_resource}/token",
            data = {
                "grant_type": grant_type,
                "resource": resource,
            },
            auth = aiohttpx.BasicAuth(app_id, app_secret) if (app_id and app_secret) else None,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        self.authorization = OidcAuthorization.parse_obj(data.json())
        if configure:
            if self.debug_enabled:
                logger.info(f'Configuring Authorization with token: {self.authorization.access_token}')
            self.settings.configure(
                app_id = app_id,
                app_secret = app_secret,
                oidc_grant_type = grant_type,
                resource = resource,
                access_token = self.authorization.access_token,
                token_type = self.authorization.token_type
            )


    async def async_configure(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        grant_type: Optional[str] = None,
        resource: Optional[str] = None,
        refresh: Optional[bool] = False,
        configure: Optional[bool] = True,
        **kwargs,
    ): 
        """
        Configure the OIDC

        Args:
            app_id: The application id
            app_secret: The application secret
            grant_type: The grant type
            resource: The resource
            refresh: Whether to refresh the token
            configure: Whether to configure the token in global settings
            **kwargs: Additional arguments
        """
        if (self.authorization is not None and not self.authorization.is_expired) and not refresh:
            return self.authorization
        
        app_id = app_id if app_id is not None else self.settings.app_id
        app_secret = app_secret if app_secret is not None else self.settings.app_secret
        grant_type = grant_type if grant_type is not None else self.settings.oidc_grant_type
        resource = resource if resource is not None else self.settings.resource

        if self.debug_enabled:
            logger.info(f'Fetching Authorization for app_id: {app_id}, grant: {grant_type}, resource: {resource}')
        
        api_response = await self._async_send(
            method = "POST",
            url = f"{self.api_resource}/token",
            data = {
                "grant_type": grant_type,
                "resource": resource,
            },
            auth = aiohttpx.BasicAuth(app_id, app_secret) if (app_id and app_secret) else None,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        self.authorization = OidcAuthorization.parse_obj(data.json())
        if configure:
            if self.debug_enabled:
                logger.info(f'Configuring Authorization with token: {self.authorization.access_token}')
            self.settings.configure(
                app_id = app_id,
                app_secret = app_secret,
                oidc_grant_type = grant_type,
                resource = resource,
                access_token = self.authorization.access_token,
                token_type = self.authorization.token_type
            )
        return self.authorization



