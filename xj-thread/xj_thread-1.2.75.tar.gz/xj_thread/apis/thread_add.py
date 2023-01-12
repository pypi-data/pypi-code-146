# encoding: utf-8
"""
@project: djangoModel->thread_add
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 信息添加接口
@created_time: 2022/8/8 13:36
"""
from rest_framework.views import APIView

from xj_user.services.user_service import UserService
from ..services.thread_item_service import ThreadItemService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data


class ThreadAdd(APIView):
    def post(self, request):
        # token验证
        token = request.META.get('HTTP_AUTHORIZATION', None)
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            return util_response(err=6045, msg=error_text)
        params = parse_data(request)
        # print("ThreadAdd: params:", params)
        # print("ThreadAdd: token_serv:", token_serv)
        params['user_id'] = token_serv.get('user_id', None)
        # # 表单初步验证
        # validator = ThreadAddValidator(params)
        # is_pass, error = validator.validate()
        # if not is_pass:
        #     return util_response(err=4022, msg=error)
        # 插入服务
        data, err_txt = ThreadItemService.add(params)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
