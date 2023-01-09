from typing import Optional, Dict
from lazyops.types import BaseSettings, lazyproperty
from aiolago.version import VERSION



class LagoSettings(BaseSettings):

    url: Optional[str] = None
    scheme: Optional[str] = 'http://'
    host: Optional[str] = None
    port: Optional[int] = 3000
    
    api_key: Optional[str] = None
    api_path: Optional[str] = '/api/v1/'

    api_key_header: Optional[str] = None
    organization_id: Optional[str] = None

    ignore_errors: Optional[bool] = False
    debug_enabled: Optional[bool] = True

    timeout: Optional[int] = 10
    max_retries: Optional[int] = 3
    
    class Config:
        env_prefix = 'LAGO_'
        case_sensitive = False

    @lazyproperty
    def api_url(self) -> str:
        if self.url:
            return self.url
        if self.host:
            url = f"{self.scheme}{self.host}"
            if self.port: url += f":{self.port}"
            return url
        
        # Return the official Lago API URL
        return "https://api.getlago.com"
    
    @lazyproperty
    def base_url(self) -> str:
        if self.api_path:
            from urllib.parse import urljoin
            return urljoin(self.api_url, self.api_path)
        return self.api_url
    
    @lazyproperty
    def headers(self):
        _headers = {"Content-Type": "application/json", "User-Agent": f"aiolago/{VERSION}"}
        if self.api_key: 
            if self.api_key_header:
                _headers[self.api_key_header] = self.api_key
            else:
                _headers['Authorization'] = f'Bearer {self.api_key}'
        return _headers


    def get_headers(
        self, 
        api_key: Optional[str] = None, 
        api_key_header: Optional[str] = None, 
        **kwargs
    ) -> Dict[str, str]:

        headers = self.headers.copy()
        if kwargs: headers.update(**kwargs)
        api_key_header = api_key_header if api_key_header is not None else self.api_key_header
        api_key = api_key if api_key is not None else self.api_key
        if api_key:
            if api_key_header:
                headers[api_key_header] = api_key
            else:
                headers['Authorization'] = f'Bearer {api_key}'
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
        api_key: Optional[str] = None,
        api_path: Optional[str] = None,
        api_key_header: Optional[str] = None,
        organization_id: Optional[str] = None,
        ignore_errors: Optional[bool] = None,
        debug_enabled: Optional[bool] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        **kwargs,
    ):
        """
        Configure the Lago API client.

        :param url: The Lago API URL.
        :param scheme: The Lago API scheme.
        :param host: The Lago API host.
        :param port: The Lago API port.
        :param api_key: The Lago API key.
        :param api_path: The Lago API path.
        :param api_key_header: The Lago API key header.
        :param organization_id: The Lago organization ID.
        :param ignore_errors: Ignore Lago API errors.
        :param debug_enabled: Enable debug mode.
        :param timeout: Timeout in seconds.
        :param max_retries: Maximum number of retries.
        """
        if url is not None: self.url = url
        if scheme is not None: self.scheme = scheme
        if host is not None: self.host = host
        if port is not None: self.port = port
        if api_key is not None: self.api_key = api_key
        if api_path is not None: self.api_path = api_path
        if api_key_header is not None: self.api_key_header = api_key_header
        if organization_id is not None: self.organization_id = organization_id
        if ignore_errors is not None: self.ignore_errors = ignore_errors
        if debug_enabled is not None: self.debug_enabled = debug_enabled
        if timeout is not None: self.timeout = timeout
        if max_retries is not None: self.max_retries = max_retries
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)



settings = LagoSettings()