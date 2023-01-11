import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response

from ..models import SandBox


class FinanceSandBoxService:

    @staticmethod
    def get():
        currencies = SandBox.objects.all().annotate(value=F('sand_box_name'), sand_box=F('sand_box_name'))

        return list(currencies.values('value', 'sand_box', 'sand_box_name'))

    @staticmethod
    def post(params):
        sand_box_name = params.get('sand_box_name', '')
        if sand_box_name:
            sand_box_set = SandBox.objects.filter(sand_box_name=sand_box_name).first()
            if sand_box_set is not None:
                return None, "sand_box_name已存在"
        try:
            SandBox.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
