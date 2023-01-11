from __future__ import annotations

from tcsoa.gen.StructureManagement._2016_09.PublishByLink import FindSourcesResponse
from tcsoa.gen.StructureManagement._2007_06.PublishByLink import LineAndWindow
from typing import List
from tcsoa.base import TcService


class PublishByLinkService(TcService):

    @classmethod
    def findSourcesInWindow(cls, input: List[LineAndWindow]) -> FindSourcesResponse:
        """
        Finds all source BOMLines objects of the PublishLink in source BOMWindow for input target BOMLine objects. All
        sources are returned as BOMLine objects.
        
        Use cases:
        Determine if BOMWindow has sources for input target BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='findSourcesInWindow',
            library='StructureManagement',
            service_date='2016_09',
            service_name='PublishByLink',
            params={'input': input},
            response_cls=FindSourcesResponse,
        )
