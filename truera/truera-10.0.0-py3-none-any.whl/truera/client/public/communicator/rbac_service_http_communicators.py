import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator
from truera.client.public.communicator.rbac_service_communicator import \
    RbacServiceCommunicator
from truera.protobuf.rbac import rbac_pb2 as rbac_pb


class HttpRbacServiceCommunicator(RbacServiceCommunicator):

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        connection_string = connection_string.rstrip("/")
        self.connection_string = f"{connection_string}/api/rbac"
        self.http_communicator = HttpCommunicator(
            connection_string=self.connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def check_permission(
        self,
        req: rbac_pb.CheckPermissionRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/{user_id}/resource/{resource_type}/{resource_id}".format(
            conn=self.connection_string,
            user_id=req.user_id,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def grant_role(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/{subject_id}/resource/{resource_type}/{resource_id}/role/{role_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id,
            role_id=req.role_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def revoke_role(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/user/{subject_id}/resource/{resource_type}/{resource_id}/role/{role_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id,
            role_id=req.role_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def get_user_permissions(
        self,
        req: rbac_pb.PermissionsRequest,
        request_context=None
    ) -> rbac_pb.PermissionsResponse:
        uri = "{conn}/users/permission".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.PermissionsResponse()
        )

    def get_user_roles(
        self,
        req: rbac_pb.GetRolesRequest,
        request_context=None
    ) -> rbac_pb.GetRolesResponse:
        uri = "{conn}/users/role".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.GetRolesResponse()
        )

    def get_user_resources(
        self,
        req: rbac_pb.GetResourceFilter,
        request_context=None
    ) -> rbac_pb.GetResourceResponse:
        uri = "{conn}/users/resource".format(conn=self.connection_string)
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.get_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.GetResourceResponse()
        )

    # v1 APIs
    def grant_subject_role_for_resource(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/v1/subjects/{subject_id}/resources/{resource_type}/{resource_id}/roles/{role_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id,
            role_id=req.role_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def revoke_subject_role_for_resource(
        self,
        req: rbac_pb.RoleRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/v1/subjects/{subject_id}/resources/{resource_type}/{resource_id}/roles/{role_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id,
            role_id=req.role_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def remove_subject_from_resource(
        self,
        req: rbac_pb.SubjectResourceRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/v1/resources/{resource_type}/{resource_id}/subjects/{subject_id}".format(
            conn=self.connection_string,
            subject_id=req.subject_id,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def authorize_create_resource(
        self,
        req: rbac_pb.AuthorizeResourceRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/v1/resources/{resource_type}/{resource_id}".format(
            conn=self.connection_string,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.post_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )

    def authorize_archive_resource(
        self,
        req: rbac_pb.AuthorizeResourceRequest,
        request_context=None
    ) -> rbac_pb.AuthorizationResponse:
        uri = "{conn}/v1/resources/{resource_type}/{resource_id}".format(
            conn=self.connection_string,
            resource_type=req.resource_id.resource_type,
            resource_id=req.resource_id.resource_id
        )
        json_req = self.http_communicator._proto_to_json(req)
        json_resp = self.http_communicator.delete_request(uri, json_req)
        return self.http_communicator._json_to_proto(
            json_resp, rbac_pb.AuthorizationResponse()
        )
