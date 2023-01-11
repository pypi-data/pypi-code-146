import time
import grpc
import authz_sdk.api_pb2 as api_pb2
import authz_sdk.api_pb2_grpc as api_pb2_grpc

class ClientAuthenticationInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, channel: grpc.Channel, client_id: str, client_secret: str):
        self.channel = channel
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

        self.stub = api_pb2_grpc.ApiStub(channel)

    def authenticate(self):
        request = api_pb2.AuthenticateRequest(client_id=self.client_id, client_secret=self.client_secret)
        response = self.stub.Authenticate(request)

        self.token = response.token
        self.expiration_time = int(time.time()) + response.expires_in

        return self.token

    def intercept_unary_unary(self, continuation, client_call_details, request):
        if not self.token or self.expiration_time < int(time.time()):
            self.authenticate()

        request_metadata = [('authorization', f"Bearer {self.token}")]

        client_call_details = client_call_details._replace(metadata=request_metadata)
        response = continuation(client_call_details, request)

        return response