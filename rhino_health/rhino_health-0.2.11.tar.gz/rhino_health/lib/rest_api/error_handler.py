from rhino_health.lib.rest_api.api_request import APIRequest
from rhino_health.lib.rest_api.api_response import APIResponse
from rhino_health.lib.rest_api.request_adapter import RequestAdapter


class ErrorHandler(RequestAdapter):
    """
    Simple check to see if our request failed or succeeded.
    You can define custom acceptable status codes per api request call via adapter_kwargs
    """

    DEFAULT_ACCEPTED_STATUS_CODES = [200, 201]

    def after_request(
        self, api_request: APIRequest, api_response: APIResponse, adapter_kwargs: dict
    ):
        if api_request.request_status != APIRequest.RequestStatus.PENDING:
            # Some other adapter handled already
            return
        valid_status_codes = adapter_kwargs.get(
            "accepted_status_codes", self.DEFAULT_ACCEPTED_STATUS_CODES
        )
        if api_response.status_code not in valid_status_codes:
            api_request.request_status = APIRequest.RequestStatus.FAILED
        else:
            api_request.request_status = APIRequest.RequestStatus.SUCCESS
