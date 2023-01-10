from __future__ import annotations

from tcsoa.gen.Internal.Core._2007_06.ProjectLevelSecurity import TopLevelHierarchyOutputResponse, ProjectSmartFolderHierarchyOutputResponse, GetFilteredProjectDataInputData, GetFilteredProjectDataResponse
from typing import List
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getProjectsSmartFolderHierarchy(cls, projectIDs: List[str]) -> ProjectSmartFolderHierarchyOutputResponse:
        """
        This operation gets a list of  project smart folder hierarchy for each of the given project ids. If the project
        ID given in the argument does not exists error code 101007: the project ID is invalid; will be returned in a
        partial error.
        """
        return cls.execute_soa_method(
            method_name='getProjectsSmartFolderHierarchy',
            library='Internal-Core',
            service_date='2007_06',
            service_name='ProjectLevelSecurity',
            params={'projectIDs': projectIDs},
            response_cls=ProjectSmartFolderHierarchyOutputResponse,
        )

    @classmethod
    def getTopLevelSmartFolderHierarchy(cls) -> TopLevelHierarchyOutputResponse:
        """
        This operation returns top-level smart folder hierarchy as configured by the administrator.  For more
        information on smart folder hierarchy refer to Teamcenter documentation under administration section of Project
        Level Security. If the global constant named "ProjectTopLevelSmartFolders" does not exist in the system then
        the operation returns an empty list. There are no errors that will be returned.
        """
        return cls.execute_soa_method(
            method_name='getTopLevelSmartFolderHierarchy',
            library='Internal-Core',
            service_date='2007_06',
            service_name='ProjectLevelSecurity',
            params={},
            response_cls=TopLevelHierarchyOutputResponse,
        )

    @classmethod
    def getFilteredProjectData(cls, input: List[GetFilteredProjectDataInputData]) -> GetFilteredProjectDataResponse:
        """
        This operation obtains data contained in a specified project by applying the given filter criteria. If no
        filter criteria is specified in the input argument all data in the project is returned. If the project id
        specified in the argument does not exist then s error code 101007: the project ID is invalid is returned and if
        the specified type does not exist in the system and error 39007: The specified name type name is invalid for a
        type is returned.
        """
        return cls.execute_soa_method(
            method_name='getFilteredProjectData',
            library='Internal-Core',
            service_date='2007_06',
            service_name='ProjectLevelSecurity',
            params={'input': input},
            response_cls=GetFilteredProjectDataResponse,
        )
