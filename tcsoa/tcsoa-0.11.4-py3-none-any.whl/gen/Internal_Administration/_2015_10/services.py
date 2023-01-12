from __future__ import annotations

from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def resetUserPassword(cls, userid: str, oldpassword: str, newpassword: str) -> bool:
        """
        Changes password of a user. A login user is allowed to modify his(her) own password. As of Teamcenter 11.3, a
        system administrator or privileged user is allowed to modify other users's passwords. This operation will throw
        a ServiceException as described below.".
        
        Use cases:
        This operation is used by the Active Workspace user interface.
        
        Exceptions:
        >Service Exception
        
        10729: Either the specified user ID is not the current session user, or the logged-in user is not a system
        administrator or an authorized user.
        """
        return cls.execute_soa_method(
            method_name='resetUserPassword',
            library='Internal-Administration',
            service_date='2015_10',
            service_name='UserManagement',
            params={'userid': userid, 'oldpassword': oldpassword, 'newpassword': newpassword},
            response_cls=bool,
        )
