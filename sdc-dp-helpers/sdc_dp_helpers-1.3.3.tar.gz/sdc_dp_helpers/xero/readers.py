# pylint: disable=no-member,inconsistent-return-statements,wrong-import-order
import datetime
import os

# import ast
import json
import requests
from dateutil.relativedelta import relativedelta

from sdc_dp_helpers.api_utilities.retry_managers import request_handler
from sdc_dp_helpers.xero import auth_handler as pixie
from sdc_dp_helpers.xero.config_managers import get_config
from xero import Xero


def date_filter_helper(from_date: str, to_date: str, filter_field: str = None) -> str:
    """
    Custom implementation of date filters borrowed from:
    https://github.com/ClaimerApp/pyxero/blob/master/xero/basemanager.py
    """
    if not from_date:
        raise ValueError("No from_date set")

    # common date_field inside of the accounts and contacts modules is UpdatedDateUTC
    filter_field = "UpdatedDateUTC" if not filter_field else filter_field
    api_filter = filter_field + ">=DateTime(" + ",".join(from_date.split("-")) + ")"
    if to_date:
        api_filter = (
            api_filter
            + "&&"
            + filter_field
            + "<=DateTime("
            + ",".join(to_date.split("-"))
            + ")"
        )
    # end if

    return api_filter


class CustomXeroReader:
    """
    Custom Xero Reader
    """

    def __init__(self, **kwargs):
        self.config_path = kwargs.get("config_path")
        self.creds_path = kwargs.get("creds_path")
        self.config = get_config(self.config_path)
        three_months_back = (datetime.date.today() - relativedelta(months=3)).strftime(
            "%Y-%m-01"
        )
        today = datetime.date.today().strftime("%Y-%m-%d")

        self.config["from_date"] = self.config.get("start_date", three_months_back)
        self.config["to_date"] = self.config.get("end_date", today)
        self.from_date = None
        self.to_date = None

        self.client_id = self.config.get("client_id", None)
        if not self.client_id:
            raise ValueError("No client_id set")

        self.auth_token = pixie.get_auth_token(
            client_id=self.client_id, local_token_path=self.creds_path
        )

    def fetch_reports(self) -> dict:
        """
        Loops through reports in the config to pull each of them
        """
        data_set = {}
        for report_name in self.config.get("reports", []):
            if report_name not in [
                "BalanceSheet",
                "ProfitAndLoss",
                # "TrialBalance", #not pulling this atm
                "AgedPayablesByContact",
                "AgedReceivablesByContact",
            ]:
                raise ValueError(report_name + " is not supported or does not exist.")

            self.auth_token = pixie.get_auth_token(self.client_id, self.creds_path)

            self.auth_token.tenant_id = tenant_id = self.config.get("tenant_id")

            xero_obj = Xero(self.auth_token)
            trackingcategories = (
                i for i in xero_obj.trackingcategories.all() if i is not None
            )

            for tracking_category in trackingcategories:
                request_params = {
                    "report_name": report_name,
                    "tenant_id": tenant_id,
                    "tracking_category": tracking_category,
                    "xero_obj": xero_obj,
                    "auth_token": self.auth_token,
                    "from_date": self.config.get("from_date"),
                    "to_date": self.config.get("to_date"),
                }

                if report_name in ["BalanceSheet", "ProfitAndLoss"]:
                    result = self.fetch_report(request_params)
                    if result and result is not None:
                        data_set[
                            (
                                report_name
                                + "_"
                                + tracking_category["TrackingCategoryID"]
                            )
                        ] = result

                elif report_name in [
                    "AgedPayablesByContact",
                    "AgedReceivablesByContact",
                ]:

                    for contact in xero_obj.contacts.filter(
                        raw="AccountNumber!=null", AccountNumber__startswith="999999"
                    ):
                        print(contact["ContactID"])
                        request_params.update({"contactId": contact["ContactID"]})
                        # print(type(report_name),
                        # type(tracking_category["TrackingCategoryID"]), type(contact_id))

                        result = self.fetch_report(request_params)
                        if result and result is not None:
                            data_set[
                                (
                                    report_name
                                    + "_"
                                    + tracking_category["TrackingCategoryID"]
                                    + "_"
                                    + contact["ContactID"]
                                )
                            ] = result
                else:
                    raise ValueError(
                        f"Unknown report named '{report_name}'. Check your spelling maybe?"
                    )

        return data_set

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 0.1)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    def fetch_report(self, request_params: dict) -> str:
        """
        This method accepts Parameters
            report_name: report name as per Xero API endpoint
            from_date: start_date of the report
            to_date: end date of the report
            returns: report for those parameters using the requests API directly
        """
        # unpack request
        report_name = request_params["report_name"]

        today = datetime.date.today()
        three_months_back = (today - relativedelta(months=3)).strftime("%Y-%m-01")
        today = today.strftime("%Y-%m-%d")

        self.from_date = request_params.get(
            "from_date", request_params.get("date", three_months_back)
        )
        self.to_date = request_params.get("to_date", today)
        tracking_category = request_params["tracking_category"]

        self.auth_token = pixie.get_auth_token(
            client_id=self.client_id, local_token_path=self.creds_path
        )
        # self.auth_token.tenant_id = request['tenant_id']

        my_headers = {
            "Authorization": "Bearer "
            + self.auth_token.token[
                "access_token"
            ],  # self.xero_client.token["access_token"],
            "Xero-Tenant-Id": request_params["tenant_id"],
            "Accept": "application/json",
        }
        my_params = {
            "fromDate": self.from_date,
            "toDate": self.from_date,
        }
        if tracking_category:
            my_params.update(
                {"trackingCategoryID": tracking_category["TrackingCategoryID"]}
            )

        if "filter_items" in request_params.keys():
            my_params.update(request_params["filter_items"])

        if "contactId" in request_params.keys():
            my_params.update({"contactId": request_params["contactId"]})

        response = requests.get(
            "https://api.xero.com/api.xro/2.0/Reports/" + report_name,
            params=my_params,
            headers=my_headers,
            timeout=30,
        )
        # response.text = response.text.strip("'<>() ").replace('\'', '\"')
        # print(response.text)
        report = json.loads(
            response.text.replace("\r", "").replace("\n", "").strip("'<>() ")
        )
        report = {
            "tenantId": self.auth_token.tenant_id,
            "trackingCategoryId": tracking_category["TrackingCategoryID"],
            "report": report,
            "from_date": self.from_date,
            "to_date": self.from_date,
        }
        return json.dumps(report)

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 0.1)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    def run_request(self, xero_client, api_object, request):
        """
        Run the API request that consumes a request payload and site url.
        This separates the request with the request handler from the rest of the logic.
        """
        # To Do Handle API Errors
        api_call = getattr(xero_client, api_object)
        # XeroRateLimitExceeded
        return api_call.filter(
            raw=date_filter_helper(request["from_date"], request["to_date"]),
            page=request["page"],
        )

    def fetch_modules(self) -> dict:
        """
        Consumes a .yaml config file and loops through the date and url
        to return relevant data from Xero API.
        """
        self.auth_token = pixie.get_auth_token(self.client_id, self.creds_path)
        self.auth_token.tenant_id = [
            i["tenantId"]
            for i in self.auth_token.get_tenants()
            if i["tenantId"] == self.config["tenant_id"]
        ][0]
        xero = Xero(self.auth_token)

        today = datetime.date.today()
        three_months_back = (today - relativedelta(months=3)).strftime("%Y-%m-01")
        today = today.strftime("%Y-%m-%d")

        self.from_date = self.config.get("from_date", three_months_back)
        self.to_date = self.config.get("to_date", today)
        data_set = {}

        for api_object in self.config.get("modules", []):
            if api_object not in [
                "contacts",
                "accounts",
                "invoices",
                "banktransactions",
                "manualjournals",
                "purchaseorders",
            ]:
                raise ValueError(api_object + " is not supported or does not exist.")
            data_set[api_object] = []
            prev_response = None
            page = 1

            while True:
                response = self.run_request(
                    xero_client=xero,
                    api_object=api_object,
                    request={
                        "from_date": self.from_date,
                        "to_date": self.to_date,
                        "page": page,
                    },
                )
                if len(response) < 1:
                    print("Request returned empty payload. breaking...")
                    break
                if response == prev_response:
                    print("Request returned copy of last payload. breaking...")
                    break
                data_set[api_object] += [
                    # the response objects are returned as a dictionary with datetime.
                    # datetime objects,to convert to json type we ask json to attempt to
                    # convert all pythonic objects to something acceptable for a json object
                    # only thereafter can we convert back to json for saving to json file
                    json.loads(
                        json.dumps(response_obj, indent=4, sort_keys=True, default=str)
                    )
                    for response_obj in response
                ]

                # ensure the token is still fresh
                self.auth_token = pixie.get_auth_token(self.client_id, self.creds_path)
                prev_response = response
                page += 1
        return data_set

    def run_query(self):
        """
        As dictated by the config;
        This function fetches all modules and reports requested based on the config
        """
        if getattr(self.config, "modules", None):
            return self.fetch_modules()
        if getattr(self.config, "reports", None):
            return self.fetch_reports()
