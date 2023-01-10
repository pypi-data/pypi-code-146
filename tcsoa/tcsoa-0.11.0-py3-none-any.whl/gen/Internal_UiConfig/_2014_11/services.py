from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.UiConfig._2014_11.UiConfig import ResetUIConfigInput, ResetUIConfigResponse
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def resetUIConfigs(cls, resetUiConfigsIn: List[ResetUIConfigInput]) -> ResetUIConfigResponse:
        """
        If a client needs to reset the column and/or command information for one or more client scopes, they can use
        this operation with the scope of the login user to receive the new effective UI configuration.
        """
        return cls.execute_soa_method(
            method_name='resetUIConfigs',
            library='Internal-UiConfig',
            service_date='2014_11',
            service_name='UiConfig',
            params={'resetUiConfigsIn': resetUiConfigsIn},
            response_cls=ResetUIConfigResponse,
        )
