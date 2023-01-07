import json
import re

from rhino_health.lib.rest_api.error_parsers.error_parser import ErrorParser

NESTED_MESSAGE_MATCHER = re.compile(r"Error getting [\w\s]+: ReverseRpcError: [\w]+@[\w\s]+: ")


class ReverseRPCErrorParser(ErrorParser):
    """
    Parses the nested reverse rpc errors and returns the underlying error
    """

    def parse(self, api_response):
        try:
            response_data = api_response.raw_response.json()["data"]
            nested_cohort_response = NESTED_MESSAGE_MATCHER.sub("", response_data)
            error_data = json.loads(nested_cohort_response)
            return error_data.get("message", error_data)
        except:
            return None
