import json
from mercuryclient.types.bank_account_verify.request import AccountVerifyRequest


class AccountVerifyMixin:
    """
    Mixin for bank account verification
    """

    def verify_bank_account(
        self, request_obj: AccountVerifyRequest, provider: str, profile: str
    ):
        """
        bank account verification using the mercury service

        :param request_obj: AccountVerifyRequest
        :param provider: cashfree
        :param profile: An existing profile in Mercury. The profile has to correspond
        to the provider.
        :return: (request_id, data)
        """
        api = "api/v1/account_verify/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile
        request_dict["provider"] = provider

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
            "Error while sending account verify request. Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
