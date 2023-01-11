from abc import ABC
from abc import abstractmethod

from truera.protobuf.rbac import rbac_pb2 as rbac_pb


class RbacServiceCommunicator(ABC):

    @abstractmethod
    def check_permission(
        self,
        req: rbac_pb.CheckPermissionRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def grant_role(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def revoke_role(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def get_user_permissions(
        self,
        req: rbac_pb.PermissionsRequest,
        request_context=None
    ) -> rbac_pb.PermissionsResponse:
        pass

    @abstractmethod
    def get_user_roles(
        self,
        req: rbac_pb.GetRolesRequest,
        request_context=None
    ) -> rbac_pb.GetRolesResponse:
        pass

    @abstractmethod
    def get_user_resources(
        self,
        req: rbac_pb.GetResourceFilter,
        request_context=None
    ) -> rbac_pb.GetResourceResponse:
        pass

    @abstractmethod
    def grant_subject_role_for_resource(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def revoke_subject_role_for_resource(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def remove_subject_from_resource(
        self,
        req: rbac_pb.SubjectResourceRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def authorize_create_resource(
        self,
        req: rbac_pb.AuthorizeResourceRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass

    @abstractmethod
    def authorize_archive_resource(
        self,
        req: rbac_pb.AuthorizeResourceRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        pass
