class GstVerifyMixin:
    """
    Mixin for gst verification
    """

    def verify_gstin(self, gstin_number: str, provider: str, profile: str):
        """
        gstin verification using the mercury service

        :param request_obj: GstVerifyRequest
        :param provider: any
        :param profile: An existing profile in Mercury. The profile has to correspond
        to the provider.
        :return: (request_id, data)
        """
        api = "api/v1/gst_verification/"

        request_dict = {
            "profile": profile,
            "provider": provider,
            "gstin_number": gstin_number,
        }

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        try:
            response_json = r.json()
        except Exception:
            response_json = {}

        if r.status_code == 201:
            return {"request_id": request_id, "data": response_json}

        raise Exception(
            "Error while sending gstin verify request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_verify_gst_result(self, request_id: str):
        api = "api/v1/gst_verification/"

        request_id, r = self._get_json_http_request(
            api,
            headers={"X-Mercury-Request-Id": request_id},
            send_request_id=False,
            add_bearer_token=True,
        )

        if r.status_code == 200:
            result = r.json()
            if result["status"] == "FAILURE":
                raise Exception(
                    "Error verifying Gst. Status: {} | Message {}".format(
                        result["status"], result["message"]
                    )
                )
            return request_id, result

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error getting Gst Verification result. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
