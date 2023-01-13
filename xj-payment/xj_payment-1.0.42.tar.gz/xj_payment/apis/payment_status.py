from django.http import JsonResponse
from rest_framework.views import APIView

from utils.custom_response import util_response
from utils.custom_tool import parse_data
from ..services.payment_satus_service import PaymentStatusService


class PaymentStatus(APIView):
    def get(self, request, *args, **kwargs):
        params = parse_data(request)
        data, err_txt = PaymentStatusService.get(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
            'data': data
        })

    def post(self, request, *args, **kwargs):
        params = parse_data(request)
        data, err_txt = PaymentStatusService.post(params)
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return JsonResponse({
            'err': 0,
            'msg': 'OK',
        })
