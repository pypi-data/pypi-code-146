import os

from elasticsearch import Elasticsearch

from sparrow_order_lib.es.es_util import logger
from sparrow_order_lib.es.es_util.exceptions import ESUtilESClusterException


def init_es():
    ''' 连接ES集群并返回

    如果 集群不可达或不可用, 则抛出异常
    '''
    try:

        hosts = os.environ.get('ES_HOST')

        assert hosts is not None, "未设置ES_HOST"

        port = os.environ.get('ES_PORT')

        assert port is not None, "未设置ES_PORT"

        login = os.environ.get('ES_USER')

        assert login is not None, "未设置ES_USER"

        passwd = os.environ.get('ES_PASSWD')

        assert passwd is not None, "未设置ES_PASSWD"

        es = Elasticsearch(
            hosts=[hosts],
            port=port,
            http_auth=(login, passwd)
        )

        health_status = es.cluster.health().get('status')
        assert health_status != 'red', f"health_status={health_status}"
    except BaseException as err:
        logger.error(err, exc_info=True)
        raise ESUtilESClusterException(err.__str__())
    return es
