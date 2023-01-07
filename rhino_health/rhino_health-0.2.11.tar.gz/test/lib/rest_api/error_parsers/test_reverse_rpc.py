import json
from test.lib.rest_api.api_response_factory import ApiResponseFactory

import pytest

from rhino_health.lib.rest_api.error_parsers.reverse_rpc import ReverseRPCErrorParser


class TestReverseRpc:
    def test_nested_error(self):
        parser = ReverseRPCErrorParser()
        expected_error_message = "My Error Message"
        nested_json = json.dumps({"message": expected_error_message})
        api_response = ApiResponseFactory.build(
            json_response={
                "data": f"Error getting cohort metrics: ReverseRpcError: GetCohortMetric@RhinoHealthTest: {nested_json}"
            },
            status_code=400,
        )
        error_message = parser.parse(api_response)
        assert error_message == expected_error_message

    def test_unrelated_error(self):
        parser = ReverseRPCErrorParser()
        api_response = ApiResponseFactory.build(json_response="Unrelated Error", status_code=401)
        error_message = parser.parse(api_response)
        assert error_message is None
