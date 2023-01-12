import grpc;
import authz_sdk.api_pb2_grpc as authz_grpc;
import authz_sdk.api_pb2 as proto

from authz_sdk.interceptor import client_authentication

"""
Client is the Authz Python SDK client to use to contact the backend server.

You have to construct it with the Authz backend server hostname and a service account
client_id and client_secret.
"""
class Client:
    def __init__(self, host: str, client_id: str, client_secret: str):
        channel = grpc.insecure_channel(host)
        auth_interceptor = client_authentication.ClientAuthenticationInterceptor(channel, client_id, client_secret)

        channel = grpc.intercept_channel(channel, auth_interceptor)
        self.stub = authz_grpc.ApiStub(channel)

    """"
    IsAllowed is a wrapper of Check() method that allows to perform a single
    check if a principal can perform an action on a resource kind and value.
    """
    def IsAllowed(self, principal: str, resource_kind: str, resource_value: str, action: str):
        result = self.stub.Check(proto.CheckRequest(
            checks=[
                proto.Check(
                    principal=principal,
                    resource_kind=resource_kind,
                    resource_value=resource_value,
                    action=action,
                )
            ]
        ))

        return result.checks[0].is_allowed