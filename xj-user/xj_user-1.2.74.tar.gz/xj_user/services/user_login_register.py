from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
import jwt
import requests
from pathlib import Path
from main.settings import BASE_DIR
from ..models import BaseInfo, Auth
from ..utils.model_handle import parse_model
from ..services.wechat_service import WechatService
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

redis_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))
redis_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))

redis_host = redis_main_config_dict.redis_host or redis_module_config_dict.redis_host or ""
redis_port = redis_main_config_dict.redis_port or redis_module_config_dict.redis_port or ""
redis_password = redis_main_config_dict.redis_password or redis_module_config_dict.redis_password or ""


class LoginRegister:
    @staticmethod
    def login_register(phone, code):
        wechat_openid = LoginRegister.get_openid(code=code)
        current_user = BaseInfo.objects.filter(phone=phone).filter()
        current_user = parse_model(current_user)
        if not current_user:
            base_info = {
                'user_name': '',
                'nickname': phone,
                'phone': phone,
                'email': '',
                'full_name': '请修改用户名',
                'wechat_openid': wechat_openid['openid']
            }
            BaseInfo.objects.create(**base_info)
            current_user = BaseInfo.objects.filter(phone=phone).filter()
            current_user = parse_model(current_user)
            current_user = current_user[0]
            # 生成登录token
            token = LoginRegister.set_token(current_user.get('id', None), phone)

            # 创建用户登录信息，绑定token
            auth = {
                'user_id': current_user.get('id', None),
                'password': make_password('123456', None, 'pbkdf2_sha1'),
                'plaintext': '123456',
                'token': token,
            }
            Auth.objects.update_or_create({'user_id': current_user.get('id', None)}, **auth)
            auth_set = Auth.objects.filter(user_id=current_user.get('id', None), password__isnull=False).order_by(
                '-update_time').first()
            return 0, {'token': auth_set.token, 'user_info': current_user}
        current_user = current_user[0]
        auth_set = Auth.objects.filter(user_id=current_user.get('id', None), password__isnull=False).order_by(
            '-update_time').first()
        return 0, {'token': auth_set.token, 'user_info': current_user}

    @staticmethod
    def set_token(user_id, account):
        # 生成过期时间
        expire_timestamp = datetime.utcnow() + timedelta(
            days=int(expire_day),
            seconds=int(expire_second)
        )
        # 返回token
        return jwt.encode(
            payload={'user_id': user_id, 'account': account, "exp": expire_timestamp},
            key=jwt_secret_key
        )

    @staticmethod
    def get_openid(code):
        """
        :param code（openid登录的code）:
        :return:(err,data)
        """
        req_params = {
            'appid': app_id,
            'secret': app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        user_info = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=req_params, timeout=3,
                                 verify=False)
        return user_info.json()
