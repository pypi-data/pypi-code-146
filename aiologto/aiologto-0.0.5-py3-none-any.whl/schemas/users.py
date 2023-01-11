
import datetime
from enum import Enum
from typing import Optional, Type, List, Dict, Any, Union
from lazyops.types.formatting import to_camel_case
from aiologto.types.base import BaseRoute, BaseResource, lazyproperty, Json


__all__ = [
    'User',
    'UserResponse',
    'UserRoute',
]

# https://docs.logto.io/api/#tag/Users
# Update API Specs to https://docs.logto.io/docs/recipes/interact-with-management-api/advanced-user-search/

class BaseUser(BaseResource):
    primary_email: Optional[str]
    username: Optional[str]
    name: Optional[str]

    def dict(
        self,
        *,
        by_alias: bool = True,
        exclude_none: bool = False,
        **kwargs
    ):
        return super().dict(
            by_alias=by_alias,
            exclude_none=exclude_none,
            **kwargs
        )

class UserSearchMode(str, Enum):
    like = 'like'
    exact = 'exact'
    similiar = 'similiar_to'
    posix = 'posix'

class UserSearchJointMode(str, Enum):
    OR = 'or'
    AND = 'and'


class User(BaseUser):
    password: Optional[str]

class UserUpdate(BaseUser):
    primary_phone: Optional[str]
    avatar: Optional[str]
    custom_data: Optional[Dict]
    role_names: Optional[List]
    identities: Optional[Dict]
    application_id: Optional[str]

class UserResponse(BaseUser):
    id: Optional[str]
    primary_phone: Optional[str]
    avatar: Optional[str]
    custom_data: Optional[Dict]
    role_names: Optional[List]
    identities: Optional[Dict]
    application_id: Optional[str]
    last_sign_in_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]

UserListResponse = Optional[List[UserResponse]]

class UserRoute(BaseRoute):
    input_model: Optional[Type[BaseResource]] = User
    response_model: Optional[Type[BaseResource]] = UserResponse
    patch_model: Optional[Type[BaseResource]] = UserUpdate

    @lazyproperty
    def api_resource(self):
        return 'api/users'
    
    def get(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a Single User

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        return super().get(
            resource_id=user_id,
            params=params,
            headers=headers,
            **kwargs
        )
    
    async def async_get(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a Single User

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        return await super().async_get(
            resource_id=user_id,
            params=params,
            headers=headers,
            **kwargs
        )
    
    def parse_user_search_params(
        self,
        search: Optional[str] = None,
        search_params: Optional[Union[List[Dict[str, str]], Dict[str, str]]] = None,
        mode: Optional[Union[UserSearchMode, Union[List[Dict[str, UserSearchMode]], Dict[str, UserSearchMode]]]] = UserSearchMode.like,
        joint_mode: Optional[UserSearchJointMode] = UserSearchJointMode.OR,
        hide_admin_user: Optional[bool] = None,
        is_case_sensitive: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, str]:
        """
        Helper function to map the parameters for a User Search
        """
        if not params: params = {}
        # Fuzzy search
        if search: params['search'] = search
        # Advanced search
        if search_params:
            if isinstance(search_params, dict):
                for key, value in search_params.items():
                    key = to_camel_case(key)
                    if 'search' not in key: key = f'search.{key}'
                    params[key] = value
            elif isinstance(search_params, list):
                for item in search_params:
                    for key, value in item.items():
                        key = to_camel_case(key)
                        if 'search' not in key: key = f'search.{key}'
                        params[key] = value
        if mode:
            if isinstance(mode, dict):
                for key, value in mode.items():
                    key = to_camel_case(key)
                    if isinstance(value, str): value = UserSearchMode(value)
                    if'mode' not in key: key = f'mode.{key}'
                    params[key] = value.value
            if isinstance(mode, list):
                for item in mode:
                    for key, value in item.items():
                        key = to_camel_case(key)
                        if isinstance(value, str): value = UserSearchMode(value)
                        if 'mode' not in key: key = f'mode.{key}'
                        params[key] = value.value
        
        if joint_mode:
            if isinstance(joint_mode, str): joint_mode = UserSearchJointMode(joint_mode)
            params['joint'] = joint_mode.value

        if hide_admin_user is not None: params['hideAdminUser'] = hide_admin_user
        if is_case_sensitive is not None: params['isCaseSensitive'] = is_case_sensitive
        if page is not None: params['page'] = page
        if page_size is not None: params['pageSize'] = page_size
        return params

    def list(
        self, 
        search: Optional[str] = None,
        search_params: Optional[Union[List[Dict[str, str]], Dict[str, str]]] = None,
        mode: Optional[Union[UserSearchMode, Union[List[Dict[str, UserSearchMode]], Dict[str, UserSearchMode]]]] = None,
        joint_mode: Optional[UserSearchJointMode] = None,
        hide_admin_user: Optional[bool] = None,
        is_case_sensitive: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> UserListResponse:
        """
        Retrieve all Users

        :param search: The search query string
        :param search_params: Optional Query Parameters
        :param mode: The search mode
        :param joint_mode: The joint search mode
        :param hide_admin_user: Whether to hide the Admin User
        :param is_case_sensitive: Whether to search case-sensitive
        :param page: The page number
        :param page_size: The page size

        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        
        :return: UserListResponse
        """
        params = self.parse_user_search_params(
            search=search,
            search_params=search_params,
            mode=mode,
            joint_mode=joint_mode,
            hide_admin_user=hide_admin_user,
            is_case_sensitive=is_case_sensitive,
            page=page,
            page_size=page_size,
            **kwargs
        )
        return super().list(
            params=params,
            headers=headers,
            **kwargs
        )
    
    async def async_list(
        self,
        search: Optional[str] = None,
        search_params: Optional[Union[List[Dict[str, str]], Dict[str, str]]] = None,
        mode: Optional[Union[UserSearchMode, Union[List[Dict[str, UserSearchMode]], Dict[str, UserSearchMode]]]] = None,
        joint_mode: Optional[UserSearchJointMode] = None,
        hide_admin_user: Optional[bool] = None,
        is_case_sensitive: Optional[bool] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> UserListResponse:
        """
        Retrieve all Users

        :param search: The search query string
        :param search_params: Optional Query Parameters
        :param mode: The search mode
        :param joint_mode: The joint search mode
        :param hide_admin_user: Whether to hide the Admin User
        :param is_case_sensitive: Whether to search case-sensitive
        :param page: The page number
        :param page_size: The page size

        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments
        
        :return: UserListResponse
        """
        params = self.parse_user_search_params(
            search=search,
            search_params=search_params,
            mode=mode,
            joint_mode=joint_mode,
            hide_admin_user=hide_admin_user,
            is_case_sensitive=is_case_sensitive,
            page=page,
            page_size=page_size,
            **kwargs
        )
        return await super().async_list(
            params=params,
            headers=headers,
            **kwargs
        )

    def get_user_data(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a User's Custom Data

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
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
    
    async def async_get_user_data(
        self, 
        user_id: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict] = None,
        **kwargs
    )  -> UserResponse:
        """
        GET a User's Custom Data

        :param user_id: The User ID of the Resource to GET
        :param params: Optional Query Parameters
        :param headers: Optional Header Parameters
        :param kwargs: Optional keyword arguments

        :return: UserResponse
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        api_response = await self._async_send(
            method = 'GET',
            url = api_resource, 
            params = params,
            headers = headers,
            **kwargs
        )
        data = self.handle_response(api_response)
        if data: data = data.json()
        return self.prepare_response(data)

    def update_user_data(
        self, 
        user_id: str,
        user_data: Union[Dict, Type[BaseResource]],
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users `customData` dict

        :param user_id: The User ID to Update
        :param user_data: The `customData` dict to update
        """
        
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        if not isinstance(user_data, dict):
            user_data = user_data.dict()
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            json = user_data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())

    async def async_update_user_data(
        self, 
        user_id: str,
        user_data: Union[Dict, Type[BaseResource]],
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users `customData` dict

        :param user_id: The User ID to Update
        :param user_data: The `customData` dict to update
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/custom-data'
        if not isinstance(user_data, dict):
            user_data = user_data.dict()

        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            json = user_data,
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())
    
    def update_user_password(
        self, 
        user_id: str,
        password: str,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users password

        :param user_id: The User ID to Update
        :param password: The new user password
        """
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/password'
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            json = {"password": password},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return data is not None
        # return self.prepare_response(data.json())

    async def async_update_user_password(
        self, 
        user_id: str,
        password: str,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users password

        :param user_id: The User ID to Update
        :param password: The new user password
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/password'
        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            json = {"password": password},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return data is not None
        # return self.prepare_response(data.json())
    
    def update_user_status(
        self, 
        user_id: str,
        suspended: bool,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users's status, which is either suspended or not

        :param user_id: The User ID to Update
        :param suspended: bool
        """
        headers = self.get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/is-suspended'
        api_response = self._send(
            method = 'PATCH',
            url = api_resource,
            json = {"isSuspended": suspended},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())

    async def async_update_user_status(
        self, 
        user_id: str,
        suspended: bool,
        headers: Optional[Dict] = None,
        **kwargs
    ):
        """
        Update a users's status, which is either suspended or not

        :param user_id: The User ID to Update
        :param suspended: bool
        """
        headers = await self.async_get_headers(headers = headers, **kwargs)
        api_resource = f'{self.api_resource}/{user_id}/is-suspended'
        api_response = await self._async_send(
            method = 'PATCH',
            url = api_resource,
            json = {"isSuspended": suspended},
            headers = headers,
            timeout = self.timeout,
            **kwargs
        )
        data = self.handle_response(api_response)
        return self.prepare_response(data.json())
    
    def exists(
        self,
        user_id: str,
        **kwargs
    ) -> bool:
        """
        See whether a User Exists

        :param user_id: The ID of the User to Validate
        """
        if 'exists' not in self.methods_enabled:
            raise NotImplementedError(f'EXISTS is not allowed for {self.api_resource}')

        try:
            return self.get(user_id = user_id, **kwargs)
        except Exception:
            return False
    
    async def async_exists(
        self,
        user_id: str,
        **kwargs
    ) -> bool:
        """
        See whether a User Exists

        :param user_id: The ID of the User to Validate
        """
        if 'exists' not in self.methods_enabled:
            raise NotImplementedError(f'EXISTS is not allowed for {self.api_resource}')

        try:
            return await self.async_get(user_id = user_id, **kwargs)
        except Exception:
            return False