from test.lib.rhino_session_factory import RhinoSessionFactory

import factory

from rhino_health.lib.rest_api.api_response import APIResponse


class MockApiResponse(APIResponse):
    def __init__(self, json_response, status_code, *args, **kwargs):
        self.status_code = status_code
        super(MockApiResponse, self).__init__(*args, **kwargs)
        self.json_response = json_response

    @property
    def raw_response(self):
        return self

    @raw_response.setter
    def raw_response(self, value):
        if value:
            self.json_response = value

    def json(self):
        return self.json_response


class ApiResponseFactory(factory.Factory):
    class Meta:
        model = MockApiResponse
        inline_args = ("json_response",)
        strategy = factory.BUILD_STRATEGY

    status_code = 200
    json_response = ""
    session = factory.SubFactory(RhinoSessionFactory)
    request_response = None
    api_request = factory.StubFactory()  # TODO: Factory
