# _*_coding:utf-8_*_

import os, logging, time, json, copy
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import response
from rest_framework import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from django.db.models import F

from ..models import *

logger = logging.getLogger(__name__)


# 获取支付方式
class FinanceCurrencyService:  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """

    @staticmethod
    def get():
        currencies = Currency.objects.all().annotate(value=F('currency'))

        return list(currencies.values('currency', 'value'))

    @staticmethod
    def post(params):
        currency = params.get('currency', '')
        if currency:
            currency_set = Currency.objects.filter(currency=currency).first()
            if currency_set is not None:
                return None, "currency已存在"
        try:
            Currency.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
