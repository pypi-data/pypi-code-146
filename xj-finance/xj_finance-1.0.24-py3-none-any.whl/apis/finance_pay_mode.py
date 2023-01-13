# _*_coding:utf-8_*_

import os, logging, time, json, copy
from rest_framework.response import Response
from rest_framework import generics

from ..utils.model_handle import parse_data, util_response
from ..services.finance_pay_mode_service import FinancePayModeService

logger = logging.getLogger(__name__)


# 获取支付方式
class FinancePayMode(generics.UpdateAPIView):  # 或继承(APIView)

    def get(self, request, *args, **kwargs):
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': FinancePayModeService.get()
        })

    # 支付方式添加
    def post(self, request, *args, **kwargs):
        params = parse_data(request)
        if not params:
            return util_response(err=6046, msg='至少需要一个请求参数')
        data, err_txt = FinancePayModeService.post(params=params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

        # 支付方式修改

    def put(self, request, *args, **kwargs):
        params = parse_data(request)
        if not params:
            return util_response(err=6046, msg='至少需要一个请求参数')
        data, err_txt = FinancePayModeService.put(params=params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
