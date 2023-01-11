import logging
from typing import Any, Dict, List, Optional, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.user_manager_service_communicator import \
    UserManagerServiceCommunicator
from truera.client.public.communicator.user_manager_service_http_communicator import \
    HttpUserManagerServiceCommunicator
from truera.protobuf.rbac import rbac_pb2 as rbac_pb


class UserManagerServiceClient():

    def __init__(
        self,
        communicator: UserManagerServiceCommunicator,
        logger=None
    ) -> None:
        self.logger = logger if logger else logging.getLogger(__name__)
        self.communicator = communicator

    @classmethod
    def create(
        cls,
        connection_string: str = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if use_http:
            communicator = HttpUserManagerServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.user_manager_service_grpc_communicator import \
                GrpcUserManagerServiceCommunicator
            communicator = GrpcUserManagerServiceCommunicator(
                connection_string, auth_details, logger
            )
        return UserManagerServiceClient(communicator, logger)

    def add_user_as_admin(
        self,
        subject_id: str,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.AdminRequest(subject_id=subject_id)
        authorization_response = self.communicator.add_user_as_admin(
            req, request_context=request_context
        )
        return authorization_response

    def remove_user_as_admin(
        self,
        subject_id=None,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.AdminRequest(subject_id=subject_id)
        authorization_response = self.communicator.remove_user_as_admin(
            req, request_context=request_context
        )
        return authorization_response

    def add_user(
        self,
        user_id: str,
        user_name: str,
        user_email: str,
        subject_ids: List[str],
        user_info: Dict[str, Any],
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        user = rbac_pb.User(
            id=user_id,
            name=user_name,
            email=user_email,
            subject_ids=subject_ids,
            user_info=user_info
        )
        req = rbac_pb.AddUserRequest(user=user)
        authorization_response = self.communicator.add_user(
            req, request_context=request_context
        )
        return authorization_response

    def get_users(
        self,
        filter: Optional[List[str]] = None,
        request_context=None
    ) -> rbac_pb.GetUsersResponse:
        if filter is None:
            filter = []
        req = rbac_pb.GetUsersFilter(contains=filter)
        get_users_repsonse = self.communicator.get_users(
            req, request_context=request_context
        )
        return get_users_repsonse

    def auto_add_user(self, request_context=None) -> rbac_pb.GetUsersResponse:
        req = rbac_pb.AutoUserRequest()
        auto_user_repsonse = self.communicator.auto_add_user(
            req, request_context=request_context
        )
        return auto_user_repsonse

    def add_user_to_project(
        self,
        subject_id: str,
        project_id: str,
        as_owner: bool,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.UserProjectRequest(
            subject_id=subject_id, project_id=project_id, as_owner=as_owner
        )
        authorization_response = self.communicator.add_user_to_project(
            req, request_context=request_context
        )
        return authorization_response

    def remove_user_from_project(
        self,
        subject_id: str,
        project_id: str,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.UserProjectRequest(
            subject_id=subject_id, project_id=project_id
        )
        authorization_response = self.communicator.remove_user_from_project(
            req, request_context=request_context
        )
        return authorization_response

    def authorize_create_project(
        self,
        project_id: str,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.ProjectRequest(project_id=project_id)
        authorization_response = self.communicator.authorize_create_project(
            req, request_context=request_context
        )
        return authorization_response

    def authorize_archive_project(
        self,
        project_id: str,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.ProjectRequest(project_id=project_id)
        authorization_response = self.communicator.authorize_archive_project(
            req, request_context=request_context
        )
        return authorization_response

    def get_current_user(self):
        auto_add_response = self.auto_add_user()
        assert len(auto_add_response.users) == 1
        return auto_add_response.users[0]

    def accept_user_terms_of_service(
        self, request_context=None
    ) -> rbac_pb.GetUsersResponse:
        req = rbac_pb.AutoUserRequest()
        auto_user_repsonse = self.communicator.accept_user_terms_of_service(
            req, request_context=request_context
        )
        return auto_user_repsonse

    def create_group_with_proto(
        self,
        name: str,
        email: str,
        description: str,
        request_context=None,
    ) -> rbac_pb.CreateGroupResponse:
        req = rbac_pb.CreateGroupRequest(
            name=name, email=email, description=description
        )
        group_resp = self.communicator.create_group(
            req, request_context=request_context
        )
        return group_resp

    def get_group_with_proto(
        self,
        group_id: str,
        request_context=None,
    ) -> rbac_pb.GroupInfoResponse:
        req = rbac_pb.GroupRequest(group_id=group_id)
        group_resp = self.communicator.get_group(
            req, request_context=request_context
        )
        return group_resp

    def delete_group_with_proto(
        self,
        group_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        req = rbac_pb.GroupRequest(group_id=group_id)
        group_resp = self.communicator.delete_group(
            req, request_context=request_context
        )
        return group_resp

    def add_users_to_group_with_proto(
        self,
        group_id: str,
        user_ids: List,
        request_context=None,
    ) -> rbac_pb.GroupInfoResponse:
        req = rbac_pb.GroupUsersRequest(group_id=group_id, user_ids=user_ids)
        group_resp = self.communicator.add_users_to_group(
            req, request_context=request_context
        )
        return group_resp

    def remove_users_from_group_with_proto(
        self,
        group_id: str,
        user_ids: List,
        request_context=None,
    ) -> rbac_pb.GroupInfoResponse:
        req = rbac_pb.GroupUsersRequest(group_id=group_id, user_ids=user_ids)
        group_resp = self.communicator.remove_users_from_group(
            req, request_context=request_context
        )
        return group_resp

    def get_groups_with_proto(
        self,
        user_id: str,
        request_context=None,
    ) -> rbac_pb.GetGroupsResponse:
        req = rbac_pb.GetGroupsRequest(user_id=user_id)
        group_resp = self.communicator.get_groups(
            req, request_context=request_context
        )
        return group_resp

    def update_group_with_proto(
        self,
        group_id: str,
        name: str,
        description: str,
        request_context=None,
    ) -> rbac_pb.GetGroupsResponse:
        req = rbac_pb.UpdateGroupRequest(
            group_id=group_id, name=name, description=description
        )
        group_resp = self.communicator.update_group(
            req, request_context=request_context
        )
        return group_resp
