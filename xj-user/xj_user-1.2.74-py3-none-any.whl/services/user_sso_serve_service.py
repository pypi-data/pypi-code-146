from django.db.models import F
from rest_framework.response import Response

from ..models import UserSsoServe, UserSsoToUser
from xj_user.utils.custom_response import util_response


class UserSsoServeService:
    @staticmethod
    def list():
        user_sso_serve_list = UserSsoServe.objects.values("id", "sso_code", "sso_name", "sso_url", "description")
        return user_sso_serve_list, None

    @staticmethod
    def add(data):
        res_set = UserSsoServe.objects.filter(sso_code=data['sso_code']).first()
        if res_set:
            return None, "登录代码已存在"
        user_sso_serve = UserSsoServe.objects.create(**data)
        if user_sso_serve:
            return {"contact_book_id": user_sso_serve.id}, None

    @staticmethod
    def user_sso_to_user(user_id, app_id):
        res_set = UserSsoToUser.objects.filter(user_id=user_id, app_id=app_id).first()
        if res_set:
            return res_set, None
        return None, "单点登录记录不存在"
