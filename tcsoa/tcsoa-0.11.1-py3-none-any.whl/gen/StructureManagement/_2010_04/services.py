from __future__ import annotations

from tcsoa.gen.StructureManagement._2010_04.StructureSearch import SearchExpressionSet
from tcsoa.gen.StructureManagement._2008_05.StructureSearch import SearchScope, StructureSearchResultResponse
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def startSearch(cls, scope: SearchScope, searchExpression: SearchExpressionSet) -> StructureSearchResultResponse:
        """
        Start searching a structure for a given search expression within the scope specified
        """
        return cls.execute_soa_method(
            method_name='startSearch',
            library='StructureManagement',
            service_date='2010_04',
            service_name='StructureSearch',
            params={'scope': scope, 'searchExpression': searchExpression},
            response_cls=StructureSearchResultResponse,
        )
