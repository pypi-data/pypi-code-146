# encoding: utf-8
"""
@project: djangoModel->user_detail_info
@author: 孙楷炎
@synopsis: 用户详细信息操作
@created_time: 2022/6/27 19:42
"""

from rest_framework.views import APIView

from ..services.user_detail_info_service import DetailInfoService, parse_data
from ..services.user_service import UserService
from ..utils.custom_response import util_response


# 列表
class UserListDetail(APIView):
    def get(self, request, *args):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6045, msg=error_text)
        params = request.query_params
        data, err_txt = DetailInfoService.get_list_detail(params)
        if not error_text:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)


# 用户详细信息
class UserDetail(APIView):
    def get(self, request, *args):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6045, msg=error_text)
        user_id = request.query_params.get('user_id') if request.query_params.get('user_id') else token_serv['user_id']
        data, error_text = DetailInfoService.get_detail(user_id)
        if error_text is None:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)


# 用户必须存在才有信息编辑，所以这个接口是多余的
class UserDetailEdit(APIView):
    def post(self, request, *args):
        # 身份验证，传user_id使用传的，没有传使用token获取的
        token_serv, error_text = UserService.check_token(request.META.get('HTTP_AUTHORIZATION', None))
        if error_text:
            return util_response(err=6045, msg=error_text)
        # 查询该用户是否存在详细信息 TODO 需要判断修改人是否有权限
        params = parse_data(request)
        if not params:
            return util_response(err=6046, msg='至少需要一个请求参数')
        params.setdefault('user_id', token_serv.get('user_id'))
        data, err_txt = DetailInfoService.create_or_update_detail(params=params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)


# 用户必须存在才有信息编辑，所以这个接口是多余的
class UserDetailExtendFields(APIView):
    def get(self, request, *args):
        # 身份验证，传user_id使用传的，没有传使用token获取的
        # 查询该用户是否存在详细信息 TODO 需要判断修改人是否有权限
        data, err_txt = DetailInfoService.get_extend_fields()
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
