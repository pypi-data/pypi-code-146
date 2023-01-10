# _*_coding:utf-8_*_
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils.model_handle import parse_data, util_response
from ..services.user_sso_serve_service import UserSsoServeService


class UserSsoServe(APIView):

    def get(self, request, *args, **kwargs):
        # print(self.request)
        data, err_txt = UserSsoServeService.list()
        if not data:
            return util_response(err=4002, msg=err_txt)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': data
        })

    def post(self, request, *args, **kwargs):
        # print(self.request)
        params = parse_data(self.request)
        data, err_txt = UserSsoServeService.add(params)
        if not data:
            return util_response(err=4002, msg=err_txt)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': data
        })
