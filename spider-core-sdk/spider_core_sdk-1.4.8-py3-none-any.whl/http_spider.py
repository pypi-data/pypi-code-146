import json
import time
import six
import logging
from logging import handlers
from collections import Iterable

from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider
from scrapy.utils.log import TopLevelFormatter
from spider_core.serverapi import ServerApi


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


class HttpSpider(Spider):
    def __init__(self, instance_id, spider_id=None, env=None, cjzt_log=None, **kwargs):
        super(HttpSpider, self).__init__()
        self.log_handler = None
        self.log_filename = cjzt_log

        self.api = ServerApi(
            spider_id=spider_id,
            instance_id=instance_id,
        )
        self.api.init_setting(env)
        self.idle_count = 0
        self.item_list = []

        self.instance_id = instance_id
        self.spider_id = spider_id
        self.request_count = 0
        self.fetch_num = getattr(self, 'FETCH_NUM', 1)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(HttpSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(obj.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(obj.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(obj.request_scheduled, signal=signals.request_scheduled)
        return obj

    def _get_handler(self):
        """ Return a log handler object according to settings """
        if self.log_filename:
            encoding = self.settings.get('LOG_ENCODING')
            handler = handlers.RotatingFileHandler(
                filename=self.log_filename, maxBytes=2048000, backupCount=5, encoding=encoding
            )
        elif self.settings.getbool('LOG_ENABLED'):
            handler = logging.StreamHandler()
        else:
            handler = logging.NullHandler()

        formatter = logging.Formatter(
            fmt=self.settings.get('LOG_FORMAT'),
            datefmt=self.settings.get('LOG_DATEFORMAT')
        )
        handler.setFormatter(formatter)
        log_level = self.settings.get('LOG_LEVEL')
        handler.setLevel(log_level)
        if self.settings.getbool('LOG_SHORT_NAMES'):
            handler.addFilter(TopLevelFormatter(['scrapy']))
        return handler

    def start_requests(self, spider=None):
        return self.next_requests(spider)

    def item_scraped(self, item, response, spider):
        """
        当item被爬取，并通过所有 Item Pipeline 后(没有被丢弃(dropped)，发送该信号
        :param item:
        :param response:
        :param spider:
        :return:
        """
        self.crawler.stats.inc_value('cjzt/items', spider=spider)
        if item:
            self.item_list.append(time.time())
            self.idle_count = 0
            # 判断 当前触发时间与上次触发时间 之间的间隔是否大于20秒，如果大于20秒则发送心跳包
            if (self.item_list[-1] - self.item_list[0]) > 10:
                self.item_list = [self.item_list[-1]]
                self.api.send_heartbeat(status='working')

    def request_scheduled(self, request, spider):
        """
        触发请求调度调用
        :param request:
        :param spider:
        :return:
        """
        if request:
            self.idle_count = 0
            self.request_count += 1
            if self.request_count == 16:
                self.api.send_heartbeat(status='working')
                self.request_count = 0

    def fetch_data(self, spider=None):
        result = self.api.get_data(key=self.api.data_list_key, number=self.fetch_num)
        if result and result['code'] == 200:
            self.logger.debug(f'suc fetch_data: {result} instance_id: {self.instance_id}')
            data = result['data']
            if isinstance(data, str):
                return [data]
            return data
        else:
            self.logger.error(self.crawler.stats.get_stats())
            self.crawler.stats.clear_stats(spider=spider)
            # self.crawler.stats.set_value('cjzt/items', 0)
            self.api.data_list_key = ''
            self.logger.debug(f'error fetch_data: {result} instance_id: {self.instance_id}')
        return []

    def next_requests(self, spider=None):
        """Returns a request to be scheduled or none."""
        found = 0
        datas = self.fetch_data(spider)
        self.logger.debug(f'next_requests: datas {datas}')
        for data in datas:
            data = json.loads(data)
            self.api.set_args({'batch': data.get('batch', '')})
            reqs = self.make_request_from_data(data)
            if isinstance(reqs, Iterable):
                for req in reqs:
                    req.depth = found
                    yield req
                    # XXX: should be here?
                    req.depth += 1
                    found += 1
                    self.logger.info(f'start req url:{req.url}')
            elif reqs:
                reqs.depth = found
                yield reqs
                reqs.depth += 1
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

    def make_request_from_data(self, data):
        url = bytes_to_str(data)
        return self.make_requests_from_url(url)

    def schedule_next_requests(self, spider=None):
        """Schedules a request if available"""
        # TODO: While there is capacity, schedule a batch of requests.
        for req in self.next_requests(spider):
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self, spider):
        """Schedules a request if available, otherwise waits."""
        if self.log_handler is None and self.log_filename:
            self.log_handler = self._get_handler()
            logging.root.addHandler(self.log_handler)

        if self.api.data_list_key:
            self.schedule_next_requests(spider)
            raise DontCloseSpider
        task_status = self.api.task_query()
        self.logger.debug(f'fetch task: {task_status}')
        """向爬虫中台获取任务"""
        if task_status['code'] == 200:
            self.logger.debug(f'fetch task:{self.instance_id}, {task_status}')

            self.api.send_heartbeat(status='working')
            task_data = task_status['data']
            self.api.set_args(task_data)
            self.idle_count = 0

        """闲置状态 触发5次 发送心跳接口"""
        if self.idle_count == 5:
            self.api.send_heartbeat(status='waiting')
            self.logger.debug('send_heartbeat --- waiting')
            self.idle_count = 0
        self.idle_count += 1
        raise DontCloseSpider


def send_data_status(func):
    def inner(obj, response, *args, **kwargs):
        data = response.meta
        if obj.api.data_type == 'point':
            data_value = f"{data['lat']},{data['lng']}"
        else:
            data_value = f"{data['shop_id']}"

        try:
            res = func(obj, response, *args, **kwargs)
            obj.api.task_callback(data_value)
            return res
        except Exception as e:
            obj.logger.error(f'send_data_status error: {e}')
            obj.api.task_callback(data_value, False)
    return inner
