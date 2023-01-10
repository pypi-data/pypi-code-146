# _*_coding:utf-8_*_
from django.forms import model_to_dict

from ..models import Platform


class UserPlatformService:
    def __init__(self):
        pass

    # 检测账户
    @staticmethod
    def get_platform_info(platform_name=None):
        if not platform_name:
            return None, '平台参数未传(platform_name)'

        platform_set = Platform.objects.filter(platform_name=platform_name).first()
        # print(">  get_platform_info platform_set:", platform_set, type(platform_set))
        if not platform_set:
            return None, '平台不存在'

        return model_to_dict(platform_set), None

