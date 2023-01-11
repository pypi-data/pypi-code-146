from __future__ import annotations

from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def getSecurityToken(cls, duration: int) -> str:
        """
        This operation returns a security token for the current user. This token can be used as the 'password' argument
        on the 'login' service operations. The token is valid for the duration specified on the input, if used in the
        'login' operation after that duration, the 'login' operation will fail. A session established with this token
        is still subject to a session time-out due to inactivity. At which point the client application will be
        presented with an authentication challenge through the 'CredentialManager' interface. The client application's
        implementation of the 'CredentialManager' interface is responsible for obtaining the user's credentials (i.e.
        prompting the user) before continuing on with the session.
        
        Exceptions:
        >- 214184:    Failed to generate the security token.
        
        """
        return cls.execute_soa_method(
            method_name='getSecurityToken',
            library='Internal-Core',
            service_date='2014_11',
            service_name='Session',
            params={'duration': duration},
            response_cls=str,
        )
