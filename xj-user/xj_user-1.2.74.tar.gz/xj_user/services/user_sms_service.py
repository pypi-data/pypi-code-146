# encoding: utf-8
"""
@project: djangoModel->Auth
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 小程序SDK
@created_time: 2022/7/7 9:38
"""
from datetime import datetime, timedelta
from pathlib import Path

from django.contrib.auth.hashers import make_password
import jwt
import requests

from main.settings import BASE_DIR
from xj_user.services.user_detail_info_service import DetailInfoService
from ..models import BaseInfo, Auth, UserSsoToUser
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.model_handle import parse_model
from ..utils.nickname_generate import gen_one_word_digit

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

payment_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
payment_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = payment_main_config_dict.wechat_merchant_app_id or payment_module_config_dict.wechat_merchant_app_id or ""

sub_app_secret = payment_main_config_dict.wechat_merchant_app_secret or payment_module_config_dict.wechat_merchant_app_secret or ""

app_id = main_config_dict.app_id or module_config_dict.app_id or ""
app_secret = main_config_dict.secret or module_config_dict.secret or ""
jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""


class UserSmsService:

    def get_openid(self, code):
        """
        :param code（openid登录的code）:
        :return:(err,data)
        """
        req_params = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        user_info = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session',
            params=req_params,
            timeout=3,
            verify=False
        )
        return user_info.json()

    def phone_login(self, phone, login_code, sso_serve_id=None, detail_params=None):
        if detail_params is None:
            detail_params = {}
        # 根据手机号获取用户
        current_user = BaseInfo.objects.filter(phone=phone).filter()
        current_user = parse_model(current_user)
        # 根据 小程序code换取openid
        openid = ""
        if login_code:
            wechat_openid = self.get_openid(code=login_code)
            openid = wechat_openid.get("openid", "")

        # 如果当前用户不存在则注册在登录授权
        if not current_user:
            # 进行注册用户基础信息
            base_info = {
                'user_name': '',
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': '',
                'full_name': '请修改用户名',
            }
            BaseInfo.objects.create(**base_info)
            current_user = BaseInfo.objects.filter(phone=phone).filter()
            current_user = parse_model(current_user)
            current_user = current_user[0]
            # 用户第一次登录即注册，允许添加用户的详细信息
            try:
                detail_params.setdefault("user_id", current_user.get('id', None))
                data, err = DetailInfoService.create_or_update_detail(detail_params)
            except Exception as e:
                pass

            # 进行单点登录相关操作
            if sso_serve_id:
                sso_data = {
                    "sso_serve_id": sso_serve_id,
                    "user_id": current_user.get('id', None),
                    "sso_unicode": openid,
                    "app_id": sub_appid
                }
                UserSsoToUser.objects.create(**sso_data)
            # 生成登录token
            token = self.__set_token(current_user.get('id', None), phone)
            # 创建用户登录信息，绑定token
            auth = {
                'user_id': current_user.get('id', None),
                'password': make_password('123456', None, 'pbkdf2_sha1'),
                'plaintext': '123456',
                'token': token,
            }
            Auth.objects.update_or_create({'user_id': current_user.get('id', None)}, **auth)
            auth_set = Auth.objects.filter(
                user_id=current_user.get('id', None),
                password__isnull=False
            ).order_by('-update_time').first()
            return 0, {'token': auth_set.token, 'user_info': current_user}
        else:
            # 存在当前用户，直接进行授权
            current_user = current_user[0]
            sso = UserSsoToUser.objects.filter(user_id=current_user.get('id', None), app_id=sub_appid).first()
            if not sso:
                if sso_serve_id:
                    sso_data = {
                        "sso_serve_id": sso_serve_id,
                        "user_id": current_user.get('id', None),
                        "sso_unicode": openid,
                        "app_id": sub_appid
                    }
                    UserSsoToUser.objects.create(**sso_data)
            token = self.__set_token(current_user.get('id', None), phone)
            # 创建用户登录信息，绑定token
            auth = {
                'token': token,
            }
            Auth.objects.filter(user_id=current_user.get('id', None)).update(**auth)
            auth_set = Auth.objects.filter(
                user_id=current_user.get('id', None),
                password__isnull=False
            ).order_by('-update_time').first()
            return 0, {'token': auth_set.token, 'user_info': current_user}

    def __set_token(self, user_id, account):
        # 生成过期时间
        expire_timestamp = datetime.utcnow() + timedelta(
            days=7,
            seconds=0
        )
        # 返回token
        return jwt.encode(
            payload={'user_id': user_id, 'account': account, "exp": expire_timestamp},
            key=jwt_secret_key
        )
