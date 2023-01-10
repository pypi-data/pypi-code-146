# _*_coding:utf-8_*_

import logging
from pathlib import Path
import re

from django.db.models import Q
from rest_framework import generics
from rest_framework import response
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from main.settings import BASE_DIR
from xj_role.services.role_service import RoleService
from xj_role.services.user_group_service import UserGroupService
from ..models import *
from ..services.user_detail_info_service import DetailInfoService
from ..services.user_service import UserService
from ..utils.custom_response import util_response
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.model_handle import parse_data

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""

logger = logging.getLogger(__name__)


class UserInfoSerializer(serializers.ModelSerializer):
    # 方法一：使用SerializerMethodField，并写出get_platform, 让其返回你要显示的对象就行了
    # p.s.SerializerMethodField在model字段显示中很有用。
    # platform = serializers.SerializerMethodField()

    # # 方法二：增加一个序列化的字段platform_name用来专门显示品牌的name。当前前端的表格columns里对应的’platform’列要改成’platform_name’
    user_id = serializers.ReadOnlyField(source='id')

    # platform_id = serializers.ReadOnlyField(source='platform.platform_id')
    # platform_name = serializers.ReadOnlyField(source='platform.platform_name')

    class Meta:
        model = BaseInfo
        fields = [
            'user_id',
            # 'platform',
            # 'platform_uid',
            # 'platform__platform_name',
            # 'platform_id',
            # 'platform_name',
            'user_name',
            'full_name',
            'phone',
            'email',
            'wechat_openid',
            'user_info',
        ]
        # exclude = ['platform_uid']

    # 这里是调用了platform这个字段拼成了get_platform
    def get_platform(self, obj):
        return obj.platform.platform_name
        # return {
        #     'id': obj.platform.platform_id,
        #     'name': obj.platform.platform_name,
        # }


# 获取用户信息
class UserEdit(generics.UpdateAPIView):  # 或继承(APIView)
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    serializer_class = UserInfoSerializer
    params = None

    def post(self, request, *args, **kwargs):
        # self.params = request.query_params.copy()  # 返回QueryDict类型
        self.params = request.data.copy()  # 返回QueryDict类型
        # print("> params:", self.params)
        # print("> params: user_info:", self.params.get('user_info', ''))
        # print("> params: user_info:", type(self.params.get('user_info', '')))

        try:
            token = self.request.META.get('HTTP_AUTHORIZATION', '')
            if re.match(r'Bearer (.*)', token):
                token = re.match(r'Bearer (.*)', token).group(1)
            # print("> token:", token)

            if not token:
                # raise MyApiError('缺少Token', 6001)
                return util_response('', 7557, "缺少Token")

            # 判断token是否失效
            t_auth = Auth.objects.filter(token=token).order_by('-update_time').first()
            # print("> t_auth:", t_auth)
            if not t_auth:
                # raise MyApiError('token失效', 6002)
                return util_response('', 7557, "token失效")

            # 如果有用户ID则找到该ID，没有则修改自己的ID
            # print("> self.params['user_id']:", self.params)
            if 'user_id' in self.params:
                user_id = self.params.get('user_id', '')
            else:
                user_id = t_auth.user_id
            # print("> user_id:", user_id)

            t_user = BaseInfo.objects.get(id=user_id)
            # print("> t_user:", t_user)

            # 检查必填项
            # if not self.params.get('platform_uid', ''):
            #     self.params['platform_uid'] = t_user.platform_uid
            if not self.params.get('user_name', ''):
                self.params['user_name'] = t_user.user_name

            serializer = UserInfoSerializer(instance=t_user, data=self.params, )
            if not serializer.is_valid():
                raise MyApiError(serializer.errors, 6003)
            serializer.save()

            res = {
                'err': 0,
                'msg': '修改成功',
            }

        except SyntaxError:
            # print("> SyntaxError:")
            res = {
                'err': 6004,
                'msg': '语法错误'
            }
        except LookupError:
            res = {
                'err': 6005,
                'msg': '无效数据查询'
            }
        # 这里 error是一个类的对象，要用error.属性名来返回
        except Exception as error:
            res = {
                'err': error.err if hasattr(error, 'err') else 4000,  # 发生系统异常时报4000
                'msg': error.msg if hasattr(error, 'msg') else error.args,  # 发生系统异常时捕获error.args
            }
            if not hasattr(error, 'err'):
                res['file'] = error.__traceback__.tb_frame.f_globals["__file__"],  # 发生异常所在的文件
                res['line'] = error.__traceback__.tb_lineno,  # 发生异常所在的行数
        except:
            res = {
                'err': 6006,
                'msg': '未知错误'
            }

        # return super(UserLogin, self).patch(request, *args, **kwargs)
        return response.Response(res)

    def put(self, request, *args, **kwargs):
        self.params = parse_data(request)
        detaili_list = DetailInfoService.transform_result(self.params)
        detaili = detaili_list[0]
        # 权限验证
        token = request.META.get('HTTP_AUTHORIZATION', '')
        token_serv, error_text = UserService.check_token(token)
        if error_text:
            # raise MyApiError(error_text, 6010)
            return util_response(err=6002, msg=error_text)
            # 判断token是否失效
        if re.match(r'Bearer(.*)$', token, re.IGNORECASE):
            token = re.match(r'Bearer(.*)$', token, re.IGNORECASE).group(1).strip()
        t_auth = Auth.objects.filter(token=token).order_by('-update_time').first()
        if not t_auth:
            # raise MyApiError('token失效', 6002)
            return util_response(err=6002, msg="token失效")

        # 如果有用户ID则找到该ID，没有则修改自己的ID
        if 'user_id' in self.params:
            user_id = self.params.get('user_id', '')
        else:
            user_id = t_auth.user_id
        # 添加逻辑
        try:

            user_name = str(self.params.get('user_name', ''))
            full_name = str(self.params.get('full_name', ''))
            nickname = str(self.params.get('nickname', ''))
            phone = str(self.params.get('phone', ''))
            # 用户角色部门绑定
            user_role_list = self.params.get('user_role_list', None)
            user_group_list = self.params.get('user_group_list', None)

            base_info = {}
            if user_name:
                base_info['user_name'] = user_name
                is_exists = BaseInfo.objects.filter(Q(user_name=user_name), ~Q(id=user_id)).exists()
                if is_exists:
                    return util_response('', 7557, "用户名已存在")
            if full_name:
                base_info['full_name'] = full_name
            if nickname:
                base_info['nickname'] = nickname
            if phone:
                base_info['phone'] = phone

            BaseInfo.objects.filter(id=user_id).update(**base_info)

            if detaili.get("user_name"):
                del detaili['user_name']
            if detaili.get("full_name"):
                detaili['real_name'] = detaili['full_name']
                del detaili['full_name']
            if detaili.get("nickname"):
                del detaili['nickname']
            if detaili.get("phone"):
                del detaili['phone']
            if detaili.get("email"):
                del detaili['email']
            if detaili.get("user_role_list"):
                del detaili['user_role_list']
            if detaili.get("user_group_list"):
                del detaili['user_group_list']
            detaili = DetailInfoService.transform_params(detaili)
            detailinfo = DetailInfo.objects.filter(user_id=user_id).first()
            if detailinfo:
                DetailInfo.objects.filter(user_id=user_id).update(**detaili)
            else:
                detaili['user_id'] = user_id
                DetailInfo.objects.create(**detaili)

            # 用户绑定权限和部门
            if user_group_list:
                UserGroupService.bind_user_group(user_id, user_group_list)

            if user_role_list:
                RoleService.bind_user_role(user_id, user_role_list)

            res = {
                'err': 0,
                'msg': '修改成功',
                'data': {"user_id": user_id},
            }

        except SyntaxError:
            res = {
                'err': 4001,
                'msg': '语法错误'
            }
        except LookupError:
            res = {
                'err': 4002,
                'msg': '无效数据查询'
            }
        except Exception as valueError:
            res = {
                'err': valueError.err if hasattr(valueError, 'err') else 4000,
                'msg': valueError.msg if hasattr(valueError, 'msg') else valueError.args,
            }
        except:
            res = {
                'err': 4999,
                'msg': '未知错误'
            }

        return response.Response(data=res, status=None, template_name=None, headers={"Authorization": token}, content_type=None)

    def delete(self, request, *args, **kwargs):
        # return model_delete(request, BaseInfo)
        from_data = parse_data(request)
        if not 'id' in from_data.keys():
            return util_response('', 7557, "ID不能为空")
        res = BaseInfo.objects.filter(id=from_data['id'])
        if not res:
            return util_response('', 7557, "数据不存在")

        detailinfo = DetailInfo.objects.filter(user_id=from_data['id']).first()
        if detailinfo:
            DetailInfo.objects.filter(user_id=from_data['id']).delete()
        res.delete()
        return util_response()


class MyApiError(Exception):
    def __init__(self, message, err_code=4010):
        self.msg = message
        self.err = err_code

    def __str__(self):
        # repr()将对象转化为供解释器读取的形式。可省略
        return repr(self.msg)
