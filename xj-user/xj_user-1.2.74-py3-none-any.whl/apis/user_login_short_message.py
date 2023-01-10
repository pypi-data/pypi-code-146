from django.core.cache import cache
from rest_framework import response
from rest_framework.views import APIView

from ..utils.model_handle import parse_data
from ..services.user_sms_service import UserSmsService
from ..utils.custom_response import util_response


class ShortMessageLogin(APIView):

    # 短信验证码校验
    def sms_login(self):
        # 1. 电话和手动输入的验证码
        params = parse_data(self)
        phone = params.get('phone')
        code = params.get('code')
        login_code = params.get('login_code', None)
        sso_serve_id = params.get('sso_serve_id', None)
        if code is None:
            return util_response(err=4002, msg="验证码不能为空")
        cache_code = cache.get(phone)
        if code == cache_code:
            app = UserSmsService()
            err, data = app.phone_login(phone=phone, login_code=login_code, sso_serve_id=sso_serve_id, detail_params=params)
            if err == 0:
                return util_response(data=data)
            else:
                return util_response(msg=err, err=6004)
        else:
            return util_response(err=4002, msg="验证码错误")

    # 短信验证码校验
    def post(self, request):
        # 1. 电话和手动输入的验证码
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        login_code = request.data.get('login_code', None)
        sso_serve_id = request.data.get('sso_serve_id', None)

        # params = parse_data(self)
        print(self.request.POST.get('phone'))
        if code is None:
            res = {
                'err': 4002,
                'msg': '验证码不能为空',
            }
            return response.Response(data=res, status=None, template_name=None)
        cache_code = cache.get(phone)
        if code == cache_code:
            app = UserSmsService()
            err, data = app.phone_login(phone=phone, login_code=login_code, sso_serve_id=sso_serve_id)
            if err == 0:
                return util_response(data=data)
            else:
                return util_response(msg=err, err=6004)
        else:
            res = {
                'err': 4002,
                'msg': '验证码错误',
            }
            return response.Response(data=res, status=None, template_name=None)


class MyApiError(Exception):
    def __init__(self, message, err_code=4010):
        self.msg = message
        self.err = err_code

    def __str__(self):
        # repr()将对象转化为供解释器读取的形式。可省略
        return repr(self.msg)
