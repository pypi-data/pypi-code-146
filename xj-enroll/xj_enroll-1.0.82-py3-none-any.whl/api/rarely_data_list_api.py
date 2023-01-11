# encoding: utf-8
"""
@project: djangoModel->statu_code_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/10/14 14:10
"""
from rest_framework.views import APIView

from ..models import EnrollStatusCode
from ..utils.custom_response import util_response


class OtherListAPIView(APIView):
    def enroll_status_code(self):
        res = list(EnrollStatusCode.objects.all().values())
        return util_response(data=res)
