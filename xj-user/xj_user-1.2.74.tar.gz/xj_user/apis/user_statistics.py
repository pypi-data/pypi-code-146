# encoding: utf-8
"""
@project: djangoModel->user_statistics
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户统计API
@created_time: 2022/11/3 10:48
"""
from rest_framework.views import APIView

from ..services.user_statistics_service import UserStatisticsService
from ..utils.custom_response import util_response


class UserStatisticsAPI(APIView):
    def get(self, request):
        data, err = UserStatisticsService.user_statistics()
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
