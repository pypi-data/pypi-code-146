from django.shortcuts import redirect
from zeep import Client

from django_payment_gateways.exceptions import PurchaseFailedException, InvalidPaymentException
from django_payment_gateways.modules.abstracts import Driver, Receipt
from django_payment_gateways.modules.invoice import Invoice


class Normal(Driver):
    _invoice: Invoice
    _settings: dict

    def __init__(self, invoice: Invoice, settings: dict):
        self._invoice = invoice
        self._settings = settings

    def purchase(self) -> str:
        data = {
            "LoginAccount": self._settings.get("merchantId"),
            "Amount": self._invoice.amount * 10,
            "AdditionalData": self._invoice.get_detail("description") or self._settings.get("description"),
            "OrderId": self._invoice.get_uuid(),
            "CallBackUrl": self._settings.get("callbackUrl")
        }

        result = self._get_client(self.get_purchase_url()).service.SalePaymentRequest(requestData=data)
        token = result.Token
        status = int(result.Status)

        if token and status == 0:
            self._invoice.set_transaction_id(token)
            print(token)
            return self._invoice.transaction_id
        else:
            message = self.translate_status(str(status))
            raise PurchaseFailedException(message, str(status))

    def pay(self):
        transaction_id = self._invoice.transaction_id
        payment_url = self.get_payment_url()
        pay_url = f'{payment_url}?Token={transaction_id}'
        return redirect(pay_url)

    def verify(self, request):
        status = int(request.POST.get('status'))
        token = self._invoice.transaction_id or request.POST.get('Token')

        if status != 0 or not token:
            raise InvalidPaymentException('عملیات پرداخت توسط کاربر لغو شد.', status)

        data = {
            'LoginAccount': self._settings.get('merchantId'),
            'Token': token
        }
        result = self._get_client(self.get_verification_url()).service.ConfirmPayment(requestData=data)

        status = int(result.Status)
        rrn = str(result.RRN)
        if status == -138:
            raise InvalidPaymentException(
                "این تراکنش پرداخت شده بوده است"
            )

        if status != 0:
            message = self.translate_status(str(status))
            raise InvalidPaymentException(message, status)

        if status == 0:
            # successful
            return self.create_receipt(rrn)
        else:
            message = self.translate_status(str(status))
            raise InvalidPaymentException(message, status)

    def get_purchase_url(self) -> str:
        return self._settings.get('apiPurchaseUrl')

    def get_payment_url(self) -> str:
        return self._settings.get('apiPaymentUrl')

    def get_verification_url(self) -> str:
        return self._settings.get('apiVerificationUrl')

    def _get_client(self, url: str):
        return Client(url)

    def translate_status(self, status: str) -> str:
        translations = {
            "-32768": "UnknownError",
            "-1552": "PaymentRequestIsNotEligibleToReversal",
            "-1551": "PaymentRequestIsAlreadyReversed",
            "-1550": "PaymentRequestStatusIsNotReversible",
            "-1549": "MaxAllowedTimeToReversalHasExceeded",
            "-1548": "BillPaymentRequestServiceFailed",
            "-1540": "InvalidConfirmRequestService",
            "-1536": "TopupChargeServiceTopupChargeRequestFailed",
            "-1533": "PaymentIsAlreadyConfirmed",
            "-1532": "MerchantHasConfirmedPaymentRequest",
            "-1531": "CannotConfirmNonSuccessfulPayment",
            "-1530": "MerchantConfirmPaymentRequestAccessViolated",
            "-1528": "ConfirmPaymentRequestInfoNotFound",
            "-1527": "CallSalePaymentRequestServiceFailed",
            "-1507": "ReversalCompleted",
            "-1505": "PaymentConfirmRequested",
            "-138": "CanceledByUser",
            "-132": "InvalidMinimumPaymentAmount",
            "-131": "InvalidToken",
            "-130": "TokenIsExpired",
            "-128": "InvalidIpAddressFormat",
            "-127": "InvalidMerchantIp",
            "-126": "InvalidMerchantPin",
            "-121": "InvalidStringIsNumeric",
            "-120": "InvalidLength",
            "-119": "InvalidOrganizationId",
            "-118": "ValueIsNotNumeric",
            "-117": "LengthIsLessOfMinimum",
            "-116": "LengthIsMoreOfMaximum",
            "-115": "InvalidPayId",
            "-114": "InvalidBillId",
            "-113": "ValueIsNull",
            "-112": "OrderIdDuplicated",
            "-111": "InvalidMerchantMaxTransAmount",
            "-108": "ReverseIsNotEnabled",
            "-107": "AdviceIsNotEnabled",
            "-106": "ChargeIsNotEnabled",
            "-105": "TopupIsNotEnabled",
            "-104": "BillIsNotEnabled",
            "-103": "SaleIsNotEnabled",
            "-102": "ReverseSuccessful",
            "-101": "MerchantAuthenticationFailed",
            "-100": "MerchantIsNotActive",
            "-1": "Server Error",
            "0": "Successful",
            "1": "Refer To Card Issuer Decline",
            "2": "Refer To Card Issuer Special Conditions",
            "3": "Invalid Merchant",
            "5": "Do Not Honour",
            "6": "Error",
            "8": "Honour With Identification",
            "9": "Request In-progress",
            "10": "Approved For Partial Amount",
            "12": "Invalid Transaction",
            "13": "Invalid Amount",
            "14": "Invalid Card Number",
            "15": "No Such Issuer",
            "17": "Customer Cancellation",
            "20": "Invalid Response",
            "21": "No Action Taken",
            "22": "Suspected Malfunction",
            "30": "Format Error",
            "31": "Bank Not Supported By Switch",
            "32": "Completed Partially",
            "33": "Expired Card Pick Up",
            "38": "Allowable PIN Tries Exceeded Pick Up",
            "39": "No Credit Account",
            "40": "Requested Function is not supported",
            "41": "Lost Card",
            "43": "Stolen Card",
            "45": "Bill Can not Be Payed",
            "51": "No Sufficient Funds",
            "54": "Expired Account",
            "55": "Incorrect PIN",
            "56": "No Card Record",
            "57": "Transaction Not Permitted To CardHolder",
            "58": "Transaction Not Permitted To Terminal",
            "59": "Suspected Fraud-Decline",
            "61": "Exceeds Withdrawal Amount Limit",
            "62": "Restricted Card-Decline",
            "63": "Security Violation",
            "65": "Exceeds Withdrawal Frequency Limit",
            "68": "Response Received Too Late",
            "69": "Allowable Number Of PIN Tries Exceeded",
            "75": "PIN Reties Exceeds-Slm",
            "78": "Deactivated Card-Slm",
            "79": "Invalid Amount-Slm",
            "80": "Transaction Denied-Slm",
            "81": "Cancelled Card-Slm",
            "83": "Host Refuse-Slm",
            "84": "Issuer Down-Slm",
            "91": "Issuer Or Switch Is Inoperative",
            "92": "Not Found for Routing",
            "93": "Cannot Be Completed",
        }
        unknown_error = 'خطای ناشناخته رخ داده است.'
        return translations[status] if status in translations else unknown_error

    def create_receipt(self, reference_id: str) -> Receipt:
        return Receipt('parsian', reference_id)
