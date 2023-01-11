from django.http import JsonResponse
from rest_framework.views import APIView

from xj_payment.utils.utils_v1 import my_ali_pay


class query(APIView):

    def refund_inquiry(self):
        """
         退款查询接口
         :param request:
          :return:
          """
        if self.method == "GET":
            out_trade_no = self.GET.get('out_trade_no')
            trade_no = self.GET.get('trade_no')
            alipay = my_ali_pay()
            order_string = alipay.api_alipay_trade_fastpay_refund_query(
                trade_no=str(trade_no),
                out_request_no=str(out_trade_no),
            )
            return JsonResponse(order_string)

    def trade_query(self):
        """
        支付查询接口
        :param request:
         :return:
          """
        if self.method == "GET":
            out_trade_no = self.GET.get('out_trade_no')
            trade_no = self.GET.get('trade_no')
            alipay = my_ali_pay()
            order_string = alipay.api_alipay_trade_query(
                trade_no=str(trade_no),
                out_trade_no=str(out_trade_no),
            )
            return JsonResponse(order_string)
