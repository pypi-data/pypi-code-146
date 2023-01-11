# _*_coding:utf-8_*_

import os, logging, time, json, copy
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from xj_user.services.user_service import UserService

from ..utils.model_handle import parse_data, util_response
from ..services.finance_statistic_service import FinanceStatisticService

logger = logging.getLogger(__name__)


class FinanceStatistic(generics.UpdateAPIView):  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    # serializer_class = FinanceTransactsSerializer
    params = None  # 请求体的原始参数

    print("-" * 30, os.path.basename(__file__), "-" * 30)

    def get(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return util_response(err=4001, msg='缺少Token')

        data, err_txt = UserService.check_token(token)
        if not data:
            return util_response(err=4002, msg=err_txt)
        params = parse_data(request)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': FinanceStatisticService.get(params, data['user_id'])
        })


