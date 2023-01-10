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
import redis
import requests

from main.settings import BASE_DIR
from .user_detail_info_service import DetailInfoService
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

redis_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))
redis_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))

redis_host = redis_main_config_dict.redis_host or redis_module_config_dict.redis_host or ""
redis_port = redis_main_config_dict.redis_port or redis_module_config_dict.redis_port or ""
redis_password = redis_main_config_dict.redis_password or redis_module_config_dict.redis_password or ""


# print(">", sub_appid)


class WechatService:
    wx_login_url = "https://api.weixin.qq.com/sns/jscode2session"
    wx_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    wx_get_phone_url = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"

    def __init__(self):
        self.login_param = {'appid': app_id, 'secret': app_secret, 'grant_type': 'authorization_code'}
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password
        )

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
        user_info = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=req_params, timeout=3,
                                 verify=False)
        return user_info.json()
        # try:
        #     response = requests.get(self.wx_login_url, code).json()
        #     if not response['errcode'] == 0:  # openid 换取失败
        #         return response['errcode'], response['errmsg']
        # except Exception as e:
        #     return 6445, '请求错误'

    def wechat_login(self, phone_code, login_code, sso_serve_id=None, detail_params=None):
        """
        过期续约就是重新登录
        :param detail_params:
        :param code: 换取手机号码的code
        :return:(err,data)
        """
        # code 换取手机号
        if detail_params is None:
            detail_params = {}
        url = self.wx_get_phone_url + "?access_token={}".format(self.get_access_token()['access_token'])
        header = {'content-type': 'application/json'}
        response = requests.post(url, json={'code': phone_code}, headers=header).json()
        if not response['errcode'] == 0:
            return response['errmsg'], ""
        phone = response['phone_info']['phoneNumber']
        # 检查是否存在该用户，不存在直接注册
        # current_user = BaseInfo.objects.filter(phone=phone).filter()
        # current_user = parse_model(current_user)
        # if not current_user:
        #     base_info = {
        #         'user_name': '',
        #         'phone': phone,
        #         'email': '',
        #         'full_name': '请修改用户名',
        #     }
        #     current_user = BaseInfo.objects.create(**base_info)
        #     current_user = parse_model(current_user)
        # current_user = current_user[0]
        # # 生成登录token
        # token = self.__set_token(current_user.get('id', None), phone)
        # # 创建用户登录信息，绑定token
        # auth = {
        #     'user_id': current_user.get('id', None),
        #     'password': make_password('123456', None, 'pbkdf2_sha1'),
        #     'plaintext': '123456',
        #     'token': token,
        # }
        # Auth.objects.update_or_create({'user_id': current_user.get('id', None)}, **auth)
        # return 0, {'token': token, 'user_info': current_user}

        # 通过换取的手机号判断用户是否存在
        current_user = BaseInfo.objects.filter(phone=phone).filter()
        current_user = parse_model(current_user)
        if not login_code:
            return None, "微信登录 login_code 必传"
        wechat_openid = self.get_openid(code=login_code)
        if wechat_openid.get("openid", None) is None:
            return None, "获取 openid 失败 查openid是否过期"
        # 登录即注册操作
        if not current_user:
            # 用户不存在的时候，进行注册用户
            base_info = {
                'user_name': '',
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': '',
                'full_name': '请修改用户名',
                # 'wechat_openid': wechat_openid['openid']
            }
            BaseInfo.objects.create(**base_info)
            current_user = BaseInfo.objects.filter(phone=phone).filter()
            current_user = parse_model(current_user)
            current_user = current_user[0]
            # 生成登录token
            token = self.__set_token(current_user.get('id', None), phone)
            # 用户第一次登录即注册，允许添加用户的详细信息
            try:
                detail_params.setdefault("user_id", current_user.get('id', None))
                data, err = DetailInfoService.create_or_update_detail(detail_params)
            except Exception as e:
                pass

            # 创建单点登录
            if sso_serve_id:
                sso_data = {
                    "sso_serve_id": sso_serve_id,
                    "user_id": current_user.get('id', None),
                    "sso_unicode": wechat_openid['openid'],
                    "app_id": sub_appid
                }
                UserSsoToUser.objects.create(**sso_data)
            # 创建用户登录信息，绑定token
            auth = {
                'user_id': current_user.get('id', None),
                'password': make_password('123456', None, 'pbkdf2_sha1'),
                'plaintext': '123456',
                'token': token,
            }
            Auth.objects.update_or_create({'user_id': current_user.get('id', None)}, **auth)
            auth_set = Auth.objects.filter(user_id=current_user.get('id', None), password__isnull=False).order_by('-update_time').first()

            return 0, {'token': auth_set.token, 'user_info': current_user}
        else:
            # 用户存在的时候
            current_user = current_user[0]
            sso = UserSsoToUser.objects.filter(user_id=current_user.get('id', None), app_id=sub_appid).first()
            if not sso:
                if sso_serve_id:
                    sso_data = {
                        "sso_serve_id": sso_serve_id,
                        "user_id": current_user.get('id', None),
                        "sso_unicode": wechat_openid['openid'],
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

    def get_access_token(self):
        # access_token = self.redis.get('access_token')
        # if access_token:
        #     ttl = self.redis.ttl('access_token')
        #     return {"access_token": access_token.decode('utf-8'), 'expires_in': ttl, 'local': True}
        param = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'grant_type': 'client_credential'
        }
        response = requests.get(self.wx_token_url, param).json()
        # if 'access_token' in response.keys():
        #     self.redis.set('access_token', response['access_token'])
        #     self.redis.expire('access_token', response['expires_in'])
        return response

    def __del__(self):
        self.redis.close()
