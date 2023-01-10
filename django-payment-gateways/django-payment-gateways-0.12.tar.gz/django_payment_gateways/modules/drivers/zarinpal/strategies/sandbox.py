from django.shortcuts import redirect
from zeep import Client

from django_payment_gateways.exceptions import PurchaseFailedException, InvalidPaymentException
from django_payment_gateways.modules.abstracts.driver import Driver
from django_payment_gateways.modules.abstracts.receipt import Receipt
from django_payment_gateways.modules.invoice import Invoice


class Sandbox(Driver):
    _invoice: Invoice
    _settings: dict

    def __init__(self, invoice: Invoice, settings: dict):
        self._invoice = invoice
        self._settings = settings

    def purchase(self) -> str:
        data = {
            'MerchantID': self._settings.get('merchantId'),
            'Amount': self._invoice.amount,
            'Description': self._invoice.get_detail('description') or self._settings.get('description'),
            'Mobile': self._invoice.get_detail('mobile') or self._settings.get('mobile'),
            'Email': self._invoice.get_detail('email') or self._settings.get('email'),
            'CallbackURL': self._settings.get('callbackUrl'),
        }
        result = self._get_client(self.get_purchase_url()).service.PaymentRequest(**data)

        if result.Status != 100 or not result.Authority:
            message = self.translate_status(result.Status)
            raise PurchaseFailedException(message, result.Status)

        self._invoice.set_transaction_id(result.Authority)
        return self._invoice.transaction_id

    def pay(self):
        transaction_id = self._invoice.transaction_id
        payment_url = self.get_payment_url()
        pay_url = payment_url + transaction_id
        return redirect(pay_url)

    def verify(self, request):
        status = request.GET.get('Status')
        if status != 'OK':
            raise InvalidPaymentException('عملیات پرداخت توسط کاربر لغو شد.', -22)

        authority = self._invoice.transaction_id or request.GET.get('Authority')

        data = {
            'MerchantID': self._settings.get('merchantId'),
            'Authority': authority,
            'Amount': self._invoice.amount,
        }
        result = self._get_client(self.get_verification_url()).service.PaymentVerification(**data)

        if result.Status != 100:
            message = self.translate_status(result.Status)
            raise InvalidPaymentException(message, result.Status)

        return self.create_receipt(result.RefID)

    def get_purchase_url(self) -> str:
        return self._settings.get('sandboxApiPurchaseUrl')

    def get_payment_url(self) -> str:
        return self._settings.get('sandboxApiPaymentUrl')

    def get_verification_url(self) -> str:
        return self._settings.get('sandboxApiVerificationUrl')

    def _get_client(self, url: str):
        return Client(url)

    def translate_status(self, status: str) -> str:
        translations = {
            "-1": "اطلاعات ارسال شده ناقص است.",
            "-2": "IP و يا مرچنت كد پذيرنده صحيح نيست",
            "-3": "با توجه به محدوديت هاي شاپرك امكان پرداخت با رقم درخواست شده ميسر نمي باشد",
            "-4": "سطح تاييد پذيرنده پايين تر از سطح نقره اي است.",
            "-11": "درخواست مورد نظر يافت نشد.",
            "-12": "امكان ويرايش درخواست ميسر نمي باشد.",
            "-21": "هيچ نوع عمليات مالي براي اين تراكنش يافت نشد",
            "-22": "تراكنش نا موفق ميباشد",
            "-33": "رقم تراكنش با رقم پرداخت شده مطابقت ندارد",
            "-34": "سقف تقسيم تراكنش از لحاظ تعداد يا رقم عبور نموده است",
            "-40": "اجازه دسترسي به متد مربوطه وجود ندارد.",
            "-41": "اطلاعات ارسال شده مربوط به AdditionalData غيرمعتبر ميباشد.",
            "-42": "مدت زمان معتبر طول عمر شناسه پرداخت بايد بين 30 دقيه تا 45 روز مي باشد.",
            "-54": "درخواست مورد نظر آرشيو شده است",
            "101": "عمليات پرداخت موفق بوده و قبلا PaymentVerification تراكنش انجام شده است.",
        }
        unknown_error = 'خطای ناشناخته رخ داده است.'
        return translations[status] if status in translations else unknown_error

    def create_receipt(self, reference_id: str) -> Receipt:
        return Receipt('zarinpal', reference_id)
