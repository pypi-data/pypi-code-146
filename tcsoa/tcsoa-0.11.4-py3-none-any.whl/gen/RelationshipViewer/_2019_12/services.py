from __future__ import annotations

from tcsoa.gen.RelationshipViewer._2019_12.NetworkEngine import GetViewsParamMap
from tcsoa.gen.RelationshipViewer._2014_11.NetworkEngine import GraphTypeListResponse
from tcsoa.base import TcService


class NetworkEngineService(TcService):

    @classmethod
    def getViews4(cls, getViewsInput: GetViewsParamMap) -> GraphTypeListResponse:
        """
        This operation provides a list of the available graph view types identified by the input key and the object
        type. A graph view is a set of configuration that can be used for network expansion. For example: localized
        view name and category types which classify a list of supported Teamcenter Business Object types, legend color
        of each category types. The view list is role based, different role may get different view list.
        """
        return cls.execute_soa_method(
            method_name='getViews4',
            library='RelationshipViewer',
            service_date='2019_12',
            service_name='NetworkEngine',
            params={'getViewsInput': getViewsInput},
            response_cls=GraphTypeListResponse,
        )
