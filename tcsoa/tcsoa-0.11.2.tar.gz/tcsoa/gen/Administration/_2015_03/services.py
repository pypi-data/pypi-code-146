from __future__ import annotations

from typing import List
from tcsoa.base import TcService
from tcsoa.gen.Administration._2015_03.UserManagement import UserProfileProperties, UserProfilePropertiesResponse


class UserManagementService(TcService):

    @classmethod
    def setUserProfileProperties(cls, userProfileInputs: List[UserProfileProperties]) -> UserProfilePropertiesResponse:
        """
        This operation sets the given properties on the Fnd0CustomUserProfile of the specified User. A new
        Fnd0CustomUserProfile object will be created if it does not already exist and the fnd0custom_user_profile
        property of the User will be set to the newly created Fnd0CustomUserProfile object.
        
        Use cases:
        Use Case 1: Set the properties for a User who does not have a Custom User Profile object.
        Use Case 2: Set the properties for a User who has a Custom User Profile object.
        """
        return cls.execute_soa_method(
            method_name='setUserProfileProperties',
            library='Administration',
            service_date='2015_03',
            service_name='UserManagement',
            params={'userProfileInputs': userProfileInputs},
            response_cls=UserProfilePropertiesResponse,
        )
