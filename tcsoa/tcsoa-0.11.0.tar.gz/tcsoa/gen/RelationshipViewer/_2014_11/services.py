from __future__ import annotations

from tcsoa.gen.RelationshipViewer._2014_11.NetworkEngine import GraphTypeListResponse
from tcsoa.base import TcService


class NetworkEngineService(TcService):

    @classmethod
    def getViews3(cls, key: str) -> GraphTypeListResponse:
        """
        This operation provides a list of the available graph view types identified by the input key. A graph view is a
        set of configuration that can be used for network expansion. For example: localized view name and category
        types which classify a list of supported Teamcenter Business Object types, legend color of each category types.
        The view list is role based, different role may get different view list.
        """
        return cls.execute_soa_method(
            method_name='getViews3',
            library='RelationshipViewer',
            service_date='2014_11',
            service_name='NetworkEngine',
            params={'key': key},
            response_cls=GraphTypeListResponse,
        )
