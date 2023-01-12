from __future__ import annotations

from tcsoa.gen.Internal.Administration._2013_05.UserManagement import LicenseStatusResponse, ActivateUserInput
from typing import List
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def activateUsers2(cls, activateUsers: List[ActivateUserInput]) -> LicenseStatusResponse:
        """
        This operation activates user(s) based on the number of allowed active author, consumer, or occasional user
        licenses,  associated with license bundles. If enough licenses are not available for either the license level
        or the license bundle, a partial error is returned with the index of the activateUsers input.
        """
        return cls.execute_soa_method(
            method_name='activateUsers2',
            library='Internal-Administration',
            service_date='2013_05',
            service_name='UserManagement',
            params={'activateUsers': activateUsers},
            response_cls=LicenseStatusResponse,
        )
