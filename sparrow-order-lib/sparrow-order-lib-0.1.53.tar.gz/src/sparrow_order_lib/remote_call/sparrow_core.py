"""
    服务依赖sparrow_core
"""

from django.conf import settings

from .sparrow_api_path import CORE_USER_INFO_BY_ID_API_PATH


from sparrow_cloud.restclient import rest_client

import logging
logger = logging.getLogger(__name__)


# core服务基类
class ServiceSparrowCoreBase(object):

    SERVICE_CONF = settings.SPARROW_CORE_CONF


class ServiceSparrowCore(ServiceSparrowCoreBase):

    @classmethod
    def get_user_info(cls, user_id):
        """
            根据用户ID查询用户信息
        """
        try:
            api = CORE_USER_INFO_BY_ID_API_PATH.format(user_id)
            resp = rest_client.get(cls.SERVICE_CONF, api)
            return resp
        except Exception as e:
            logger.error("get user info user_id = {} error {}".format(user_id, e))
            return None
