from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ModelSchema
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def initTypeByNames(cls, typeNames: List[str]) -> ModelSchema:
        """
        Get schema info from server
        """
        return cls.execute_soa_method(
            method_name='initTypeByNames',
            library='Internal-Core',
            service_date='2006_03',
            service_name='Session',
            params={'typeNames': typeNames},
            response_cls=ModelSchema,
        )

    @classmethod
    def initTypeByUids(cls, uids: List[str]) -> ModelSchema:
        """
        Get schema info from server
        """
        return cls.execute_soa_method(
            method_name='initTypeByUids',
            library='Internal-Core',
            service_date='2006_03',
            service_name='Session',
            params={'uids': uids},
            response_cls=ModelSchema,
        )
