import json
from mercuryclient.types.bbps.request import (
    AgentRequest,
    BillPaymentRequest,
    BillPaymentRequestTransid,
    ComplaintStatusRequest,
    GetAmountRequest,
    ServiceComplaintRequest,
    TxnComplaintRequest,
)


class BbpsMixin:
    def set_agent_on_board(self, request_obj: AgentRequest, profile: str):
        """
        Create Agent using the mercury service

        :param: request_obj: AgentRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/agent/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Agent Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_state(self, profile: str):
        """
        Ftech state using the mercury service

        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/state/"

        request_dict = {}
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Status Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_district_by_state(self, request_obj: dict, profile: str):
        """
        Fetch Status  using the mercury service

        :param: request_obj: dict
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/distrct/"

        request_dict = request_obj
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending District Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_bill_categories(self, request_obj: dict, profile: str):
        """
        Ftech Bill Categories  using the mercury service

        :param: request_obj: dict
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/bill_categories/"

        request_dict = request_obj
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending bill categories Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_biller_by_categories(self, request_obj: dict, profile: str):
        """
        Fetch billers using the mercury service

        :param: request_obj: dict
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/biller/"

        request_dict = request_obj
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Biller Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_customer_params_by_biller_id(self, request_obj: dict, profile: str):
        """
        Fetch customer params using the mercury service

        :param: request_obj: dict
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/customer_by_biller/"

        request_dict = request_obj
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending customer params Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_amount(self, request_obj: GetAmountRequest, profile: str):
        """
        Fetching Amount  using the mercury service

        :param: request_obj: GetAmountRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/amount/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending get amount Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def send_bill_payment_request_transid(
        self, request_obj: BillPaymentRequestTransid, profile: str
    ):
        """
        Bill payment with trans id using the mercury service

        :param: request_obj: BillPaymentRequestTransid
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/payment_transid/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Bbps Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def send_bill_payment_request(self, request_obj: BillPaymentRequest, profile: str):
        """
        Send bill payment using the mercury service

        :param: request_obj: BillPaymentRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/payment/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending bill payment Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_duplicate_payment_receipt(self, request_obj: dict, profile: str):
        """
        Fetch duplicate receipt using the mercury service

        :param: request_obj: Dict
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/payment_receipt/"

        request_dict = request_obj
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while fetching duplicate receipt Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def register_trasaction_complaint(
        self, request_obj: TxnComplaintRequest, profile: str
    ):
        """
        Register trasaction complaint using the mercury service

        :param: request_obj: TxnComplaintRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/trasaction_complaint/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending trasaction complaint Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def register_service_complaint(
        self, request_obj: ServiceComplaintRequest, profile: str
    ):
        """
        Service complaint using the mercury service

        :param: request_obj: ServiceComplaintRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/service_complaint/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Service complaint Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_complaint_status(self, request_obj: ComplaintStatusRequest, profile: str):
        """
        Fetch complaint status using the mercury service

        :param: request_obj: ComplaintStatusRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/complaint_status/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending Complaint Status Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_bbpsid(self, profile: str):
        """
        Fetch bbps id  using the mercury service

        :param profile: An existing profile in Mercury.
        :return: (request_id, status,data )
        """

        api = "api/v1/bbps/bbpsid/"

        request_dict = {}
        request_dict["profile"] = profile

        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:

            return {"request_id": request_id, "data": r.content}

        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending bbps id Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
