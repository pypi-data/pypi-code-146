from __future__ import annotations

from typing import List
from tcsoa.gen.Administration._2014_10.UserManagement import MakeUserResponse
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def makeUser(cls, arguments: List[str], batchFileFmsTicket: str, enableStandardOutput: bool, enableStandardError: bool) -> MakeUserResponse:
        """
        This operation executes the make_user utility on the Teamcenter server with the specified command line
        arguments and optional batch input file. The make_user utility runs with the same user and group as the current
        session user.
        """
        return cls.execute_soa_method(
            method_name='makeUser',
            library='Administration',
            service_date='2014_10',
            service_name='UserManagement',
            params={'arguments': arguments, 'batchFileFmsTicket': batchFileFmsTicket, 'enableStandardOutput': enableStandardOutput, 'enableStandardError': enableStandardError},
            response_cls=MakeUserResponse,
        )
