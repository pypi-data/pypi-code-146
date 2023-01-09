"""
    服务依赖sparrow_product
"""
import logging

from sparrow_cloud.restclient import rest_client
from sparrow_cloud.authorization.token import get_app_token, get_user_token


from .svc_config import SPARROW_PRODUCT_SERVICE
from .sparrow_api_path import PRODUCT_SHOP_ID_BY_USER_ID, PRODUCT_USER_IDS_BY_SHOP_ID, PRODUCT_SHOP_IDS_FOR_LOUCENG

logger = logging.getLogger(__name__)


# product服务基类
class ServiceSparrowProductBase(object):

    SERVICE_CONF = SPARROW_PRODUCT_SERVICE


class ServiceSparrowCore(ServiceSparrowProductBase):

    @classmethod
    def get_shop_id_by_guide_user_id(cls, user_id):
        '''
        根据导购的user_id，获取切换的专柜ID
        http://{{host}}/api/sparrow_admin/user/detail/
        参数
            None
        返回
            123
        '''
        api_path = PRODUCT_SHOP_ID_BY_USER_ID
        err_msg = ""
        try:
            logger.info(f"开始访问{api_path},SPARROW_PRODUCT_SERVICE_CONF={cls.SERVICE_CONF} user_id={user_id}")
            token = get_user_token(user_id)
            response = rest_client.get(cls.SERVICE_CONF, api_path=api_path, token=token)
            logger.info(f"访问结束 response={str(response)} user_id={user_id}")
            if "guide" not in response:
                return None
            guide_dict = response["guide"]
            if "shop" not in guide_dict:
                return None
            shop_dict = guide_dict["shop"]
            if "id" not in shop_dict:
                return None
            shop_id = shop_dict["id"]
            return shop_id
        except BaseException as ex:
            err_msg = f"当远程调用切换的专柜ID服务时， 远程访问异常: {str(ex)}"
            logger.error(err_msg)
            return None

    @classmethod
    def get_user_ids_by_shop_id(cls, shop_id, is_current_shop=None):
        '''
        由 shop_id 查询 该专柜所有导购的 user_id

        :params shop_id: 专柜ID
        :params is_current_shop: 导购的当前专柜是否是该专柜,  None-不筛选, 0-筛选不是当前专柜的, 1-筛选是当前专柜的
        '''
        app_token = get_app_token()
        api_path = PRODUCT_USER_IDS_BY_SHOP_ID.format(shop_id=shop_id)

        if is_current_shop is not None:
            api_path += '&is_current_shop={}'.format(int(bool(is_current_shop)))

        err_msg = ""

        user_id_list = []

        try:
            to_continue = True
            while to_continue:

                to_continue = False

                logger.info(f"开始访问{api_path},SPARROW_PRODUCT_SERVICE_CONF={cls.SERVICE_CONF} shop_id={shop_id}")

                response = rest_client.get(cls.SERVICE_CONF, api_path=api_path, token=app_token)

                logger.info(f"访问结束 response={str(response)} shop_id={shop_id}")

                if isinstance(response, dict):
                    user_infos = response.get('results', [])

                    for user_info in user_infos:
                        user_id = user_info.get("user", {}).get("id")
                        if user_id:
                            user_id_list.append(user_id)

                    to_continue = bool(response.get("next"))

        except BaseException as ex:
            err_msg = f"当远程调用切换的专柜ID服务时， 远程访问异常: {str(ex)}"
            logger.error(err_msg)

        return user_id_list

    @classmethod
    def get_shop_ids_for_louceng(cls, user_id):
        '''
        由楼层的 user_id 获取对应的所有的 shop_ids
        '''
        app_token = get_app_token()
        api_path = PRODUCT_SHOP_IDS_FOR_LOUCENG.format(user_id)

        shop_id_list = []

        try:
            to_continue = True
            while to_continue:

                to_continue = False

                logger.info(f"开始访问{api_path},SPARROW_PRODUCT_SERVICE_CONF={cls.SERVICE_CONF} louceng_user_id={user_id}")

                response = rest_client.get(cls.SERVICE_CONF, api_path=api_path, token=app_token)

                logger.info(f"访问结束 response={str(response)} louceng_user_id={user_id}")

                if isinstance(response, dict):
                    shop_infos = response.get('results', [])

                    for shop_info in shop_infos:
                        shop_id = shop_info.get("id")
                        if shop_id:
                            shop_id_list.append(shop_id)

                    to_continue = bool(response.get("next"))

        except BaseException as ex:
            err_msg = f"当远程调用切换的专柜ID服务时， 远程访问异常: {str(ex)}")
            logger.error(err_msg)

        return shop_id_list
