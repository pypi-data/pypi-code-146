import json
import aiohttpx
import backoff

from lazyops.types import BaseModel, lazyproperty, Field
from lazyops.utils import ObjectEncoder, Json
from lazyops.types.formatting import to_camel_case
from aiologto.utils.logs import logger

from aiologto.utils.config import LogtoSettings
from aiologto.utils.config import settings as logto_settings

from aiologto.types.errors import APIError, fatal_exception
from typing import Dict, Optional, Any, List, Type, Callable, Coroutine, Union, Tuple

__all__ = [
    'BaseRoute',
    'BaseResource',
    'RESPONSE_SUCCESS_CODES',
]

RESPONSE_SUCCESS_CODES = [
    200, 
    201, 
    202, 
    204
]

VALID_SEND_KWARGS = [
    'method',
    'url',
    'content',
    'data',
    'files',
    'json',
    'params',
    'headers',
    'cookies',
    'auth',
    'follow_redirects',
    'timeout',
    'extensions',
]


class BaseResource(BaseModel):

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True
        alias_generator = to_camel_case
        json_dumps = Json.dumps

    @lazyproperty
    def resource_id(self):
        if hasattr(self, 'logto_id'):
            return self.logto_id
        return self.id if hasattr(self, 'id') else None
    
    @staticmethod
    def create_resource(
        resource: Type['BaseResource'],
        **kwargs
    ) -> Tuple[Type['BaseResource'], Dict]:
        """
        Extracts the resource from the kwargs and returns the resource 
        and the remaining kwargs
        """
        resource_fields = [field.name for field in resource.__fields__.values()]
        resource_kwargs = {k: v for k, v in kwargs.items() if k in resource_fields}
        return_kwargs = {k: v for k, v in kwargs.items() if k not in resource_fields and k in VALID_SEND_KWARGS}
        resource_obj = resource.parse_obj(resource_kwargs)
        if logto_settings.debug_enabled: logger.info(f'Created Resource: {resource_obj} | {return_kwargs}')
        return resource_obj, return_kwargs
    
    def update_dict(
        self,
        *,
        by_alias: bool = False,
        exclude_none: bool = False,
        **kwargs
    ):
        return super().dict(
            by_alias = by_alias,
            exclude_none = exclude_none,
            **kwargs
        )
        

class BaseRoute(BaseModel):
    client: aiohttpx.Client
    success_codes: Optional[List[int]] = RESPONSE_SUCCESS_CODES
    input_model: Optional[Type[BaseResource]] = None
    response_model: Optional[Type[BaseResource]] = None
    patch_model: Optional[Type[BaseResource]] = None

    usage_model: Optional[Type[BaseResource]] = None

    settings: Optional[LogtoSettings] = logto_settings

    # Options
    timeout: Optional[int] = None
    debug_enabled: Optional[bool] = False
    on_error: Optional[Callable] = None
    ignore_errors: Optional[bool] = False

    _get_headers: Optional[Callable] = None
    _async_get_headers: Optional[Coroutine] = None

    @lazyproperty
    def api_resource(self):
        return ''

    @lazyproperty
    def root_name(self):
        return ''
    
    @lazyproperty
    def methods_enabled(self):
        return ['get', 'list', 'create', 'update', 'delete', 'upsert', 'exists']
    
    def get_headers(self, headers: Optional[Dict] = None, **kwargs):
        """
        Fetches the headers with auth
        """
        return self._get_headers(headers = headers, **kwargs) if self._get_headers is not None else self.settings.get_headers(**kwargs)


    async def async_get_headers(self, headers: Optional[Dict] = None, **kwargs):
        """
        Fetches the headers with auth
        """
        return await self._async_get_headers(headers = headers, **kwargs) if self._async_get_headers is not None else self.settings.get_headers(**kwargs)
    
    def get(
        self, 
        resource_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Type[BaseResource]:
        """
        GET a Single Resource

        :param resource_id: The ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        """
        if 'get' not in self.methods_enabled:
            raise NotImplementedError(f'GET is not allowed for {self.api_resource}')
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{resource_id}'
        api_response = self._send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)


    async def async_get(
        self, 
        resource_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> Type[BaseResource]:
        """
        GET a Single Resource

        :param resource_id: The ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        """
        if 'get' not in self.methods_enabled:
            raise NotImplementedError(f'GET is not allowed for {self.api_resource}')
        
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{resource_id}'
        api_response = await self._async_send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)

    def list(
        self, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Union[List[Type[BaseResource]], Dict[str, Any]]]:
        """
        GET all available objects of Resource

        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        
        :return: Dict[str, Union[List[Type[BaseResource]], Dict[str, Any]]]
        """
        if 'list' not in self.methods_enabled:
            raise NotImplementedError(f'LIST is not allowed for {self.api_resource}')

        headers = self.get_headers(headers = headers, **kwargs)
        api_response = self._send(
            method = 'GET',
            url = self.api_resource,
            params = params,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)

    async def async_list(
        self, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Dict[str, Union[List[Type[BaseResource]], Dict[str, Any]]]:
        """
        GET all available objects of Resource

        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: Dict[str, Union[List[Type[BaseResource]], Dict[str, Any]]]
        """
        if 'list' not in self.methods_enabled:
            raise NotImplementedError(f'LIST is not allowed for {self.api_resource}')

        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_response = await self._async_send(
            method = 'GET',
            url = self.api_resource,
            params = params,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)

    def delete(
        self, 
        resource_id: str,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        DELETE a Resource

        :param resource_id: The ID of the Resource to DELETE
        """
        if 'delete' not in self.methods_enabled:
            raise NotImplementedError(f'DELETE is not allowed for {self.api_resource}')

        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{resource_id}'
        api_response = self._send(
            method = 'DELETE',
            url = api_resource,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return data is None
    
    async def async_delete(
        self, 
        resource_id: str,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        DELETE a Resource

        :param resource_id: The ID of the Resource to DELETE
        """
        if 'delete' not in self.methods_enabled:
            raise NotImplementedError(f'DELETE is not allowed for {self.api_resource}')

        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{resource_id}'
        api_response = await self._async_send(
            method = 'DELETE',
            url = api_resource,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return data is None

    def create(
        self, 
        input_object: Optional[Type[BaseResource]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Create a Resource

        :param input_object: Input Object to Create
        """
        if 'create' not in self.methods_enabled:
            raise NotImplementedError(f'CREATE is not allowed for {self.api_resource}')

        if input_object is None:
            input_object, kwargs = self.input_model.create_resource(
                resource = self.input_model,
                **kwargs
            )

        headers = self.get_headers(headers = headers, **kwargs)
        data = json.dumps(input_object.dict(exclude_none=True), cls = ObjectEncoder)
        api_response = self._send(
            method = 'POST',
            url = self.api_resource,
            data = data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return True if data is None else self.prepare_response(data.json())
    
    async def async_create(
        self, 
        input_object: Optional[Type[BaseResource]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Create a Resource

        :param input_object: Input Object to Create
        """
        if 'create' not in self.methods_enabled:
            raise NotImplementedError(f'CREATE is not allowed for {self.api_resource}')

        if input_object is None:
            input_object, kwargs = self.input_model.create_resource(
                resource = self.input_model,
                **kwargs
            )

        headers = await self.async_get_headers(headers = headers, **kwargs)
        data = json.dumps(input_object.dict(exclude_none=True), cls = ObjectEncoder)
        api_response = await self._async_send(
            method = 'POST',
            url = self.api_resource,
            data = data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return True if data is None else self.prepare_response(data.json())

    def update(
        self, 
        input_object: Optional[Type[BaseResource]] = None,
        resource_id: str = None,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a Resource

        :param input_object: Input Object to Update
        :param resource_id: The ID of the Resource to Update
        """
        if 'update' not in self.methods_enabled:
            raise NotImplementedError(f'UPDATE is not allowed for {self.api_resource}')

        patch_model = self.patch_model or self.input_model
        if input_object is None:
            input_object, kwargs = patch_model.create_resource(
                resource = patch_model,
                **kwargs
            )
        else:
            resource_id = input_object.resource_id
            input_object, kwargs = patch_model.create_resource(
                resource = patch_model,
                **(
                    input_object.update_dict() if hasattr(input_object, 'update_dict') \
                        else input_object.dict(by_alias = False)
                )
            )
        
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = self.api_resource
        resource_id = resource_id or input_object.resource_id

        if resource_id is not None:
            api_resource = f'{api_resource}/{resource_id}'

        data = json.dumps(input_object.dict(exclude_none = True), cls = ObjectEncoder)
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            data = data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())

    async def async_update(
        self, 
        input_object: Optional[Type[BaseResource]] = None,
        resource_id: str = None,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a Resource

        :param input_object: Input Object to Update
        :param resource_id: The ID of the Resource to Update
        """
        if 'update' not in self.methods_enabled:
            raise NotImplementedError(f'UPDATE is not allowed for {self.api_resource}')

        patch_model = self.patch_model or self.input_model
        if input_object is None:
            input_object, kwargs = patch_model.create_resource(
                resource = patch_model,
                **kwargs
            )
        else:
            resource_id = input_object.resource_id
            input_object, kwargs = patch_model.create_resource(
                resource = patch_model,
                **(
                    input_object.update_dict() if hasattr(input_object, 'update_dict') \
                        else input_object.dict(by_alias = False)
                )
            )
        
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = self.api_resource
        resource_id = resource_id or input_object.resource_id

        if resource_id is not None:
            api_resource = f'{api_resource}/{resource_id}'
        
        data = json.dumps(input_object.dict(exclude_none = True), cls = ObjectEncoder)
        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            data = data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())
    
    """
    Extra Methods
    """

    def exists(
        self,
        resource_id: str,
        **kwargs
    ) -> bool:
        """
        See whether a Resource Exists

        :param resource_id: The ID of the Resource to Valid
        """
        if 'exists' not in self.methods_enabled:
            raise NotImplementedError(f'EXISTS is not allowed for {self.api_resource}')

        try:
            return self.get(resource_id = resource_id, **kwargs)
        except Exception:
            return False
    
    async def async_exists(
        self,
        resource_id: str,
        **kwargs
    ) -> bool:
        """
        See whether a Resource Exists

        :param resource_id: The ID of the Resource to Valid
        """
        if 'exists' not in self.methods_enabled:
            raise NotImplementedError(f'EXISTS is not allowed for {self.api_resource}')

        try:
            return await self.async_get(resource_id = resource_id, **kwargs)
        except Exception:
            return False
    
    def upsert(
        self,
        resource_id: str,
        input_object: Optional[Type[BaseResource]] = None,
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

        :resource_id: The ID of the Resource to Upsert
        :param input_object: Input Object to Upsert
        :param update_existing (bool): Whether to update the Resource if it exists
        :overwrite_existing (bool): Whether to overwrite the Resource if it exists
        """
        if 'upsert' not in self.methods_enabled:
            raise NotImplementedError(f'UPSERT is not allowed for {self.api_resource}')

        resource = self.exists(resource_id = resource_id, **kwargs)
        if resource is not None:
            if update_existing:
                return self.update(input_object = input_object, identifier = resource_id, **kwargs)
            if overwrite_existing:
                self.delete(resource_id = resource_id, **kwargs)
                return self.create(input_object = input_object, **kwargs)
            return resource
        return self.create(input_object = input_object, **kwargs)
    
    async def async_upsert(
        self,
        resource_id: str,
        input_object: Optional[Type[BaseResource]] = None,
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

        :resource_id: The ID of the Resource to Upsert
        :param input_object: Input Object to Upsert
        :param update_existing (bool): Whether to update the Resource if it exists
        :overwrite_existing (bool): Whether to overwrite the Resource if it exists
        """
        if 'upsert' not in self.methods_enabled:
            raise NotImplementedError(f'UPSERT is not allowed for {self.api_resource}')

        resource = await self.async_exists(resource_id = resource_id, **kwargs)
        if resource is not None:
            if update_existing:
                return self.async_update(input_object = input_object, identifier = resource_id, **kwargs)
            if overwrite_existing:
                await self.async_delete(resource_id = resource_id, **kwargs)
                return await self.async_create(input_object = input_object, **kwargs)
            return resource
        return await self.async_create(input_object = input_object, **kwargs)


    def prepare_response(
        self, 
        data: Union[Dict, List],
        response_object: Optional[Type[BaseResource]] = None,
        **kwargs
    ):
        """
        Prepare the Response Object
        
        :param data: The Response Data
        :param response_object: The Response Object
        """
        response_object = response_object or self.response_model
        if response_object:
            if isinstance(data, list):
                return response_object.create_many(data)
            return response_object.parse_obj(data)
        raise NotImplementedError('Response model not defined for this resource.')

    def handle_response(
        self, 
        response: aiohttpx.Response,
        **kwargs
    ):
        """
        Handle the Response

        :param response: The Response
        """
        if self.debug_enabled:
            logger.info(f'[{response.status_code} - {response.request.url}] headers: {response.headers}, body: {response.text}')
        
        if response.status_code in self.success_codes:
            return response if response.text else None
        
        if self.ignore_errors:
            return None
        
        raise APIError(
            url = response.request.url,
            status = response.status_code,
            payload = response.text
        )

    def _send(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = None,
        **kwargs
    ) -> aiohttpx.Response:
        if retries is None: retries = self.settings.max_retries
        if timeout is None: timeout = self.timeout
        @backoff.on_exception(
            backoff.expo, Exception, max_tries = retries + 1, giveup = fatal_exception
        )
        def _retryable_send():
            return self.client.request(
                method = method,
                url = url,
                params = params,
                data = data,
                headers = headers,
                timeout = timeout,
                **kwargs
            )
        return _retryable_send()
    
    async def _async_send(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = None,
        **kwargs
    ) -> aiohttpx.Response:
        if retries is None: retries = self.settings.max_retries
        if timeout is None: timeout = self.timeout
        @backoff.on_exception(
            backoff.expo, Exception, max_tries = retries + 1, giveup = fatal_exception
        )
        async def _retryable_async_send():
            return await self.client.async_request(
                method = method,
                url = url,
                params = params,
                data = data,
                headers = headers,
                timeout = timeout,
                **kwargs
            )
        return await _retryable_async_send()




