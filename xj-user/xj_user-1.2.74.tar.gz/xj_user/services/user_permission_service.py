# encoding: utf-8
"""
@project: djangoModel->user_permission_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户权限服务
@created_time: 2022/8/23 9:33
"""
from django.db.models import F

from ..utils.j_dict import JDict
from ..models import BaseInfo, PermissionValue, Group


class PermissionService():
    __user_dict = None
    __is_err = False
    __err_message = None

    @staticmethod
    def get_group_user(user_id):
        inner_group = BaseInfo.objects.filter(id=user_id) \
            .annotate(parent_group_id=F("user_group__parent_group"))
        inner_group = inner_group.values('user_group_id', "parent_group_id").first() if inner_group else {'user_group_id': -1, "parent_group_id": -1}
        child_group_ids = [i['id'] for i in list(Group.objects.filter(parent_group=inner_group['user_group_id']).values("id"))]
        res_set = {
            "GROUP_INSIDE": [i['id'] for i in list(BaseInfo.objects.filter(user_group_id=inner_group['user_group_id']).values("id"))],
            "GROUP_PARENT": [i['id'] for i in list(BaseInfo.objects.filter(user_group_id=inner_group['parent_group_id']).values("id"))],
            "GROUP_CHILDREN": [i['id'] for i in list(BaseInfo.objects.filter(user_group_id__in=child_group_ids).values("id"))],
            "GROUP_OUTSIDE": []
        }
        return res_set, None

    @staticmethod
    def get_user_group_permission(user_id, module=None, feature="USER_GROUP", type=None):
        try:
            # 获取用户的权限
            params = {k: v for k, v in {"module": module, "feature": feature}.items() if v}
            permission_set = BaseInfo.objects.filter(id=user_id).annotate(user_permission_id=F("user_group__permission_id"))
            if not permission_set:  # 用户ID不存在
                return {}, None
            permission_dict = permission_set.values("user_permission_id").first()
            if not permission_dict['user_permission_id']:  # 没有用户组配置权限值
                return {}, None
            params.setdefault("permission_id", permission_dict['user_permission_id'])
            values = list(PermissionValue.objects.filter(**params).values(
                "module", "permission_value", "relate_value", "ban_view", "ban_edit", "ban_add", "ban_delete", "is_ban", "is_system", 'is_enable'
            ))
            if not values:  # 有权限ID但是没有 配置对应权限值
                return {}, None
            # 权限值
            res = JDict({})
            group_user, err = PermissionService.get_group_user(user_id)
            for item in values:
                item_copy = JDict(item)
                module_name = item_copy.pop('module')
                res.setdefault(module_name, {})

                current_module = getattr(res, module_name)
                current_module.setdefault('relate_value', item_copy.pop("relate_value"))

                permission_value = item_copy.pop('permission_value')
                item_copy["user_list"] = group_user[permission_value]
                current_module.setdefault(permission_value, item_copy)
            res = res[module] if module else res
            return res, None
        except Exception as e:
            print("msg:" + str(e) + "line:" + str(e.__traceback__.tb_lineno))
            return None, "msg:" + str(e) + "line:" + str(e.__traceback__.tb_lineno)
