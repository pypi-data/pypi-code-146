"""
    服务依赖sparrow_lanyue
"""

from django.conf import settings

from sparrow_cloud.authorization.token import get_app_token, get_user_token

from .svc_config import SPARROW_LANYUE_SERVICE
from .sparrow_api_path import LANYUE_I_USER_INFO


from sparrow_cloud.restclient import rest_client

import logging
logger = logging.getLogger(__name__)


# core服务基类
class ServiceSparrowLanyueBase(object):

    SERVICE_CONF = SPARROW_LANYUE_SERVICE


class ServiceSparrowLanyue(ServiceSparrowLanyueBase):

    @classmethod
    def get_user_info_dict_all(cls, user_id):
        """
            由 user_id 获得 username  displayname
            只要数据库有, 一定会拿到, 不会屏蔽会员卡异常的情况

            {
                "customer_user_id": "c50a77b2dacc412bb9dbbe138453ff7c",
                "customer_displayname": "jxxxx",
                "customer_username": "1820xxxx05",
                "user_id": "c50a77b2dacc412bxxxxxx",
                "username": "182xxxxxx05",
                "user_displayname": "jxxxx 182xxxxxx05"
            }

        """
        if not user_id:
            return {}
        api_path = LANYUE_I_USER_INFO
        err_msg = ""
        try:
            logger.info(f"开始访问{api_path},参数分别为：SERVICE={cls.SERVICE_CONF} user_id={user_id}")

            token = get_app_token()
            payload = {"user_id_list": [user_id]}
            response = rest_client.post(cls.SERVICE_CONF, api_path=api_path, json=payload, token=token)
            logger.info(f"访问结束：user_id={user_id} response={str(response)}")

            res_dict = response.get("data", {})
            user_info = res_dict.get(user_id, {})

            name = ""
            phone = ""

            name = user_info.get("name", name)
            phone = user_info.get("phone", phone)

            if name:
                user_displayname = name + " " + phone
            else:
                user_displayname = phone

            customer_info_dict = {
                "customer_user_id": user_id,
                "customer_displayname": name[:15],  # 用户昵称太长的话会引起数据错误, 所有表都是最长 15 个字符
                "customer_username": phone,
                "user_id": user_id,
                "username": phone,
                "phone": phone,
                "name": name[:15],
                "user_displayname": user_displayname[:15],  # 用户昵称太长的话会引起数据错误, 所有表都是最长 15 个字符
            }

            return customer_info_dict
        except BaseException as ex:
            err_msg = f"当远程调用{api_path}服务时，user_id={user_id}, 远程访问异常: {str(ex)}"
            logger.error(err_msg)
            return {}
