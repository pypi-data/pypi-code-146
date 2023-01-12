from __future__ import annotations

from tcsoa.gen.Administration._2015_07.UserManagement import CreateOrUpdateUserResponse, CreateOrUpdateUserInputs
from typing import List
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def createOrUpdateUser(cls, userInputs: List[CreateOrUpdateUserInputs]) -> CreateOrUpdateUserResponse:
        """
        This operation creates or updates User objects with given properties. A new User object will be created if it
        does not already exist, otherwise existing User object will be updated. This operation requires system
        administration privilege.
        
        If the Person object given as part of input does not exist it will be created. If it exist the newly created
        User object will point to given Person object.
        
        If not specified in user input, the license level will be author  and user status will be active by default in
        user creation.
        
        License Server and License Bundle on User can be updated by giving license_server and license_bundle as
        property names in userPropertyMap of CreateOrUpdateUserInputs.
        
        
        Use cases:
        Use Case 1: Create User with set of properties.
        Use Case 2: Create User with additional properties.
        Use Case 3: Update existing User&rsquo;s properties.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateUser',
            library='Administration',
            service_date='2015_07',
            service_name='UserManagement',
            params={'userInputs': userInputs},
            response_cls=CreateOrUpdateUserResponse,
        )
