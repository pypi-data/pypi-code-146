from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Manufacturing._2012_09.StructureSearch import SaveOGLinesInSrchCriteriaResponse, MapSrchCriteriaToLinesResponse, SaveOGLinesInSrchCriteriaInputInfo, MapSrchCriteriaToLinesInputInfo
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def mapSrchCriteriaToLines(cls, inputs: List[MapSrchCriteriaToLinesInputInfo]) -> MapSrchCriteriaToLinesResponse:
        """
        This operation interprets the given search criteria objects and returns the saved BOM line occurrences from the
        input BOM line scope(s).
        """
        return cls.execute_soa_method(
            method_name='mapSrchCriteriaToLines',
            library='Internal-Manufacturing',
            service_date='2012_09',
            service_name='StructureSearch',
            params={'inputs': inputs},
            response_cls=MapSrchCriteriaToLinesResponse,
        )

    @classmethod
    def saveOGLinesInSrchCriteria(cls, inputs: List[SaveOGLinesInSrchCriteriaInputInfo]) -> SaveOGLinesInSrchCriteriaResponse:
        """
        This operation stores the BOM line occurrences under the Occurrence Group structure in a search criteria object.
        """
        return cls.execute_soa_method(
            method_name='saveOGLinesInSrchCriteria',
            library='Internal-Manufacturing',
            service_date='2012_09',
            service_name='StructureSearch',
            params={'inputs': inputs},
            response_cls=SaveOGLinesInSrchCriteriaResponse,
        )
