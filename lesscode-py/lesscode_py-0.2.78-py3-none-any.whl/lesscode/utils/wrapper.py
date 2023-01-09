import functools
import json
import uuid

import tornado.options

from lesscode.web.business_exception import BusinessException
from lesscode.web.status_code import StatusCode


class User:
    """
    用户对象类
    """

    def __init__(self):
        # '账号id',
        self.id = None
        # 用户名
        self.username = None
        # '密码',
        self.password = None
        # '显示名',
        self.display_name = None
        # 手机号,
        self.phone_no = None
        #  邮箱
        self.email = None
        # 组织机构id',
        self.org_id = None
        # '1正常（激活）；2未激活（管理员新增，首次登录需要改密码）； 3锁定（登录错误次数超限，锁定时长可配置）； 4休眠（长期未登录（字段，时长可配置），定时） 5禁用-账号失效；
        self.account_status = None
        # 角色id集合
        self.roleIds = None


def user_verification(username="admin", **kw):
    def wrapper(func):
        @functools.wraps(func)
        def run(self, *args, **kwargs):
            if tornado.options.options.running_env != "local":
                user_str = self.request.headers.get("User")
                if user_str:
                    user = json.loads(user_str)
                    if isinstance(user, dict):
                        user_username = user.get("username")
                        if username != user_username:
                            raise BusinessException(StatusCode.ACCESS_DENIED)
                    else:
                        raise BusinessException(StatusCode.ACCESS_DENIED)
                else:
                    raise BusinessException(StatusCode.ACCESS_DENIED)

            return func(self, *args, **kwargs)

        return run

    return wrapper


def login_verification(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if tornado.options.options.running_env != "local":
            user = self.request.headers.get("User")
            if not user:
                raise BusinessException(StatusCode.INVALID_TOKEN)
            else:
                user_info = json.loads(user)
                if not user_info:
                    raise BusinessException(StatusCode.INVALID_TOKEN)
        return func(self, *args, **kwargs)

    return wrapper
