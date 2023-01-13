import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response

from ..models import PaymentType


class FinancePaymentTypeService:

    @staticmethod
    def get():
        currencies = PaymentType.objects.all()

        return list(currencies.values('id', 'finance_payment_type', 'description'))

    @staticmethod
    def post(params):
        finance_payment_type = params.get('finance_payment_type', '')
        if finance_payment_type:
            sand_box_set = PaymentType.objects.filter(finance_payment_type=finance_payment_type).first()
            if sand_box_set is not None:
                return None, "finance_payment_type 已存在"
        try:
            PaymentType.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
