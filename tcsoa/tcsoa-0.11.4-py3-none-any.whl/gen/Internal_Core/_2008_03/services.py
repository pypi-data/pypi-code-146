from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def disableUserSessionState(cls, names: List[str]) -> ServiceData:
        """
        Remove the named User Session State variables from the client context, and make the Teamcenter Server that
        master for these state variables. All client applications sharing the instance of the Teamcenter Server will
        use the current values of the named state variables.   The current value of the state variable as defined by
        this calling client application will become the master value for all clients.
        """
        return cls.execute_soa_method(
            method_name='disableUserSessionState',
            library='Internal-Core',
            service_date='2008_03',
            service_name='Session',
            params={'names': names},
            response_cls=ServiceData,
        )
