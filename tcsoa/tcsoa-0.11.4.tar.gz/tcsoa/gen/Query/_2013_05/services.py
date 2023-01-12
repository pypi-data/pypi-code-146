from __future__ import annotations

from typing import List
from tcsoa.gen.Query._2013_05.SavedQuery import SavedQueryProperties
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def createSavedQueries(cls, inputs: List[SavedQueryProperties]) -> ServiceData:
        """
        Creates a list of saved queries based on the input properties structure.
        """
        return cls.execute_soa_method(
            method_name='createSavedQueries',
            library='Query',
            service_date='2013_05',
            service_name='SavedQuery',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
