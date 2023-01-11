import grpc;
import authz_sdk.api_pb2_grpc as authz_grpc;
from authz_sdk.interceptor import client_authentication

class Client:
    def __init__(self, host: str, client_id: str, client_secret: str):
        channel = grpc.insecure_channel(host)
        auth_interceptor = client_authentication.ClientAuthenticationInterceptor(channel, client_id, client_secret)

        channel = grpc.intercept_channel(channel, auth_interceptor)
        self.stub = authz_grpc.ApiStub(channel)
