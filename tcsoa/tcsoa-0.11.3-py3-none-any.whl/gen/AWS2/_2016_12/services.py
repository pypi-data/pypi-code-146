from __future__ import annotations

from tcsoa.gen.AWS2._2016_12.UiConfig import GetUIConfigInput, GetUIConfigResponse
from typing import List
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def getUIConfigs2(cls, getUiConfigsIn: List[GetUIConfigInput]) -> GetUIConfigResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes command and column configuration information. This operation replaces getUIConfigs operation, it
        returns the Awp0CommandCollectionRel objects that associate the top level command collections to client scope
        in CommandConfigData2 structure instead of Awp0CommandCollection objects in CommandConfigData.
        """
        return cls.execute_soa_method(
            method_name='getUIConfigs2',
            library='AWS2',
            service_date='2016_12',
            service_name='UiConfig',
            params={'getUiConfigsIn': getUiConfigsIn},
            response_cls=GetUIConfigResponse,
        )
