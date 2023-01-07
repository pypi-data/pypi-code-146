from ..apis.echo.v1.greeting_pb2 import Greeting
from ..apis.echo.v1.greeting_service_pb2 import CreateGreetingRequest
from ..apis.echo.v1.greeting_service_pb2 import CreateGreetingResponse
from ..apis.thirdparty.greeting.chat_pb2 import Chat
from ..apis.thirdparty.greeting.hello_pb2 import Hello
from ..gateway import echo_client
from ..gateway import try_request_grpc


class EchoClient:

    @staticmethod
    def echo():
        return "hello!"

    @property
    def _stub(self):
        """
        The function returns the client object
        :return: The client object
        """
        return echo_client

    @try_request_grpc
    def create_greeting(self, name: str, world: str) -> CreateGreetingResponse:
        return self._stub.greeting.CreateGreeting(
            CreateGreetingRequest(greeting=Greeting(
                greeted=world,
                chat=Chat(hello=Hello(name=name)),
            ), ), )
