from __future__ import annotations

from tcsoa.gen.Administration._2016_03.UserManagement import DeleteUsersInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def deleteUser(cls, userInput: List[DeleteUsersInput]) -> ServiceData:
        """
        This operation deletes User objects from Teamcenter. The objects owned by the user can be deleted or keep and
        transfer their ownership to a new user. This operation requires system administration privilege.
        
        Use cases:
        Use Case 1: Delete User with given user id.
        
        Exceptions:
        >ServiceException
        
        10012 - User is not a System Administrator
        """
        return cls.execute_soa_method(
            method_name='deleteUser',
            library='Administration',
            service_date='2016_03',
            service_name='UserManagement',
            params={'userInput': userInput},
            response_cls=ServiceData,
        )
