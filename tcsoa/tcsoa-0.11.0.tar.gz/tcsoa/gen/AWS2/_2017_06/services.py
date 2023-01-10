from __future__ import annotations

from tcsoa.gen.AWS2._2017_06.UiConfig import GetUIConfigInput, GetUIConfigResponse
from typing import List
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def getUIConfigs3(cls, getUiConfigsIn: List[GetUIConfigInput]) -> GetUIConfigResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes command and column configuration information. The returned information includes
        Fnd0CommandCollectionRel objects that associate the top level command collections to client scope in
        CommandConfigData structure.
        """
        return cls.execute_soa_method(
            method_name='getUIConfigs3',
            library='AWS2',
            service_date='2017_06',
            service_name='UiConfig',
            params={'getUiConfigsIn': getUiConfigsIn},
            response_cls=GetUIConfigResponse,
        )
