from requests import PreparedRequest, Session

from semantha_sdk.response.SemanthaPlatformResponse import SemanthaPlatformResponse


class SemanthaRequest:

    def __init__(self, prepared_request: PreparedRequest):
        self.__prepared_request = prepared_request

    def execute(self) -> SemanthaPlatformResponse:
        with (Session()) as session:
            response = session.send(self.__prepared_request)
            return SemanthaPlatformResponse(response)

    def execute_async(self) -> SemanthaPlatformResponse:
        pass
