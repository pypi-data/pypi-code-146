from __future__ import annotations

from tcsoa.gen.Ai._2006_03.Ai import Configuration
from tcsoa.gen.Ai._2008_05.Ai import GenerateArrangementsResponse
from tcsoa.gen.BusinessObjects import ItemRevision
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def generateArrangements(cls, itemRev: ItemRevision, revRule: Configuration, bvType: str) -> GenerateArrangementsResponse:
        """
        The generateArrangements operation will generate a PLMXML file with arrangements for an Item Revision.
        This operation will find out the BOMView Revision with input BOMView Type associated to the Item Revision
        at first and then do generating process. An Item Revision and a BOMView Type can specify an unique BOMView
        Revision.
        If input BOMView Type is NULL, the default BOMView Type will be picked up. A revision rule can be applied to
        the BOMView Revision while generating. The output is struct GenerateArrangementsResponse with generated PLMXML
        file ticket
        and soa service data.
        """
        return cls.execute_soa_method(
            method_name='generateArrangements',
            library='Ai',
            service_date='2008_05',
            service_name='Ai',
            params={'itemRev': itemRev, 'revRule': revRule, 'bvType': bvType},
            response_cls=GenerateArrangementsResponse,
        )
