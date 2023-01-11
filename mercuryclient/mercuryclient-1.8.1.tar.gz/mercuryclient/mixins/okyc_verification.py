import time
from typing import Tuple

from mercuryclient.types.okyc_verification.enums import RequestTypes


class OkycVerificationMixin:
    """
    Mixin for verifying Okyc
    """

    def initiate_okyc_request(
        self,
        request_data,
    ) -> str:
        api = "api/v1/okyc_verification/"
        try:
            RequestTypes(request_data.get("request_type"))
        except ValueError:
            raise Exception(
                f"{request_data.get('request_type')} is not a valid request_type"
            )

        request_id, r = self._post_json_http_request(
            api, data=request_data, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:
            return request_id

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Okyc verification request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_okyc_response(self, request_id: str) -> Tuple[str, dict]:
        api = "api/v1/okyc_verification/"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            result = r.json()
            return request_id, result

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error getting Okyc Verification result. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_okyc_result(
        self, mercury_request_id: str, max_attempts: int, retry_backoff: int
    ):
        """Retry mechanism for okyc response

        raises:
            Exception: After max attempts, response till remains in progress

        returns mercury_request_id,response from the vendor

        """

        for attempts in range(max_attempts):
            time.sleep(retry_backoff)
            mercury_request_id, result = self.get_okyc_response(mercury_request_id)
            if result.get("status") != "IN_PROGRESS":
                return mercury_request_id, result

            retry_backoff *= 2

        raise Exception("Error while getting Okyc response. Status: IN_PROGRESS")

    def generate_okyc_otp(
        self,
        profile: str,
        provider: str,
        id_number: str,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Initiates the request for okyc otp generation.

        returns: mercury_request_id,otp generation response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "id_number": id_number,
            "request_type": "OTP_REQUEST",
        }
        mercury_request_id = self.initiate_okyc_request(request_data)
        return self.get_okyc_result(mercury_request_id, max_attempts, retry_backoff)

    def verify_okyc_otp(
        self,
        profile: str,
        provider: str,
        otp: str,
        otp_request_id: str,
        max_attempts: int = 3,
        retry_backoff: int = 5,
    ):
        """Get OTP from customer and verify with request_id.

        returns: mercury_request_id, verify okyc response from vendor
        """
        request_data = {
            "provider": provider,
            "profile": profile,
            "otp": otp,
            "request_id": otp_request_id,
            "request_type": "OTP_VERIFY",
        }
        mercury_request_id = self.initiate_okyc_request(request_data)
        return self.get_okyc_result(mercury_request_id, max_attempts, retry_backoff)
