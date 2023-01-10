from __future__ import annotations

from tcsoa.gen.BusinessObjects import RequestObject, AppInterface
from tcsoa.gen.Ai._2012_09.Ai import FindRequestsFilter, ProjectFilter, FindRequestsResponse, ProjectInfo, RequestInfo, GetRequestsInfo2Response, GetProjectsInfo2Response
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def getProjects(cls, filter: ProjectFilter) -> ServiceData:
        """
        get the Application Interface objects based on a optional filter.
        """
        return cls.execute_soa_method(
            method_name='getProjects',
            library='Ai',
            service_date='2012_09',
            service_name='Ai',
            params={'filter': filter},
            response_cls=ServiceData,
        )

    @classmethod
    def getProjectsInfo2(cls, projects: List[AppInterface]) -> GetProjectsInfo2Response:
        """
        return the projectInfo information for each of the supplied ApplicationInterface Objects.
        """
        return cls.execute_soa_method(
            method_name='getProjectsInfo2',
            library='Ai',
            service_date='2012_09',
            service_name='Ai',
            params={'projects': projects},
            response_cls=GetProjectsInfo2Response,
        )

    @classmethod
    def getRequestsInfo2(cls, robjects: List[RequestObject]) -> GetRequestsInfo2Response:
        """
        get details about specific RequestObjects. These include state desc,status info, custom key value pairs.
        """
        return cls.execute_soa_method(
            method_name='getRequestsInfo2',
            library='Ai',
            service_date='2012_09',
            service_name='Ai',
            params={'robjects': robjects},
            response_cls=GetRequestsInfo2Response,
        )

    @classmethod
    def setProjectsInfo(cls, infos: List[ProjectInfo]) -> ServiceData:
        """
        set the info on the ApplicationInterface Objects.
        """
        return cls.execute_soa_method(
            method_name='setProjectsInfo',
            library='Ai',
            service_date='2012_09',
            service_name='Ai',
            params={'infos': infos},
            response_cls=ServiceData,
        )

    @classmethod
    def setRequestsInfo(cls, infos: List[RequestInfo]) -> ServiceData:
        """
        method to allow caller to set the fields on the RequestObject.
        """
        return cls.execute_soa_method(
            method_name='setRequestsInfo',
            library='Ai',
            service_date='2012_09',
            service_name='Ai',
            params={'infos': infos},
            response_cls=ServiceData,
        )

    @classmethod
    def findRequests(cls, filter: FindRequestsFilter) -> FindRequestsResponse:
        """
        method to find request objects based on the input criteria.
        """
        return cls.execute_soa_method(
            method_name='findRequests',
            library='Ai',
            service_date='2012_09',
            service_name='Ai',
            params={'filter': filter},
            response_cls=FindRequestsResponse,
        )
