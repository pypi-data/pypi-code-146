from __future__ import annotations

from tcsoa.gen.Internal.Integration._2007_06.IntegrationManagement import ConnectResponse
from tcsoa.base import TcService


class IntegrationManagementService(TcService):

    @classmethod
    def connect(cls, inputVal: int, action: str) -> ConnectResponse:
        """
        Perform the License related operation such as :
        ILM__init_module:   Initialize the license module if it has not already been initialized.
        ILM__leave_module:  De-allocate license of the given module. If the user had N free licenses for this module,
        he will have (N+1) left after this call
        ILM__check_module:  Check to see if the User has bought this module and return the number of licenses purchased
        ILM__enter_module:  Allocate one license of the given module. If the user has bought N licenses for this module,
        he will have (N-1) left after this call
        ILM__exit_module:   Leave the module.
        """
        return cls.execute_soa_method(
            method_name='connect',
            library='Internal-Integration',
            service_date='2007_06',
            service_name='IntegrationManagement',
            params={'inputVal': inputVal, 'action': action},
            response_cls=ConnectResponse,
        )
