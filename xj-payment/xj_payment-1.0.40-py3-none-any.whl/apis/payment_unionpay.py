from rest_framework.views import APIView
from ..services.payment_unionpay_service import PaymentUnionPayService


class PaymentUnionPay(APIView):
    def unipay(self):
        res = PaymentUnionPayService.unipay("200", "1")
        return res
