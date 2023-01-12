# encoding: utf-8
"""
@project: djangoModel->enroll_status_code
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 状态码
@created_time: 2022/11/13 16:31
"""
from rest_framework.views import APIView
from django.views.decorators.http import require_http_methods

from xj_user.utils.user_wrapper import user_authentication_force_wrapper
from ..service.enroll_status_code_service import EnrollStatusCodeService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class EnrollStatusCodeAPI(APIView):
    @require_http_methods(['PUT'])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def batch_edit_code(self, *args, request_params=None, user_info=None, **kwargs, ):
        code = request_params.get("code", None)
        enroll_id = request_params.get("enroll_id", None) or kwargs.get("enroll_id", None)
        edit_types = request_params.get("edit_types", "enroll,enroll_record,enroll_subitems,enroll_subitem_record", "")
        if not code or not enroll_id or not edit_types:
            return util_response(err=1000, msg="参数错误")
        data, err = EnrollStatusCodeService.batcch_edit_code(enroll_id, code, edit_types.split(","))
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)
