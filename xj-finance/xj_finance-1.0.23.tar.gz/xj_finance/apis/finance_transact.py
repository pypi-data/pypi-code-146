# _*_coding:utf-8_*_

import os, logging, time, json, copy, math
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from ..services.finance_transacts_service import FinanceTransactsService
from xj_user.services.user_service import UserService
from ..utils.model_handle import parse_data, util_response
from ..services.finance_transact_service import FinanceTransactService

logger = logging.getLogger(__name__)


#
class FinanceTransact(generics.UpdateAPIView):  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """

    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    # permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    # params = None  # 请求体的原始参数
    # serializer_params = None
    #
    # print("-" * 30, os.path.basename(__file__), "-" * 30)

    # 查询一条财务交易数据
    def get(self, request, *args, **kwargs):
        # ========== 一、验证权限 ==========

        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return util_response(err=4001, msg='缺少Token')

        data, err_txt = UserService.check_token(token)
        if err_txt:
            return util_response(err=47766, msg=err_txt)
        params = parse_data(request)
        print("parse_data:", params)
        data, err_txt = FinanceTransactService.get(params, data['user_id'])
        if err_txt:
            return util_response(err=47767, msg=err_txt)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': data
        })

    # 创建
    def post(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            return util_response(err=4001, msg='缺少Token')
        data, err_txt = UserService.check_token(token)
        if not data:
            return util_response(err=4002, msg=err_txt)
        params = parse_data(request)
        params['account_id'] = data['user_id']
        if not params:
            return util_response(err=6046, msg='至少需要一个请求参数')
        data, err_txt = FinanceTransactService.post(params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    #
    #
    # # 生成交易号：2位数（当前年份后2位数字）+8位数（当前时间戳去头2位）+6位数（用户名 经过hash crc16生成的 4位十六进制 转成5位数 然后头为补0）
    # # 2位数（当前年份后2位数字）+8位数（当前时间戳去头2位）
    # def year_timestamp(self):
    #     date_time = time.localtime(time.time())
    #     # 截取第3位到第4位
    #     year_str = (str(date_time.tm_year))[2:4]
    #
    #     # 当前时间戳
    #     time_stamp = str(int(time.time()))
    #     # 截取第3位到第10位
    #     eight_time_stamp = time_stamp[2:10]
    #     code = year_str + eight_time_stamp
    #     return code
    #
    # # crc16
    # # @brief 传入需要编码一致性的字符串
    # # @return 返回十六进制字符串
    #
    # def make_crc16(self, x):
    #     a = 0xFFFF
    #     b = 0xA001
    #     for byte in x:
    #         a ^= ord(byte)
    #         for i in range(8):
    #             last = a % 2
    #             a >>= 1
    #             if last == 1:
    #                 a ^= b
    #     s = hex(a).upper()
    #     return s[2:6]
    # 分销
    def distribution(self):
        params = parse_data(self)
        data, err_txt = FinanceTransactsService.distribution(params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    # 核销
    def write_off(self):
        params = parse_data(self)
        data, err_txt = FinanceTransactsService.write_off(params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
