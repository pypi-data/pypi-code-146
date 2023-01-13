from urllib import parse

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils.model_handle import parse_data
from ..utils.custom_response import util_response
from ..services.payment_alipay_service import PaymentAlipayService


class PaymentAlipay(APIView):
    def get_pay_url(self):
        if self.method == "POST":
            money = self.POST.get('money', 0)  # 前端传回的金额
            out_trade_no = self.POST.get('out_trade_no', 0)
            params = {
                'money': money,
                'out_trade_no': out_trade_no
            }
            data, err_txt = PaymentAlipayService.get_pay_url(params, self)
            if not data:
                return util_response(err=47767, msg=err_txt)
            return JsonResponse({
                'err': 0,
                'msg': 'OK',
                'data': data
            })

    def pay_result(self):
        if self.method == "GET":
            data = self.GET.dict()
            data, err_txt = PaymentAlipayService.pay_result(data)
            if not data:
                return util_response(err=47767, msg=err_txt)
            return JsonResponse({
                'err': 0,
                'msg': 'OK',
                'data': data
            })

    def update_order(self):
        if self.method == "POST":
            print("异步通知验证开始")
            body_str = self.body.decode('utf-8')
            data = parse.parse_qs(body_str)
            PaymentAlipayService.update_order(data)
            return JsonResponse({
                'err': 0,
                'msg': 'OK',
            })

    def refund(self):
        
        if self.method == "POST":
            # 根据当前用户的配置，生成URL，并跳转。
            # print(self)
            money = (self.POST.get('price'))
            out_trade_no = self.POST.get('out_trade_no')
            params = {
                'money': money,
                'out_trade_no': out_trade_no
            }
            data, err_txt = PaymentAlipayService.refund(params, self)
            return JsonResponse({
                'err': 0,
                'msg': 'OK',
                'data': data
            })
