from __future__ import annotations

from tcsoa.gen.Core._2020_04.DataManagement import GenerateContextIDsInput2
from tcsoa.gen.Core._2016_05.DataManagement import GenerateContextSpecificIDsResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def generateContextSpecificIDs2(cls, generateContextIDsIn: List[GenerateContextIDsInput2]) -> GenerateContextSpecificIDsResponse:
        """
        Generates the range of unique IDs for input context names. The number of IDs generated for each context name
        depends on the input. If for a given context name, the ID has been reset using Teamcenter service
        resetContextID, then this service generates IDs for that context from the beginning.
        
        ID generation will also reset when the maximum limit is met. This limit is maximum number supported on 64 bit
        machine.
        
        If the validation flag is true and both contextType and contextPropName are provided, the generated IDs will be
        validated for uniquness.
        """
        return cls.execute_soa_method(
            method_name='generateContextSpecificIDs2',
            library='Core',
            service_date='2020_04',
            service_name='DataManagement',
            params={'generateContextIDsIn': generateContextIDsIn},
            response_cls=GenerateContextSpecificIDsResponse,
        )
