from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Manufacturing._2011_12.DataManagement import PostAssignIDICInput, PostAssignIDICResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def postAssignIDICMaker(cls, postAssignInput: List[PostAssignIDICInput]) -> PostAssignIDICResponse:
        """
        This operation creates IDIC (ID in context) for assembly parts in EBOM and PMI contexts. So far, IDIC heas
        generated for occurrences in consumption level only. This operation provides functionality to generate IDIC for
        received occurrences in any level.
        """
        return cls.execute_soa_method(
            method_name='postAssignIDICMaker',
            library='Internal-Manufacturing',
            service_date='2011_12',
            service_name='DataManagement',
            params={'postAssignInput': postAssignInput},
            response_cls=PostAssignIDICResponse,
        )
