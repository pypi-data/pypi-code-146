# encoding: utf-8
"""
@project: djangoModel->user_list
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户信息列表
@created_time: 2022/7/25 9:42
"""
from rest_framework.views import APIView

from xj_role.services.user_group_service import UserGroupService
from xj_role.services.permission_service import PermissionService
from ..services.user_service import UserService
from ..utils.custom_response import util_response
from ..utils.custom_tool import is_number
from ..utils.model_handle import parse_data
from ..utils.j_dict import JDict


class UserListAPIView(APIView):
    # 在有的框架中会出现传入3个参数的问题，原因不明，可能和两边使用的版本不同有关
    def get(self, request, *args):
        # # token验证
        # token = request.META.get('HTTP_AUTHORIZATION', None)
        # token_serv, error_text = UserService.check_token(token)
        # if error_text:
        #     return util_response(err=6045, msg=error_text)

        params = parse_data(request)
        # 获取权限,权限验证
        auth_list = {}
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token and str(token).strip().upper() != "BEARER":
            token_serv, error_text = UserService.check_token(token)
            if error_text:
                return util_response(err=6000, msg=error_text)
            token_serv, error_text = UserService.check_token(token)
            auth_list, error_text = PermissionService.user_permission_tree(user_id=token_serv.get("user_id"),
                                                                           module="user")
            if error_text:
                return util_response(err=1002, msg=error_text)

        auth_list = JDict(auth_list)
        ban_user_list = []
        allow_user_list = []
        if auth_list.GROUP_PARENT and auth_list.GROUP_PARENT.ban_view.upper() == "Y":
            ban_user_list.extend(auth_list.GROUP_PARENT.user_list)
        else:
            allow_user_list.extend(auth_list.GROUP_PARENT.user_list if auth_list.GROUP_PARENT else [])

        if auth_list.GROUP_CHILDREN and auth_list.GROUP_CHILDREN.ban_view.upper() == "Y":
            ban_user_list.extend(auth_list.GROUP_CHILDREN.user_list)
        else:
            allow_user_list.extend(auth_list.GROUP_CHILDREN.user_list if auth_list.GROUP_CHILDREN else [])

        if auth_list.GROUP_INSIDE and auth_list.GROUP_INSIDE.ban_view.upper() == "Y":
            ban_user_list.extend(auth_list.GROUP_INSIDE.user_list)
        else:
            allow_user_list.extend(auth_list.GROUP_INSIDE.user_list if auth_list.GROUP_INSIDE else [])

        if not auth_list.GROUP_ADMINISTRATOR and not auth_list.GROUP_MANAGER:
            if auth_list.GROUP_OUTSIDE and auth_list.GROUP_OUTSIDE.ban_view.upper() == "Y":
                params['user_id__in'] = allow_user_list  # TODO 待删除
                params['allow_user_list'] = allow_user_list
            else:
                params["user_id__not_in"] = ban_user_list  # TODO 待删除
                params["ban_user_list"] = ban_user_list
        else:
            params["is_admin"] = True
        # 分组筛选用户ID
        # user_group_id = params.pop("user_group_id", None)
        # if user_group_id and is_number(user_group_id):
        #     id_list, err = GroupService.get_user_from_group(user_group_id)
        #     params.setdefault("id_list", id_list)
        # 获取数据
        data, error_text = UserService.user_list(params,allow_user_list,ban_user_list)
        if error_text:
            return util_response(err=47767, msg=error_text)
        return util_response(data=data)
