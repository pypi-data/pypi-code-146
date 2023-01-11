from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Dict, List, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.rbac_service_communicator import \
    RbacServiceCommunicator
from truera.client.public.communicator.rbac_service_http_communicators import \
    HttpRbacServiceCommunicator
from truera.client.util.proto_enum_mapper import ProtoEnumMapper
from truera.protobuf.rbac import rbac_pb2 as rbac_pb


@dataclass(eq=True, frozen=True)
class UserProjectMatrixEntry(object):
    user_id: str
    user_name: str
    project_id: str
    project_name: str
    privilege: str


class RbacServiceClient():

    def __init__(
        self, communicator: RbacServiceCommunicator, logger=None
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
            communicator = HttpRbacServiceCommunicator(
                connection_string,
                auth_details,
                logger,
                verify_cert=verify_cert
            )
        else:
            from truera.client.private.communicator.rbac_service_grpc_communicators import \
                GrpcRbacServiceCommunicator
            communicator = GrpcRbacServiceCommunicator(
                connection_string, auth_details, logger
            )
        return RbacServiceClient(communicator, logger)

    def check_permission(
        self,
        user_id: str,
        privileges: List[str],
        resource_type: str,
        resource_id: str,
        request_context=None,
    ):
        enum_priviliges = [
            ProtoEnumMapper.get_enum(rbac_pb.Privilege, p) for p in privileges
        ]
        enum_resource_type = ProtoEnumMapper.get_enum(
            rbac_pb.ResourceType, resource_type
        )
        return self.check_permission_with_proto(
            user_id=user_id,
            privileges=enum_priviliges,
            resource_type=enum_resource_type,
            resource_id=resource_id,
            request_context=request_context
        )

    # this method should be used by internal clients and webservices only which are protobuf aware
    def check_permission_with_proto(
        self,
        user_id: str,
        privileges: List[rbac_pb.Privilege],
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        request_context=None,
    ):
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.CheckPermissionRequest(
            user_id=user_id, privileges=privileges, resource_id=resource
        )
        authorization_repsonse = self.communicator.check_permission(
            req, request_context=request_context
        )
        return authorization_repsonse

    def grant_role(
        self,
        subject_id: str,
        resource_type: str,
        resource_id: str,
        role_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        enum_resource_type = ProtoEnumMapper.get_enum(
            rbac_pb.ResourceType, resource_type
        )
        return self.grant_role_with_proto(
            subject_id=subject_id,
            resource_type=enum_resource_type,
            resource_id=resource_id,
            role_id=role_id,
            request_context=request_context
        )

    # this method should be used by internal clients and webservices only which are protobuf aware
    def grant_role_with_proto(
        self,
        subject_id: str,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        role_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.RoleRequest(
            subject_id=subject_id, role_id=role_id, resource_id=resource
        )
        authorization_repsonse = self.communicator.grant_role(
            req, request_context=request_context
        )
        return authorization_repsonse

    def revoke_role(
        self,
        subject_id: str,
        resource_type: str,
        resource_id: str,
        role_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        enum_resource_type = ProtoEnumMapper.get_enum(
            rbac_pb.ResourceType, resource_type
        )
        return self.revoke_role_with_proto(
            subject_id=subject_id,
            resource_type=enum_resource_type,
            resource_id=resource_id,
            role_id=role_id,
            request_context=request_context
        )

    # this method should be used by internal clients and webservices only which are protobuf aware
    def revoke_role_with_proto(
        self,
        subject_id: str,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        role_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.RoleRequest(
            subject_id=subject_id, role_id=role_id, resource_id=resource
        )
        authorization_repsonse = self.communicator.revoke_role(
            req, request_context=request_context
        )
        return authorization_repsonse

    def get_user_permissions(
        self,
        user_id: str,
        request_context=None
    ) -> rbac_pb.PermissionsResponse:
        req = rbac_pb.PermissionsRequest(user_id=user_id)
        permissions_response = self.communicator.get_user_permissions(
            req, request_context=request_context
        )
        return permissions_response

    def get_user_roles(
        self,
        user_id: str = None,
        request_context=None
    ) -> rbac_pb.GetRolesResponse:
        if user_id:
            req = rbac_pb.GetRolesRequest(user_id=user_id)
        else:
            req = rbac_pb.GetRolesRequest()
        get_roles_response = self.communicator.get_user_roles(
            req, request_context=request_context
        )
        return get_roles_response

    def get_user_resources(
        self,
        user_id: str,
        privileges: List[str],
        resource_types: List[str],
        request_context=None
    ) -> rbac_pb.GetResourceResponse:
        enum_priviliges = [
            ProtoEnumMapper.get_enum(rbac_pb.Privilege, p) for p in privileges
        ]
        enum_resource_types = [
            ProtoEnumMapper.get_enum(rbac_pb.ResourceType, r)
            for r in resource_types
        ]
        return self.get_user_resources_with_proto(
            user_id=user_id,
            privileges=enum_priviliges,
            resource_types=enum_resource_types,
            request_context=request_context
        )

    # this method should be used by internal clients and webservices only which are protobuf aware
    def get_user_resources_with_proto(
        self,
        user_id: str,
        privileges: List[rbac_pb.Privilege],
        resource_types: List[rbac_pb.ResourceType],
        request_context=None
    ) -> rbac_pb.GetResourceResponse:
        req = rbac_pb.GetResourceFilter(
            user_id=user_id,
            privileges=privileges,
            resource_types=resource_types
        )
        get_resource_response = self.communicator.get_user_resources(
            req, request_context=request_context
        )
        return get_resource_response

    def get_user_project_matrix(
        self, project_name_ids: Dict[str, str], users: List[rbac_pb.User]
    ) -> List[UserProjectMatrixEntry]:
        user_project_matrix = []
        for user in users:
            user_permissions = self.get_user_permissions(
                user_id=user.id
            ).permissions
            for permission in user_permissions:
                if permission.resource_id.resource_id in project_name_ids:
                    user_project_matrix.append(
                        UserProjectMatrixEntry(
                            user_id=user.id,
                            user_name=user.name,
                            project_id=permission.resource_id.resource_id,
                            project_name=project_name_ids[
                                permission.resource_id.resource_id],
                            privilege=rbac_pb.Privilege.Name(
                                permission.privilege
                            )
                        )
                    )
        return user_project_matrix

    def is_user_admin(self, user_id) -> bool:
        user_roles = self.get_user_roles(user_id=user_id).roles
        for role in user_roles:
            if role.role_id == "Admin":
                return True
        return False

    # v1 APIs
    def grant_subject_role_for_resource_v1(
        self,
        subject_id: str,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        role_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.RoleRequest(
            subject_id=subject_id, role_id=role_id, resource_id=resource
        )
        authorization_repsonse = self.communicator.grant_subject_role_for_resource(
            req, request_context=request_context
        )
        return authorization_repsonse

    def revoke_subject_role_for_resource_v1(
        self,
        subject_id: str,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        role_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.RoleRequest(
            subject_id=subject_id, role_id=role_id, resource_id=resource
        )
        authorization_repsonse = self.communicator.revoke_subject_role_for_resource(
            req, request_context=request_context
        )
        return authorization_repsonse

    def remove_subject_from_resource_v1(
        self,
        subject_id: str,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.SubjectResourceRequest(
            subject_id=subject_id, resource_id=resource
        )
        authorization_repsonse = self.communicator.remove_subject_from_resource(
            req, request_context=request_context
        )
        return authorization_repsonse

    def authorize_create_resource_v1(
        self,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.AuthorizeResourceRequest(resource_id=resource)
        authorization_repsonse = self.communicator.authorize_create_resource(
            req, request_context=request_context
        )
        return authorization_repsonse

    def authorize_archive_resource_v1(
        self,
        resource_type: rbac_pb.ResourceType,
        resource_id: str,
        request_context=None,
    ) -> rbac_pb.AuthorizationResponse:
        resource = rbac_pb.ResourceId(
            resource_id=resource_id, resource_type=resource_type
        )
        req = rbac_pb.AuthorizeResourceRequest(resource_id=resource)
        authorization_repsonse = self.communicator.authorize_archive_resource(
            req, request_context=request_context
        )
        return authorization_repsonse
