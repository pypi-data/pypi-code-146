import logging
import time
from queue import Queue
from threading import Thread
import urllib3
from elasticsearch import Elasticsearch
from ._conf import ElasticSearchConf
from advancedLogger.contract import IIndexFormatter

logger = logging.getLogger(__name__)


class ElasticSearchLogger(Thread):
    def __init__(self, index_formatter: IIndexFormatter, config: ElasticSearchConf, queue: Queue):
        super().__init__()

        self.__queue = queue
        self.__config: ElasticSearchConf = config
        self.__indexFormatter: IIndexFormatter = index_formatter

        self.__es = Elasticsearch(hosts=self.__config.hosts,
                                  http_auth=(self.__config.user, self.__config.password),
                                  sniff_on_start=self.__config.sniffOnStart,
                                  sniff_on_connection_fail=self.__config.sniffOnConnectionFail,
                                  sniffer_timeout=self.__config.snifferTimeout,
                                  sniff_timeout=self.__config.sniffTimeout)

    def run(self):

        while True:

            try:
                if not self.__queue.empty():
                    body = self.__queue.get()
                    self.__es.index(index=self.__indexFormatter.getIndex(), document=body)

            except urllib3.exceptions.ConnectTimeoutError:
                logger.error('Elastic Search Connection Error')

            except Exception as e:
                logger.exception(e)

            time.sleep(0.01)
