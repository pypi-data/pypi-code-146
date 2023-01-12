# encoding: utf-8
"""
@project: djangoModel->enroll_statistics
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 统计接口
@created_time: 2022/10/31 11:07
"""
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_user.utils.user_wrapper import user_authentication_force_wrapper
from ..service.enroll_statistics_service import EnrollStatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class EnrollStatisticsAPI(APIView):
    @require_http_methods(['GET'])
    @request_params_wrapper
    def statistics(self, *args, request_params=None, **kwargs):
        data, err = EnrollStatisticsService.statistics_by_day()
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    @user_authentication_force_wrapper
    def statistics_by_user(self, *args, user_info=None, **kwargs):
        if user_info is None:
            user_info = {}
        user_id = user_info.get("user_id")
        data, err = EnrollStatisticsService.statistics_by_user(user_id)
        finance_res, err = FinanceTransactService.get_finance_by_user(user_id)
        if err:
            return util_response(err=1000, msg=err)
        data["balance"] = round(float(finance_res.get("balance", 0)), 2) if finance_res else 0
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)
