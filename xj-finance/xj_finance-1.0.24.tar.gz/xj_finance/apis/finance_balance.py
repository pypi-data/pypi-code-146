# _*_coding:utf-8_*_

import os, logging, time, json, copy
from rest_framework.response import Response
from rest_framework import generics

from ..utils.model_handle import parse_data, util_response
from ..services.finance_service import FinanceService

logger = logging.getLogger(__name__)


# 获取余额
class FinanceBalance(generics.UpdateAPIView):  # 或继承(APIView)

    def get(self, request, *args, **kwargs):
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': FinanceService.check_balance(account_id='11', platform='muzpay', platform_id=None, currency='CNY',
                                                 sand_box='')
        })
