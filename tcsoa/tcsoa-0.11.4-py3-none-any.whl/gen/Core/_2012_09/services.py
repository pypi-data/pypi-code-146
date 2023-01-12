from __future__ import annotations

from tcsoa.gen.Core._2012_09.ProjectLevelSecurity import ProjectTeamsResponse, ProjectClientId, ProjectOpsResponse, CopyProjectsInfo, ProjectInformation, ModifyProjectsInfo
from typing import List
from tcsoa.gen.Core._2012_09.DataManagement import RelateInfoIn
from tcsoa.gen.Core._2011_06.DataManagement import SaveAsIn, SaveAsObjectsResponse
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def modifyProjects(cls, modifyProjectsInfos: List[ModifyProjectsInfo]) -> ProjectOpsResponse:
        """
        This operation modifies the given list of TC_Project objects using the input specified. The input contains new
        values for all the project properties. Values for properties other than the project team are ignored unless the
        user is the Project Administrator.
        
        The entire Project Team, with the exception of the Project Administrator, is replaced with the specified team.
        Therefore, a Project Team Administrator must be specified. If the new Project Team is different than the
        current team, the user performing this operation must be either the Project Administrator or Project Team
        Administrator for the project being modified.
        """
        return cls.execute_soa_method(
            method_name='modifyProjects',
            library='Core',
            service_date='2012_09',
            service_name='ProjectLevelSecurity',
            params={'modifyProjectsInfos': modifyProjectsInfos},
            response_cls=ProjectOpsResponse,
        )

    @classmethod
    def copyProjects(cls, copyProjectsInfos: List[CopyProjectsInfo]) -> ProjectOpsResponse:
        """
        This operation copies  the given list of TC_Project objects. The operation also copies any information which is
        in contained in the project. Data such as project team members and any objects assigned to the source project
        will also be copied to the new project. If a project with given project ID exists in the system then this
        operation will return error 101010.  The operation will continue with copying the other projects.
        """
        return cls.execute_soa_method(
            method_name='copyProjects',
            library='Core',
            service_date='2012_09',
            service_name='ProjectLevelSecurity',
            params={'copyProjectsInfos': copyProjectsInfos},
            response_cls=ProjectOpsResponse,
        )

    @classmethod
    def createProjects(cls, projectInfos: List[ProjectInformation]) -> ProjectOpsResponse:
        """
        This operation creates TC_Project objects using the given input information. If the project with given project
        ID exists in the system then this operation will return unique id violation error 101010.  However, creation of
        rest of the projects will continue.
        """
        return cls.execute_soa_method(
            method_name='createProjects',
            library='Core',
            service_date='2012_09',
            service_name='ProjectLevelSecurity',
            params={'projectInfos': projectInfos},
            response_cls=ProjectOpsResponse,
        )

    @classmethod
    def getProjectTeams(cls, projectObjs: List[ProjectClientId]) -> ProjectTeamsResponse:
        """
        This operation returns team members for the given list of TC_Project objects.
        """
        return cls.execute_soa_method(
            method_name='getProjectTeams',
            library='Core',
            service_date='2012_09',
            service_name='ProjectLevelSecurity',
            params={'projectObjs': projectObjs},
            response_cls=ProjectTeamsResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def saveAsObjectAndRelate(cls, saveAsInput: List[SaveAsIn], relateInfo: List[RelateInfoIn]) -> SaveAsObjectsResponse:
        """
        This operation saves the given object and its related objects as new instances. Related objects are identifed
        using deep copy rules. Optionally,this method relates the new object to the input target object or to a default
        folder.
        """
        return cls.execute_soa_method(
            method_name='saveAsObjectAndRelate',
            library='Core',
            service_date='2012_09',
            service_name='DataManagement',
            params={'saveAsInput': saveAsInput, 'relateInfo': relateInfo},
            response_cls=SaveAsObjectsResponse,
        )
