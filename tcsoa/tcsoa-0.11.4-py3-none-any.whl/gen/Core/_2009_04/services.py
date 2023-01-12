from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, Role
from tcsoa.gen.Core._2009_04.ProjectLevelSecurity import LoadProjectDataForUserResponse
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def loadProjectDataForUser(cls, user: User, group: Group, role: Role) -> LoadProjectDataForUserResponse:
        """
        This operation returns list of projects for a given user, group and role combination. If no group and role is
        specified it obtains all the projects for the specified user. If any of the arguments passed are invalid an
        error is returned by the operation added as a partial error.
        """
        return cls.execute_soa_method(
            method_name='loadProjectDataForUser',
            library='Core',
            service_date='2009_04',
            service_name='ProjectLevelSecurity',
            params={'user': user, 'group': group, 'role': role},
            response_cls=LoadProjectDataForUserResponse,
        )


class SessionService(TcService):

    @classmethod
    def startOperation(cls) -> str:
        """
        Start an operation bracket.  An operation bracket is a period of execution in which any object will need to be
        refreshed in the server from the database only once.  This allows the client to avoid unnecessary database
        operations that the server might perform redundantly if underlying code accesses the same object multiple
        times.  The client will use the return value to call the 'stopOperation' operation to indicate the end of the
        bracket.  Brackets may be nested or overlapped.  A bracket should start and end within the scope of a single
        client function and should not span a user interaction.  By default, each service operation starts and stops
        its own operation bracket.
        """
        return cls.execute_soa_method(
            method_name='startOperation',
            library='Core',
            service_date='2009_04',
            service_name='Session',
            params={},
            response_cls=str,
        )

    @classmethod
    def stopOperation(cls, opId: str) -> bool:
        """
        Stop an operation bracket, in which objects need to be refreshed only once.  See 'startOperation'.
        """
        return cls.execute_soa_method(
            method_name='stopOperation',
            library='Core',
            service_date='2009_04',
            service_name='Session',
            params={'opId': opId},
            response_cls=bool,
        )
