from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def getProperties(cls, objects: List[BusinessObject], attributes: List[str]) -> ServiceData:
        """
        This is a wrapper to the 'DataManagement.getProperties' operation, and is provided only to give the client
        framework the ability to complete a partial response when the server side limits the size of the return payload.
        """
        return cls.execute_soa_method(
            method_name='getProperties',
            library='Internal-Core',
            service_date='2007_12',
            service_name='Session',
            params={'objects': objects, 'attributes': attributes},
            response_cls=ServiceData,
        )
