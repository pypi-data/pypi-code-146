# _*_coding:utf-8_*_

from datetime import datetime, timedelta
from pathlib import Path
# import os, logging, time, json, copy
import re

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.forms import model_to_dict
import jwt
# from django.db.models import F
# from rest_framework import exceptions
from rest_framework import serializers

from config.config import JConfig as MainConfig
from main.settings import BASE_DIR
from ..models import Auth, DetailInfo, ExtendField
from ..models import BaseInfo
from ..utils.custom_tool import filter_result_field
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

app_id = main_config_dict.app_id or module_config_dict.app_id or ""
app_secret = main_config_dict.secret or module_config_dict.secret or ""
jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""

config = MainConfig()
class UserInfoSerializer(serializers.ModelSerializer):
    # 方法一：使用SerializerMethodField，并写出get_platform, 让其返回你要显示的对象就行了
    # p.s.SerializerMethodField在model字段显示中很有用。
    # platform = serializers.SerializerMethodField()

    # # 方法二：增加一个序列化的字段platform_name用来专门显示品牌的name。当前前端的表格columns里对应的’platform’列要改成’platform_name’
    user_id = serializers.ReadOnlyField(source='id')
    permission_value = serializers.SerializerMethodField()

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
            # 'get_group_desc',
            'user_name',
            'full_name',
            'phone',
            'email',
            'wechat_openid',
            'user_info',
            'user_group',
            'user_group_id',
            'permission',
            'permission_value'
        ]
        # exclude = ['platform_uid']

    def get_permission_value(self, instance):
        pass

    # # 这里是调用了platform这个字段拼成了get_platform
    # def get_platform(self, obj):
    #     return obj.platform.platform_name
    #     # return {
    #     #     'id': obj.platform.platform_id,
    #     #     'name': obj.platform.platform_name,
    #     # }


class UserService:
    def __init__(self):
        pass

    # 检测账户
    @staticmethod
    def check_account(account):
        """
        @param account 用户账户，可以支持三种类型：手机、用户名、邮箱。自动判断
        @description 注意：用户名不推荐由纯数字构成，因为那样容易和11位手机号冲突
        """
        # 账号类型判断
        if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
            account_type = 'phone'
        elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
            account_type = 'email'
        elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
            account_type = 'username'
        else:
            return None, "账号必须是用户名、手机或者邮箱，用户名不能是数字开头"

        # 用户ID
        user_list = BaseInfo.objects.filter(Q(user_name=account) | Q(phone=account) | Q(email=account)) \
            .annotate(user_id=F("id")) \
            .values(
            'user_id',
            'user_name',
            'full_name',
            'nickname',
            'phone',
            'email',
            'wechat_openid',
            'user_info',
            # 'user_group_id',
            # 'user_group_value',
            # 'permission_id',
            # 'permission_value'
        )
        if not user_list.count():
            return None, "账户不存在"
        if user_list.count() > 1:
            return None, "登录异常，请联系管理员，发现多账号冲突："
        # print("> user_list:", user_list)
        user_set = user_list.first()

        # serializer = UserInfoSerializer(user_set, many=False)
        # print("> serializer:", serializer)
        return user_set, None

    # 验证密码
    @staticmethod
    def check_login(user_id, password, account):
        """
        @param user_id 用户ID
        @param password 用户密码。
        @param account 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """
        auth_set = Auth.objects.filter(user_id=user_id, password__isnull=False).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + account + "(" + str(user_id) + ")"

        # 判断密码不正确
        is_pass = check_password(password, auth_set.password)
        if not is_pass:
            return None, "密码错误"

        # print(int(Config.getIns().get('xj_user', 'DAY', 7)))
        # print(Config.getIns().get('xj_user', 'JWT_SECRET_KEY', ""))

        # 过期时间
        # int(Config.getIns().get('xj_user', 'DAY', 7))
        # int(Config.getIns().get('xj_user', 'SECOND', 0))
        expire_timestamp = datetime.utcnow() + timedelta(days=7, seconds=0)
        # 为本次登录生成Token并记录
        # todo 漏洞，当用户修改用户名时，并可能导致account失效，是否存用户ID更好
        token = jwt.encode(payload={'account': account, 'user_id': user_id, "exp": expire_timestamp},
                           key=jwt_secret_key)
        # payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY', ""), verify=True, algorithms=["RS256", "HS256"])
        # print("> payload:", payload)
        auth_set.token = token
        auth_set.save()

        return {'token': token}, None

    # 微信登录
    @staticmethod
    def check_login_wechat(user_id, phone):
        """
        @param user_id 用户ID
        @param phone 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """
        auth_set = Auth.objects.filter(user_id=user_id, password__isnull=False).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + phone + "(" + str(user_id) + ")"

        # 过期时间
        expire_timestamp = datetime.utcnow() + timedelta(days=7, seconds=0)
        # 为本次登录生成Token并记录
        # todo 漏洞，当用户修改用户名时，并可能导致account失效，是否存用户ID更好
        token = jwt.encode(payload={'account': phone, 'user_id': user_id, "exp": expire_timestamp},
                           key=jwt_secret_key)
        # payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY'), verify=True, algorithms=["RS256", "HS256"])
        # print("> payload:", payload)
        auth_set.token = token
        auth_set.save()

        return {'token': token}, None

    # 验证密码
    @staticmethod
    def check_login_short(user_id, phone):
        """
        @param user_id 用户ID
        @param phone 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """
        auth_set = Auth.objects.filter(user_id=user_id, password__isnull=False).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + phone + "(" + str(user_id) + ")"

        # 过期时间
        expire_timestamp = datetime.utcnow() + timedelta(days=int(expire_day),
                                                         seconds=int(expire_second))
        # 为本次登录生成Token并记录
        # todo 漏洞，当用户修改用户名时，并可能导致account失效，是否存用户ID更好
        token = jwt.encode(payload={'account': phone, 'user_id': user_id, "exp": expire_timestamp},
                           key=jwt_secret_key)
        # payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY'), verify=True, algorithms=["RS256", "HS256"])
        # print("> payload:", payload)
        auth_set.token = token
        auth_set.save()

        return {'token': token}, None

    # 检测令牌
    @staticmethod
    def check_token(token):
        """
        @param token 用户令牌。
        @description 注意：用户令牌的载荷体payload中必须包含两个参数：account账号、exp过期时间，其中账号可以是手机、用户名、邮箱三种。
        @description BEARER类型的token是在RFC6750中定义的一种token类型，OAuth2.0协议RFC6749对其也有所提及，算是对RFC6749的一个补充。BEARER类型token是建立在HTTP/1.1版本之上的token类型，需要TLS（Transport Layer Security）提供安全支持，该协议主要规定了BEARER类型token的客户端请求和服务端验证的具体细节。
        @description 理论上，每次请求令牌后就更新一次令牌，以监测用户长期访问时，不至于到时间后掉线反复登陆。
        """
        # 检查是否有Bearer前辍，如有则截取
        # print("> token 1:", token)
        if not token:
            return None, "请登录"  # 缺少Token

        if re.match(r'Bearer(.*)$', token, re.IGNORECASE):
            token = re.match(r'Bearer(.*)$', token, re.IGNORECASE).group(1).strip()
        # print("> token 2:", token)

        if not token:
            return None, "您尚未登录"

        # # 验证token。另一种方式，从数据库核对Token，通过对比服务端的Token，以确定是否为服务器发送的。今后启用该功能。
        # auth_set = Auth.objects.filter(Q(token=token)).order_by('-update_time')
        # # print("> auth:", auth_set)
        # if not auth_set.count():
        #     raise MyApiError('token验证失败', 6002)
        # auth = auth_set.first()

        try:
            # jwt.decode会自动检查exp参数，如果超时则抛出jwt.ExpiredSignatureError超时
            # jwt_payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY'), verify=True, algorithms=["RS256", "HS256"])
            jwt_payload = jwt.decode(token, key=config.get('xj_user', 'JWT_SECRET_KEY', '@zxmxy2021!'),
                                     verify=True, algorithms=["RS256", "HS256"])
            # print("> jwt_payload:", jwt_payload)

        except jwt.ExpiredSignatureError:
            return None, "登录已过期，请重新登录"

        except jwt.InvalidTokenError:
            return None, "用户令牌无效，请重新登录"

        account = jwt_payload.get('account', None)
        user_id = jwt_payload.get('user_id', None)
        if not account:
            return {'payload': jwt_payload}, "错误：令牌载荷中未提供用户账户Account"

        # 检测用户令牌时不应该调用用户信息，这会导致任何接口都会查询用户表，时间会增加
        # user_info = UserService.check_account(account=account)

        return {'account': account, 'user_id': user_id}, None

    # 用户信息列表
    @staticmethod
    def user_list(params={}, allow_user_list=None, ban_user_list=None):
        user_base_set = BaseInfo.objects
        # 需要分页的时候
        page = params.get("page", 1)
        size = params.get("size", 20)
        # is_admin = params.pop("is_admin", False)  # TODO 漏洞

        # 允许筛选的字段
        user_name = params.get("user_name", None)
        email = params.get("email", None)
        phone = params.get("phone", None)
        full_name = params.get("full_name", None)
        nickname = params.get("nickname", None)

        # 开始按过滤条件
        try:
            user_base_set = user_base_set.annotate(user_id=F("id"))
            if allow_user_list:  # 筛选可以访问的列表
                user_base_set = user_base_set.filter(user_id__in=allow_user_list)

            if ban_user_list:  # 排除可以访问的列表
                user_base_set = user_base_set.filter(~Q(user_id__in=ban_user_list))

            if user_name:
                user_base_set = user_base_set.filter(user_name=user_name)
            if email:
                user_base_set = user_base_set.filter(email=email)
            if phone:
                user_base_set = user_base_set.filter(phone=phone)
            if full_name:
                user_base_set = user_base_set.filter(full_name__icontains=full_name)
            if nickname:
                user_base_set = user_base_set.filter(user_name__icontains=nickname)
            # print(user_base_set.query)

            # user_base_set = BaseInfo.objects.filter(**params).annotate(user_id=F("id"))
            count = user_base_set.count()
            user_base_set = user_base_set.values(
                "user_id",
                "email",
                "full_name",
                "user_name",
                "nickname",
                "phone",
                "register_time"
                # "permission_id",
                # "user_group_id",  # TODO 该功能已经移动到了角色模块 计划删除
                # "wechat_openid",
            )

        except Exception as e:
            return None, "err:" + e.__str__()
        page_set = Paginator(user_base_set, size).page(page)
        page_list = []
        if page_set:
            page_list = list(page_set.object_list)
        return {'size': int(size), 'page': int(page), 'count': count, 'list': page_list}, None

    @staticmethod
    def user_add(params):
        # 添加逻辑
        try:
            account = str(params.get('account', ''))
            password = str(params.get('password', ''))
            phone = str(params.get('phone', ''))
            full_name = str(params.get('full_name', ''))
            nickname = str(params.get('nickname', ''))

            # 边界检查
            if not account:
                return None, "account必填"

            # if not password:
            #     return None, "密码必填"

            # if not full_name:
            #     return None, "full_name"

            # 账号类型判断
            if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
                account_type = 'phone'
            elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
                account_type = 'email'
            elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
                account_type = 'username'
            else:
                return None, "账号必须是用户名、手机或者邮箱，用户名不能是数字开头"

            # 检查账号是否存在
            user_list = None
            if account_type == 'phone':
                user_list = BaseInfo.objects.filter(Q(phone=account))
            elif account_type == 'email':
                user_list = BaseInfo.objects.filter(Q(email=account))
            elif account_type == 'username':
                user_list = BaseInfo.objects.filter(Q(user_name=account))

            if user_list.count() and account_type == 'phone':
                return None, "手机已被注册: " + account
            elif user_list.count() and account_type == 'email':
                return None, "邮箱已被注册: " + account
            elif user_list.count() and account_type == 'username':
                return None, "用户名已被注册: " + account

            # # 检查平台是否存在
            # platform_id = None
            # platform_set = Platform.objects.filter(platform_name__iexact=platform)
            # if not platform_set.count() == 0:
            #     platform_id = platform_set.first().platform_id

            base_info = {
                'user_name': account if account_type == 'username' else '',
                'full_name': full_name,
                "nickname": nickname,
                'phone': account if account_type == 'phone' else phone,
                'email': account if account_type == 'email' else '',
            }
            current_user = BaseInfo.objects.create(**base_info)
            token = jwt.encode({'account': account}, jwt_secret_key)
            auth = {
                'user_id': current_user.id,
                'password': make_password(password, None, 'pbkdf2_sha1'),
                'plaintext': password,
                'token': token,
            }
            Auth.objects.create(**auth)
            # 用户绑定权限和部门

            return {"user_id": current_user.id}, None
        except SyntaxError:
            return None, "语法错误"
        except LookupError:
            return None, "无效数据查询"
        except Exception as valueError:
            return None, valueError.msg if hasattr(valueError, 'msg') else valueError.args
        except:
            return None, "未知错误"
        # 用户信息列表

    @staticmethod
    def user_basic_message(user_id=None, nickname=None, need_detail_info=True):
        # 查找是否存在该用户
        res_data = {}
        if user_id:
            user_basic_message = BaseInfo.objects.filter(id=user_id).annotate(user_id=F("id")).first()
        elif nickname:
            user_basic_message = BaseInfo.objects.filter(nickname=nickname).annotate(user_id=F("id")).first()
        else:
            # 没有输入搜索条件，非法调用直接返回空字典
            return res_data, None

        # 没有该用户的基础信息，是一个不存在的用户
        if not user_basic_message:
            return res_data, None

        # 找到该用户的基础信息
        res_data = model_to_dict(user_basic_message)

        # 不需要拼接详细信息则直接返回
        if not need_detail_info:
            return res_data, None

        # 拼接基础信息和用户详细信息
        detail_info = DetailInfo.objects.filter(user_id=user_id).first()
        if detail_info:
            extend_field_list = ExtendField.objects.all().values("field_index", "field")
            extend_field_map = {item["field_index"]: item["field"] for item in list(extend_field_list)}
            detail_info = model_to_dict(detail_info)
            [detail_alias_info] = filter_result_field(
                [detail_info],
                filter_filed_list=[i.name for i in DetailInfo._meta.fields if not i.name[0:6] == "field_"] + list(extend_field_map.keys()),
                alias_dict=extend_field_map,
            )
            res_data.update(detail_alias_info)

        # 返回基础和详细信息
        return res_data, None

    @staticmethod
    def user_edit(params):
        # 修改逻辑
        try:
            account = str(params.get('account', ''))
            password = str(params.get('password', ''))
            phone = str(params.get('phone', ''))
            full_name = str(params.get('full_name', ''))
            nickname = str(params.get('nickname', ''))
            user_id = params.get('user_id', '')

            # 边界检查
            if not account:
                return None, "account必填"

            # if not password:
            #     return None, "密码必填"

            # if not full_name:
            #     return None, "full_name"
            if not user_id:
                return None, " 用户id不能为空"
            # 账号类型判断
            if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
                account_type = 'phone'
            elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
                account_type = 'email'
            elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
                account_type = 'username'
            else:
                return None, "账号必须是用户名、手机或者邮箱，用户名不能是数字开头"

            # 检查账号是否存在
            user_list = None
            if account_type == 'phone':
                user_list = BaseInfo.objects.filter(Q(phone=account), ~Q(id=user_id))
            elif account_type == 'email':
                user_list = BaseInfo.objects.filter(Q(email=account), ~Q(id=user_id))
            elif account_type == 'username':
                user_list = BaseInfo.objects.filter(Q(user_name=account), ~Q(id=user_id))
            if user_list.count() and account_type == 'phone':
                return None, "手机已被注册: " + account
            elif user_list.count() and account_type == 'email':
                return None, "邮箱已被注册: " + account
            elif user_list.count() and account_type == 'username':
                return None, "用户名已被注册: " + account

            # # 检查平台是否存在
            # platform_id = None
            # platform_set = Platform.objects.filter(platform_name__iexact=platform)
            # if not platform_set.count() == 0:
            #     platform_id = platform_set.first().platform_id

            base_info = {
                'user_name': account if account_type == 'username' else '',
                'full_name': full_name,
                "nickname": nickname,
                'phone': account if account_type == 'phone' else phone,
                'email': account if account_type == 'email' else '',
            }
            BaseInfo.objects.filter(id=user_id).update(**base_info)

            return {"user_id": user_id}, None
        except SyntaxError:
            return None, "语法错误"
        except LookupError:
            return None, "无效数据查询"
        except Exception as valueError:
            return None, valueError.msg if hasattr(valueError, 'msg') else valueError.args
        except:
            return None, "未知错误"

    @staticmethod
    def user_role_edit(params):
        # 修改逻辑
        try:
            account = str(params.get('account', ''))
            phone = str(params.get('phone', ''))
            full_name = str(params.get('full_name', ''))
            nickname = str(params.get('nickname', ''))
            user_id = params.get('user_id', '')
            base_info = {}
            if not user_id:
                return None, " 用户id不能为空"
            # 边界检查
            if account:
                # 账号类型判断
                if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
                    account_type = 'phone'
                elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
                    account_type = 'email'
                elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
                    account_type = 'username'
                else:
                    return None, "账号必须是用户名、手机或者邮箱，用户名不能是数字开头"
                # 检查账号是否存在
                user_list = None
                if account_type == 'phone':
                    user_list = BaseInfo.objects.filter(Q(phone=account), ~Q(id=user_id))
                elif account_type == 'email':
                    user_list = BaseInfo.objects.filter(Q(email=account), ~Q(id=user_id))
                elif account_type == 'username':
                    user_list = BaseInfo.objects.filter(Q(user_name=account), ~Q(id=user_id))
                if user_list.count() and account_type == 'phone':
                    return None, "手机已被注册: " + account
                elif user_list.count() and account_type == 'email':
                    return None, "邮箱已被注册: " + account
                elif user_list.count() and account_type == 'username':
                    return None, "用户名已被注册: " + account

                base_info['user_name'] = account if account_type == 'username' else ''
                base_info['phone'] = account if account_type == 'phone' else phone
                base_info['email'] = account if account_type == 'email' else ''

            if full_name:
                base_info['full_name'] = full_name

            if nickname:
                base_info['nickname'] = nickname

            BaseInfo.objects.filter(id=user_id).update(**base_info)

            return {"user_id": user_id}, None
        except SyntaxError:
            return None, "语法错误"
        except LookupError:
            return None, "无效数据查询"
        except Exception as valueError:
            return None, valueError.msg if hasattr(valueError, 'msg') else valueError.args
        except:
            return None, "未知错误"

    @staticmethod
    def user_delete(id):
        if not id:
            return None, "ID 不能为空"
        try:
            BaseInfo.objects.filter(id=id).delete()
        except Exception as e:
            return None, e
        return None, None

    # 胡家萍 用户权限判断闭包
    @staticmethod
    def hjp_user_right_call(user_info):
        # map = {1: "集团用户", 2: "村民用户没有权限"}
        try:
            if user_info[0]['user_group'] == 1:
                return True
            else:
                return False
        except Exception as e:
            return False
