from __future__ import annotations

from tcsoa.gen.UiConfig._2014_11.UiConfig import GetUIConfigInput
from tcsoa.gen.UiConfig._2015_10.UiConfig import GetUIConfigResponse
from typing import List
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def getUIConfigs2(cls, getUiConfigsIn: List[GetUIConfigInput]) -> GetUIConfigResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes command and column configuration information. This operation replaces getUIConfigs operation, it
        returns the Fnd0CommandCollectionRel objects that associate the top level command collections to client scope
        in CommandConfigData structure in addition to Fnd0CommandCollection objects.
        """
        return cls.execute_soa_method(
            method_name='getUIConfigs2',
            library='UiConfig',
            service_date='2015_10',
            service_name='UiConfig',
            params={'getUiConfigsIn': getUiConfigsIn},
            response_cls=GetUIConfigResponse,
        )
