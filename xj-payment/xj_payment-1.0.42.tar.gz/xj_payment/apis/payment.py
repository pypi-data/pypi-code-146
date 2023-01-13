from django.http import JsonResponse
from rest_framework.views import APIView

from xj_payment.services.payment_service import PaymentService
from xj_user.services.user_service import UserService
from ..utils.model_handle import parse_data, util_response


class Payment(APIView):

    def get(self):
        # ========== 一、验证权限 ==========

        token = self.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return util_response(err=4001, msg='缺少Token')

        data, err_txt = UserService.check_token(token)
        if err_txt:
            return util_response(err=47766, msg=err_txt)
        params = parse_data(self)
        params['user_id'] = data['user_id']
        data, err_txt = PaymentService.get(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': data
        })

    def pay(self):
        params = parse_data(self)
        payment = PaymentService.pay(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            "data": payment
        })

    def refund(self):
        params = parse_data(self)
        payment = PaymentService.refund(params)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            "data": payment
        })
