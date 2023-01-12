from __future__ import annotations

from tcsoa.gen.Internal.Administration._2019_06.UserManagement import GetGroupRoleViewModelInput, GetGroupRoleViewModelResponse
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def getGroupRoleViewModelRows(cls, input: GetGroupRoleViewModelInput) -> GetGroupRoleViewModelResponse:
        """
        This operation returns the list of view models which can be later consumed in Active Workspace client. The view
        model captures the information about the group and associated default role for the group where the input user
        has active membership. Active Workspace table widgets are capable of consuming these view models and each view
        model will represent a row in the Active Workspace table widget. 
        
        Normally Active Workspace table when rendering business objects shown object represented by a rows and
        specified properties on the object as columns. But in few special cases where we really can&rsquo;t show the
        object properties as is on the column, there we need some way out. This ViewModel approach helps in handling
        such cases. For Example: User&rsquo;s Groups and default Role associated with those groups is actually a
        boolean property with the data model. But on Active Workspace UI we want to show this default role as a string
        LOV. To handle this conversion we make use of ViewModel object.
        """
        return cls.execute_soa_method(
            method_name='getGroupRoleViewModelRows',
            library='Internal-Administration',
            service_date='2019_06',
            service_name='UserManagement',
            params={'input': input},
            response_cls=GetGroupRoleViewModelResponse,
        )
