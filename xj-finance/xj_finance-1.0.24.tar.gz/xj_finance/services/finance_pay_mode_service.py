import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response

from ..models import PayMode


class FinancePayModeService:

    @staticmethod
    def get():
        currencies = PayMode.objects.all().annotate(value=F('pay_value'))

        return list(currencies.values('id', 'value', 'pay_mode'))

    @staticmethod
    def post(params):
        pay_mode = params.get('pay_mode', '')
        pay_value = params.get('value', '')
        if pay_mode:
            pay_mode_set = PayMode.objects.filter(pay_mode=pay_mode).first()
            if pay_mode_set is not None:
                return None, "pay_mode已存在"
        try:
            PayMode.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def put(params):
        pay = {}
        id = params.get('id', '')
        pay_mode = params.get('pay_mode', '')
        if pay_mode:
            pay['pay_mode'] = pay_mode
        if pay_mode:
            pay['pay_value'] = params.get('value', '')
        pay_mode_set = PayMode.objects.filter(id=id).first()
        if pay_mode_set is None:
            return None, "数据不存在"
        try:
            PayMode.objects.filter(id=id).update(**pay)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
