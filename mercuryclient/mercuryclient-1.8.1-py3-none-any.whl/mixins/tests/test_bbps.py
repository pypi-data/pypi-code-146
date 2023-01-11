from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi
from mercuryclient.types.bbps.request import (
    AgentRequest,
    BillPaymentRequest,
    BillPaymentRequestTransid,
    ComplaintStatusRequest,
    GetAmountRequest,
    ServiceComplaintRequest,
    TxnComplaintRequest,
)


class BbpsTest(TestCase):
    def setUp(self):
        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_agent_onboard(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = AgentRequest(
            name="random",
            contactperson="random",
            mobileNumber="9999999999",
            agentshopname="random",
            businesstype="KIRANA_SHOP",
            address1="random address",
            address2="random address",
            state="random",
            city="random",
            pincode="123432",
            latitude="random",
            longitude="random",
            email="some@ramdom.com",
        )
        request_dict = {
            "name": "random",
            "contactperson": "random",
            "mobileNumber": "9999999999",
            "agentshopname": "random",
            "businesstype": "KIRANA_SHOP",
            "address1": "random address",
            "address2": "random address",
            "state": "random",
            "city": "random",
            "pincode": "123432",
            "latitude": "random",
            "longitude": "random",
            "email": "some@ramdom.com",
            "profile": "some_profile",
        }
        self.client.set_agent_on_board(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/agent/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_agent_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = AgentRequest(
            name="random",
            contactperson="random",
            mobileNumber="9999999999",
            agentshopname="random",
            businesstype="KIRANA_SHOP",
            address1="random address",
            address2="random address",
            state="random",
            city="random",
            pincode="123432",
            latitude="random",
            longitude="random",
            email="some@ramdom.com",
        )
        with self.assertRaises(Exception):
            self.client.set_agent_on_board(request_obj, "some_profile")

    def test_agent_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = AgentRequest(
            name="random",
            contactperson="random",
            mobileNumber="9999999999",
            agentshopname="random",
            businesstype="KIRANA_SHOP",
            address1="random address",
            address2="random address",
            state="random",
            city="random",
            pincode="123432",
            latitude="random",
            longitude="random",
            email="some@ramdom.com",
        )
        request_id = self.client.set_agent_on_board(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_bill_categories_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"coverage": "IND"}
        request_dict = {"coverage": "IND", "profile": "some_profile"}
        self.client.get_bill_categories(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/bill_categories/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_bill_categories_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"coverage": "IND"}
        with self.assertRaises(Exception):
            self.client.get_bill_categories(request_obj, "some_profile")

    def test_bill_categories_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"coverage": "IND"}
        request_id = self.client.get_bill_categories(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_biller_by_categories_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"categoryId": "3"}
        request_dict = {"categoryId": "3", "profile": "some_profile"}
        self.client.get_biller_by_categories(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/biller/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_biller_by_categories_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"categoryId": "3"}
        with self.assertRaises(Exception):
            self.client.get_biller_by_categories(request_obj, "some_profile")

    def test_biller_by_categories_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"categoryId": "3"}
        request_id = self.client.get_biller_by_categories(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_customer_params_by_biller_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"billerId": "MAHA00000MAH01"}
        request_dict = {"billerId": "MAHA00000MAH01", "profile": "some_profile"}
        self.client.get_customer_params_by_biller_id(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/customer_by_biller/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_customer_params_by_biller_request_exception_raised_if_status_code_error(
        self,
    ):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"billerId": "MAHA00000MAH01"}
        with self.assertRaises(Exception):
            self.client.get_customer_params_by_biller_id(request_obj, "some_profile")

    def test_customer_params_by_biller_request_api_succeeds_if_status_code_success(
        self,
    ):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"billerId": "MAHA00000MAH01"}
        request_id = self.client.get_customer_params_by_biller_id(
            request_obj, "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")

    def test_get_amount_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = GetAmountRequest(
            billerId="random",
            mobileNumber="9999999999",
            crno="random",
            agentId="random",
        )
        request_dict = {
            "billerId": "random",
            "mobileNumber": "9999999999",
            "crno": "random",
            "agentId": "random",
            "profile": "some_profile",
        }
        self.client.get_amount(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/amount/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_get_amount_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = GetAmountRequest(
            billerId="random",
            mobileNumber="9999999999",
            crno="random",
            agentId="random",
        )
        with self.assertRaises(Exception):
            self.client.get_amount(request_obj, "some_profile")

    def test_get_amount_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = GetAmountRequest(
            billerId="random",
            mobileNumber="9999999999",
            crno="random",
            agentId="random",
        )
        request_id = self.client.get_amount(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_bill_payment_request_transid_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = BillPaymentRequestTransid(
            billAmount="random",
            transid="random",
            mobileNumber="9999999999",
            agentId="random",
            BillerCategory="random",
            billerId="random",
            crno="random",
        )
        request_dict = {
            "billAmount": "random",
            "transid": "random",
            "mobileNumber": "9999999999",
            "agentId": "random",
            "BillerCategory": "random",
            "billerId": "random",
            "crno": "random",
            "profile": "some_profile",
        }
        self.client.send_bill_payment_request_transid(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/payment_transid/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_bill_payment_request_transid_request_exception_raised_if_status_code_error(
        self,
    ):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = BillPaymentRequestTransid(
            billAmount="random",
            transid="random",
            mobileNumber="9999999999",
            agentId="random",
            BillerCategory="random",
            billerId="random",
            crno="random",
        )
        with self.assertRaises(Exception):
            self.client.send_bill_payment_request_transid(request_obj, "some_profile")

    def test_bill_payment_request_transid_request_api_succeeds_if_status_code_success(
        self,
    ):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = BillPaymentRequestTransid(
            billAmount="random",
            transid="random",
            mobileNumber="9999999999",
            agentId="random",
            BillerCategory="random",
            billerId="random",
            crno="random",
        )
        request_id = self.client.send_bill_payment_request_transid(
            request_obj, "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")

    def test_bill_payment_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = BillPaymentRequest(
            billAmount="random",
            mobileNumber="9999999999",
            agentId="random",
            BillerCategory="random",
            billerId="random",
            crno="random",
        )
        request_dict = {
            "billAmount": "random",
            "mobileNumber": "9999999999",
            "agentId": "random",
            "BillerCategory": "random",
            "billerId": "random",
            "crno": "random",
            "profile": "some_profile",
        }
        self.client.send_bill_payment_request(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/payment/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_bill_payment_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = BillPaymentRequest(
            billAmount="random",
            mobileNumber="9999999999",
            agentId="random",
            BillerCategory="random",
            billerId="random",
            crno="random",
        )
        with self.assertRaises(Exception):
            self.client.send_bill_payment_request(request_obj, "some_profile")

    def test_bill_payment_request_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = BillPaymentRequest(
            billAmount="random",
            mobileNumber="9999999999",
            agentId="random",
            BillerCategory="random",
            billerId="random",
            crno="random",
        )
        request_id = self.client.send_bill_payment_request(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_duplicate_payment_receipt_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"refId": "random"}
        request_dict = {"refId": "random", "profile": "some_profile"}
        self.client.get_duplicate_payment_receipt(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/payment_receipt/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_duplicate_payment_receipt_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"refId": "random"}
        with self.assertRaises(Exception):
            self.client.get_duplicate_payment_receipt(request_obj, "some_profile")

    def test_duplicate_payment_receipt_request_api_succeeds_if_status_code_success(
        self,
    ):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = {"refId": "random"}
        request_id = self.client.get_duplicate_payment_receipt(
            request_obj, "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")

    def test_trasaction_complaint_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = TxnComplaintRequest(
            transactionRefId="random",
            mobileNumber="1111111111",
            reason="random",
            description="random",
        )
        request_dict = {
            "transactionRefId": "random",
            "mobileNumber": "1111111111",
            "reason": "random",
            "description": "random",
            "profile": "some_profile",
        }
        self.client.register_trasaction_complaint(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/trasaction_complaint/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_trasaction_complaint_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = TxnComplaintRequest(
            transactionRefId="random",
            mobileNumber="1111111111",
            reason="random",
            description="random",
        )
        with self.assertRaises(Exception):
            self.client.register_trasaction_complaint(request_obj, "some_profile")

    def test_trasaction_complaint_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = TxnComplaintRequest(
            transactionRefId="random",
            mobileNumber="1111111111",
            reason="random",
            description="random",
        )
        request_id = self.client.register_trasaction_complaint(
            request_obj, "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")

    def test_service_complaint_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = ServiceComplaintRequest(
            billerId="random",
            mobileNumber="1111111111",
            description="random",
            reason="random",
            type="random",
        )
        request_dict = {
            "billerId": "random",
            "mobileNumber": "1111111111",
            "description": "random",
            "reason": "random",
            "type": "random",
            "profile": "some_profile",
        }
        self.client.register_service_complaint(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/service_complaint/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_service_complaint_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = ServiceComplaintRequest(
            billerId="random",
            mobileNumber="1111111111",
            description="random",
            reason="random",
            type="random",
        )
        with self.assertRaises(Exception):
            self.client.register_service_complaint(request_obj, "some_profile")

    def test_service_complaint_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = ServiceComplaintRequest(
            billerId="random",
            mobileNumber="1111111111",
            description="random",
            reason="random",
            type="random",
        )
        request_id = self.client.register_service_complaint(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_send_complaint_status_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = ComplaintStatusRequest(
            complaintType="Service", complaintId="random"
        )
        request_dict = {
            "complaintType": "Service",
            "complaintId": "random",
            "profile": "some_profile",
        }
        self.client.get_complaint_status(request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/complaint_status/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_complaint_status_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = ComplaintStatusRequest(
            complaintType="Service", complaintId="random"
        )
        with self.assertRaises(Exception):
            self.client.get_complaint_status(request_obj, "some_profile")

    def test_complaint_status_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_obj = ComplaintStatusRequest(
            complaintType="Service", complaintId="random"
        )
        request_id = self.client.get_complaint_status(request_obj, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")

    def test_get_bbpsid_request(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_dict = {"profile": "some_profile"}
        self.client.get_bbpsid("some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/bbps/bbpsid/",
            data=request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_get_bbpsid_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.get_bbpsid("some_profile")

    def test_get_bbpsid_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_id = self.client.get_bbpsid("some_profile")
        self.assertEqual(request_id["request_id"], "random_string")
