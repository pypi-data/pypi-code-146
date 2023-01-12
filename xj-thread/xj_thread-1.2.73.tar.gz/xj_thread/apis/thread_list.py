"""
Created on 2022-04-11
@description:刘飞
@description:发布子模块逻辑分发
"""
from rest_framework.views import APIView

from xj_location.services.location_service import LocationService
from xj_role.services.auto_permission_service import AutoPermissionValueService
from xj_user.services.user_detail_info_service import DetailInfoService
# from xj_user.services.user_service import UserService
from xj_user.utils.user_wrapper import user_authentication_wrapper
from ..services.thread_list_service import ThreadListService
from ..services.thread_statistic_service import StatisticsService
# from ..utils.custom_authentication_wrapper import authentication_wrapper
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.join_list import JoinList


class ThreadListAPIView(APIView):
    """
    get: 信息表列表
    post: 信息表新增
    """

    # @authentication_wrapper

    # 我们更希望通过装饰器来做权限验证，这样可以更好的精简API层的代码量 2022.10.3 by Sieyoo
    @user_authentication_wrapper  # 如果有token则返回user_info，无则返回空
    @request_params_wrapper
    def get(self, *args, user_info=None, request_params, **kwargs):
        params = request_params
        # print("request_params:", request_params, "kwargs:", kwargs, "user_info:", user_info)
        category_value = request_params.get('category_value') or kwargs.get("category_value")
        filter_fields = request_params.get('filter_fields', None)
        sort = request_params.get('sort', None)
        # print("> ThreadListAPIView category_value 2:", category_value)
        params.setdefault("category_value", category_value)
        page = request_params.get('page', 1)
        size = request_params.get('size', 20)
        if int(size) > 100:
            return util_response(msg='每一页不可以超过100条', err=1000)

        # 弃用，我们更希望通过装饰器来做权限验证，这样可以更好的精简API层的代码量 2022.10.3 by Sieyoo
        # 获取权限,权限验证
        # token = request.META.get('HTTP_AUTHORIZATION', None)
        # print("> ThreadListAPIView token:", token)
        # if token and str(token).strip().upper() != "BEARER":
        #     token_serv, error_text = UserService.check_token(token)
        #     if error_text:
        #         return util_response(err=6000, msg=error_text)
        #     token_serv, error_text = UserService.check_token(token)

        # ==================== 1、先通过用户ID拿到所属权限 ====================
        auth_dict = {}
        user_id = user_info.get("user_id", None) if user_info else None
        # if user_id:
        #     auth_dict, error_text = PermissionService.user_permission_tree(user_id=user_id, module="thread")
        # if error_text:
        #     return util_response(err=1002, msg=error_text)
        # auth_dict = JDict(auth_dict)  # 与当前用户有关的权限值
        # print("> auth_dict", auth_dict)
        # other_role_dict = auth_dict.THREAD and auth_dict.THREAD.OTHER_ROLE_OPERATE or {}  # 他人操作权限
        # self_role_dict = auth_dict.THREAD and auth_dict.THREAD.SELF_ROLE_OPERATE or {}  # 本人操作权限
        # print("> other_role_dict, self_role_dict", other_role_dict, self_role_dict)

        # ==================== 2、再过滤掉不可查看的类别（即同级、子级、父级、外级全禁止的） ====================

        # ==================== 3、再去掉有access_level(访问级别)的信息 ====================

        # ==================== 4、逐个类别查看是否有允许查看和用户ID列表 ====================

        # ban_user_list = []  # 允许读的用户列表
        # allow_user_list = []  # 禁止读的用户列表
        # if auth_dict.GROUP_PARENT and auth_dict.GROUP_PARENT.ban_view.upper() == "Y":
        #     ban_user_list.extend(auth_dict.GROUP_PARENT.user_list)
        # else:
        #     allow_user_list.extend(auth_dict.GROUP_PARENT.user_list if auth_dict.GROUP_PARENT else [])
        #
        # if auth_dict.GROUP_CHILDREN and auth_dict.GROUP_CHILDREN.ban_view.upper() == "Y":
        #     ban_user_list.extend(auth_dict.GROUP_CHILDREN.user_list)
        # else:
        #     allow_user_list.extend(auth_dict.GROUP_CHILDREN.user_list if auth_dict.GROUP_CHILDREN else [])
        #
        # if auth_dict.GROUP_INSIDE and auth_dict.GROUP_INSIDE.ban_view.upper() == "Y":
        #     ban_user_list.extend(auth_dict.GROUP_INSIDE.user_list)
        # else:
        #     allow_user_list.extend(auth_dict.GROUP_INSIDE.user_list if auth_dict.GROUP_INSIDE else [])
        #
        # if not auth_dict.GROUP_ADMINISTRATOR and not auth_dict.GROUP_MANAGER:
        #     if auth_dict.GROUP_OUTSIDE and auth_dict.GROUP_OUTSIDE.ban_view.upper() == "Y":
        #         params['user_id__in'] = allow_user_list
        #     else:
        #         params["user_id__not_in"] = ban_user_list
        # else:
        #     params["is_admin"] = True

        # print("> ThreadListAPIView params:", params)
        # print("> ThreadListAPIView allow_user_list, ban_user_list:", allow_user_list, ban_user_list)

        # 获取列表数据
        thread_serv, error_text = ThreadListService.list(params, page=page, size=size, filter_fields=filter_fields, sort=sort)
        # print("thread_serv:", thread_serv, "params:", params)
        if error_text:
            return util_response(err=1003, msg=error_text)
        # print("> thread_serv:", thread_serv)

        # 按权限自动过滤数据
        thread_list = AutoPermissionValueService.auto_filter_by_permission(
            source_list=thread_serv['list'], user_id=user_id, module='THREAD',
            feature_list=['OTHER_ROLE_OPERATE', 'SELF_ROLE_OPERATE', ])
        # print("> thread_list:", len(thread_list), thread_list)
        thread_serv['list'] = thread_list
        # ID列表拆分
        thread_id_list = list(set([item['id'] for item in thread_serv['list'] if item['id']]))
        user_id_list = list(set([item['user_id'] for item in thread_serv['list'] if item['user_id']]))
        # 用户数据和统计数据
        statistic_list = StatisticsService.statistic_list(id_list=thread_id_list)
        user_info_list = DetailInfoService.get_list_detail(params=None, user_id_list=user_id_list)

        # 根据模块化原则，信息模块是基本模块，但定位模块是扩展模块。不允许信息模块强制捆绑扩展模块。by sieyoo at 20221221
        # location_list, err = LocationService.location_list(params={"thread_id_list": thread_id_list}, need_pagination=False, fields=["thread_id", "name", "region_code", "longitude", "latitude"])
        # if not err:
        #     thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=location_list, l_key="id", r_key='thread_id').join()

        # 用户数据(full_name, avatar), 统计数据(statistic),
        thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=statistic_list, l_key="id",
                                       r_key='thread_id').join()
        thread_serv['list'] = JoinList(l_list=thread_serv['list'], r_list=user_info_list, l_key="user_id",
                                       r_key='user_id').join()
        thread_serv['auth_dict'] = auth_dict
        thread_serv['old_size'] = thread_serv['size']
        thread_serv['size'] = size
        # thread_serv['list'] = thread_list
        return util_response(data=thread_serv, is_need_parse_json=True)
