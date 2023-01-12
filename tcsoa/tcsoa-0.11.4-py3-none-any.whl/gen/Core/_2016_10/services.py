from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, Role
from tcsoa.gen.Core._2009_04.ProjectLevelSecurity import LoadProjectDataForUserResponse
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getDefaultProject(cls, tcUser: User, tcGroup: Group, tcRole: Role) -> LoadProjectDataForUserResponse:
        """
        This operation returns a list of the default projects for a given user, group and role combination. If no user
        is specified, it looks for the default project of the current logged in user. If no group and role is
        specified, all default projects for the specified user  are returned. When TC_show_all_user_projects is set to
        TRUE, projects are reteturned regardless of the given user&rsquo;s group and role. Therefore the default
        projects are returned without checking if the user is a member of the default project in the specified group
        and role. When TC_show_all_user_projects is set to FALSE, projects are returned only when the given user has
        the membership in the specified group and role. Therefore the default projects are returned as empty
        
        Use cases:
        Use Case 1: Changing group/role selection in the user setting dialog. The default project will be automatically
        selected in the project field, if the user has the membership in the project with given group and role
        """
        return cls.execute_soa_method(
            method_name='getDefaultProject',
            library='Core',
            service_date='2016_10',
            service_name='ProjectLevelSecurity',
            params={'tcUser': tcUser, 'tcGroup': tcGroup, 'tcRole': tcRole},
            response_cls=LoadProjectDataForUserResponse,
        )
