# encoding: utf-8
"""
@project: djangoModel->wechet_login
@author: 孙楷炎
@created_time: 2022/7/14 10:55
"""

# 微信登录方法
from rest_framework.views import APIView

from ..services.wechat_service import WechatService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data


class WechetLogin(APIView):
    # 微信手机号码登录
    def post(self, request):
        phone_code = request.data.get('phone_code', None)
        login_code = request.data.get('login_code', None)
        sso_serve_id = request.data.get('sso_serve_id', None)
        params = parse_data(request)

        if not phone_code:
            return util_response(err=6558, msg='参数错误')
        app = WechatService()
        err, data = app.wechat_login(phone_code=phone_code, login_code=login_code, sso_serve_id=sso_serve_id, detail_params=params)
        if err == 0:
            return util_response(data=data)
        else:
            return util_response(msg=err, err=6004)
