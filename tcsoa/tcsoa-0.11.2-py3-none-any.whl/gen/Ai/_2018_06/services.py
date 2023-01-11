from __future__ import annotations

from tcsoa.gen.Ai._2018_06.Ai import GetObjectsByApplicationRefsResponse, ConfigurationInfo
from typing import List
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def getObjectsByApplicationRefs(cls, input: List[ConfigurationInfo]) -> GetObjectsByApplicationRefsResponse:
        """
        This operation finds business objects associated with the list of input ApplicationRef objects. The
        ApplicationRef can be associated with either persisent or runtime business objects. One business object is
        returned for each ApplicationRef. If no associated business object can be found for an ApplicationRef then a
        NULL  is returned for that entry.
        """
        return cls.execute_soa_method(
            method_name='getObjectsByApplicationRefs',
            library='Ai',
            service_date='2018_06',
            service_name='Ai',
            params={'input': input},
            response_cls=GetObjectsByApplicationRefsResponse,
        )
