"""
    服务依赖sparrow_core_go
"""

from django.conf import settings

from sparrow_cloud.authorization.token import get_app_token, get_user_token

from .svc_config import SPARROW_CORE_GO_SERVICE
from .sparrow_api_path import CORE_GO_MEMBER_INFO_API_PATH
from .sparrow_api_path import CORE_GO_I_USER_INFO


from sparrow_cloud.restclient import rest_client

import logging
logger = logging.getLogger(__name__)


# core服务基类
class ServiceSparrowCoreGoBase(object):

    SERVICE_CONF = SPARROW_CORE_GO_SERVICE


class ServiceSparrowCoreGo(ServiceSparrowCoreGoBase):

    @classmethod
    def get_user_info_dict(cls, user_id):
        '''
        功能：根据user_id，获取会员信息
        参数：user_id
        返回：
            {
                "customer_user_id":customer_user_id,
                "customer_displayname":customer_name,
                "customer_username":customer_username,
                "customer_member_xx_level":customer_member_xx_level,
                "customer_member_number":customer_member_number,
                "user_id": customer_user_id,
                "username": customer_username,
                "user_displayname": customer_name + customer_username
            }

        '''
        if not user_id:
            return {}
        api_path = CORE_GO_MEMBER_INFO_API_PATH
        err_msg = ""
        try:
            token = get_user_token(user_id=user_id)
            logger.info(f"开始访问{api_path},参数分别为：SPARROW_CORE_GO_SERVICE={cls.SERVICE_CONF} user_id={user_id}")
            response = rest_client.get(SPARROW_CORE_GO_SERVICE, api_path=api_path, token=token)
            logger.info(f"访问结束：user_id={user_id} response={str(response)}")
            customer_displayname = ""
            customer_username = ""
            customer_member_xx_level = ""
            customer_member_number = ""
            if "name" in response:
                customer_displayname = response["name"]
            if "username" in response:
                customer_username = response["username"]
            if "level" in response:
                level_dict = response["level"]
                if "level" in level_dict:
                    customer_member_xx_level = level_dict["level"]
                if "number" in level_dict:
                    customer_member_number = level_dict["number"]

            customer_info_dict = {
                "customer_user_id": user_id,
                "customer_displayname": customer_displayname,
                "customer_username": customer_username,
                "customer_member_xx_level": customer_member_xx_level,
                "customer_member_number": customer_member_number
            }

            return customer_info_dict
        except BaseException as ex:
            err_msg = f"当远程调用{api_path}服务时，user_id={user_id}, 远程访问异常: {str(ex)}"
            logger.error(err_msg)
            return {}

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
        api_path = CORE_GO_I_USER_INFO.format(user_id)
        err_msg = ""
        try:
            logger.info(f"开始访问{api_path},参数分别为：SPARROW_CORE_GO_SERVICE={cls.SERVICE_CONF} user_id={user_id}")

            token = get_app_token()
            response = rest_client.get(SPARROW_CORE_GO_SERVICE, api_path=api_path, token=token)
            logger.info(f"访问结束：user_id={user_id} response={str(response)}")

            res_dict = response.get("data", {})

            customer_displayname = ""
            customer_username = ""

            customer_displayname = res_dict.get("name", customer_displayname)
            customer_username = res_dict.get("username", customer_username)

            if customer_displayname:
                user_displayname = customer_displayname + " " + customer_username
            else:
                user_displayname = customer_username

            customer_info_dict = {
                "customer_user_id": user_id,
                "customer_displayname": customer_displayname[:15],  # 用户昵称太长的话会引起数据错误, 所有表都是最长 15 个字符
                "customer_username": customer_username,
                "user_id": user_id,
                "username": customer_username,
                "user_displayname": user_displayname[:15],  # 用户昵称太长的话会引起数据错误, 所有表都是最长 15 个字符
            }

            return customer_info_dict
        except BaseException as ex:
            err_msg = f"当远程调用{api_path}服务时，user_id={user_id}, 远程访问异常: {str(ex)}"
            logger.error(err_msg)
            return {}
