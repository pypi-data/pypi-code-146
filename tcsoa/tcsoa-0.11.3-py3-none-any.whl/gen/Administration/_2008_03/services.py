from __future__ import annotations

from tcsoa.gen.Administration._2008_03.IRM import LicenseStatusResponse, DeactivateUserInput, ActivateUserInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class IRMService(TcService):

    @classmethod
    def deactivateUsers(cls, deactivateUser: List[DeactivateUserInput]) -> ServiceData:
        """
        This operation deactivates given users and transfers ownership of the objects owned by the users to be
        deactivated to new users if the new users are specified. The users deactivated successfully are added in the
        updated object list of the service data. If new users and groups are specified to take the ownership of the
        objects owned by the deactivated users, then the new users and groups are added in the updated object list as
        well after ownership is successfully transferred. This operation requires system administration privilege.
        """
        return cls.execute_soa_method(
            method_name='deactivateUsers',
            library='Administration',
            service_date='2008_03',
            service_name='IRM',
            params={'deactivateUser': deactivateUser},
            response_cls=ServiceData,
        )

    @classmethod
    def activateUsers(cls, activateUser: List[ActivateUserInput]) -> LicenseStatusResponse:
        """
        This operation can be used to activate user(s) based on the number of allowed active author or consumer
        licenses. If not enough licenses are available, this operation will return corresponding error code for the
        given license level. This operation activates only the user and not the Group Members corresponding to the user.
        """
        return cls.execute_soa_method(
            method_name='activateUsers',
            library='Administration',
            service_date='2008_03',
            service_name='IRM',
            params={'activateUser': activateUser},
            response_cls=LicenseStatusResponse,
        )
