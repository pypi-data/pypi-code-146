import logging
import time
import requests
from .config import host_config, date_type_map
from .utils import sign_headers


class ServerApi:
    def __init__(self, instance_id, spider_id):
        self.host = ''
        self.port = ''
        self.cjzt_url = ''

        self.ak = ''
        self.secret = ''
        self.instance_id = instance_id
        self.spider_id = spider_id
        self.store_url = ''

        self.data_type = ''
        self.task_id = ''
        self.old_task_id = ''
        self.task_type = ''
        self.data_list_key = ''
        self.date_no = ''
        self.platform = ''
        self.rep_times = ''
        self.sub_task_id = ''
        self.create_time = ''
        self.batch = ''

        self.TIMEOUT = (10, 20)

    def init_setting(self, env):
        hosts = host_config.get(env)
        if hosts is None:
            raise RuntimeError('未指定SDK运行环境')
        self.host = hosts['host']
        self.port = hosts['port']
        self.cjzt_url = f'{self.host}:{self.port}'
        self.store_url = hosts['store_url']

    def set_args(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    def send_heartbeat(self, status):
        """
        发送心跳
        :param status: waiting or working
        :return:
        """
        while 1:
            data = {
                "spider_id": self.spider_id,
                "instance_id": self.instance_id,
                'status': status
            }
            method = 'POST'
            url = f'http://{self.cjzt_url}/client/instance/heartbeat'
            try:
                r = requests.request(method, url, json=data, timeout=self.TIMEOUT)
                if r.status_code == 200:
                    return
                else:
                    logging.error(f'【/client/instance/heartbeat】服务器异常，状态码: {r.text}')
            except OSError as e:
                logging.error(f'【/client/instance/heartbeat 】客户端异常: {e}')
            time.sleep(5)

    def get_data(self, key, number=1):
        """
        获取数据
        :param key: redis key
        :param number: 获取条数

        获取一条返回为json
        返回多条返回为List[json]
        :return:
        """
        if key:
            while 1:
                try:
                    url = f'http://{self.cjzt_url}/client/data?key={key}&number={number}&subtask_id={self.sub_task_id}'
                    method = 'GET'
                    r = requests.request(method, url, timeout=10)
                    if r.status_code == 200:
                        return r.json()
                    else:
                        logging.error(f'【client/data】服务器异常,状态码：{r.json()}')
                except Exception as e:
                    logging.error(f'【client/data】客户端异常：{e}')
                time.sleep(5)
        return {}

    def task_query(self):
        while 1:
            method = 'GET'
            params = {
                'spider_id': self.spider_id,
                'instance_id': self.instance_id,
            }
            url = f'http://{self.cjzt_url}/client/task'
            try:
                r = requests.request(method, url, params=params, timeout=self.TIMEOUT)
                if r.status_code == 200:
                    return r.json()
                else:
                    logging.error(f'【/client/task】服务器异常,状态码：{r.status_code}')
            except OSError as e:
                logging.error(f'【/client/task】客户端异常：{e}')
            time.sleep(5)

    def task_callback(self, value, is_success=True):
        """
        任务确认
        :param value: 采集数据源
        :param is_success: 数据采集是否正常
        :return:
        """
        while 1:
            url = f'http://{self.cjzt_url}/client/task'
            data = {
                "spider_id": self.spider_id,
                "instance_id": self.instance_id,
                "task_id": self.task_id,
                "data_type": self.data_type,
                "data_value": value,
                "data_key": self.data_list_key,
                "is_success": is_success,
            }
            method = 'POST'
            try:
                r = requests.request(method, url, json=data, timeout=self.TIMEOUT)
                if r.status_code == 200:
                    logging.debug(f'【/client/task/callback】 code is 200 {r.text} instance_id: {self.instance_id}')
                    return
                else:
                    logging.error(f'【/client/task/callback】服务器异常,状态码：{r.text}')
            except OSError as e:
                logging.error(f'【/client/task/callback】客户端异常：{e}')
            time.sleep(5)

    def report_stats(self, stats):
        """
        上报统计数据
        """
        while 1:
            data = {
                'instance_id': self.instance_id,
                'spider_id': self.spider_id,
                'task_id': self.task_id,
                'stats': stats
            }
            url = f'http://{self.cjzt_url}/client/task/stats'
            method = 'POST'
            try:
                r = requests.request(method, url, json=data, timeout=self.TIMEOUT)
                if r.status_code == 200:
                    logging.debug(f'【/client/task/stats】 code is 200 {r.text}')
                    return
                else:
                    logging.error(f'【/client/task/stats】服务器异常,状态码：{r.text}')
            except OSError as e:
                logging.error(f'【/client/task/stats】客户端异常：{e}')
            time.sleep(5)

    def data_clean_nginx_store_api(self, item, data_type, ext_header=None):
        if isinstance(item, list):
            for i in item:
                for k, v in i.items():
                    if isinstance(v, str):
                        i[k] = v.replace('\n', '').replace('\r', '')
        else:
            for k, v in item.items():
                if isinstance(v, str):
                    item[k] = v.replace('\n', '').replace('\r', '')
        return self.nginx_store_api(item, data_type, ext_header)

    def nginx_store_api(self, item, data_type, ext_header=None):
        """
        data_type : 数据类型(店铺，商品，券等)
        """
        headers = {'Content-Type': 'application/json'}
        header = {
            "client_id": self.spider_id,
            "task_id": self.old_task_id if self.old_task_id else self.task_id,
            "plf_id": self.platform,
            "cycle_type": date_type_map.get(self.task_type, ''),
            "data_type": data_type,
            "date_no": self.date_no,
            "is_new": 1 if isinstance(item, list) else 0,
            "rep_times": self.rep_times,
            'instance_id': self.instance_id
        }
        if ext_header:
            header.update(ext_header)
        if self.batch:
            start_time = time.strptime(self.create_time, '%Y-%m-%d %H:%M:%S.%f') if self.create_time else ''
            time_apm = ('AM' if start_time.tm_hour < 14 else 'PM') if start_time else ''
            header.update({'start_time': time_apm, 'batch': self.batch})
        data = {
            "header": header,
            "data": item
        }

        while 1:
            try:
                r = requests.request(
                    method='POST', url=self.store_url,
                    headers=headers, json=data, timeout=self.TIMEOUT
                )
                if 200 <= r.status_code < 300:
                    logging.debug(f'【crawler/collect/logs】 code is 200 {r.text} task_id: {self.task_id}')
                    return
                else:
                    logging.error(f'【crawler/collect/logs】服务器异常：{r.text} task_id: {self.task_id}')
            except OSError as e:
                logging.error(f'【crawler/collect/logs】 客户端异常 : {e} task_id: {self.task_id}')

    def insert_into(self, table, data):
        method = 'POST'
        timestamp = str(int(time.time() * 1000))
        url = f'http://{self.cjzt_url}/client/data/alter/{table}'
        headers = sign_headers('POST', {}, data, self.ak, self.secret, timestamp)
        while 1:
            try:
                r = requests.request(
                    method=method, url=url,
                    headers=headers, json=data, timeout=self.TIMEOUT
                )
                if 200 <= r.status_code < 300:
                    logging.debug(f'【insert_into】 code is 200 {r.text}')
                    return
                else:
                    logging.error(f'【insert_into】服务器异常：{r.text}')
            except OSError as e:
                logging.error(f'【insert_into】 客户端异常 : {e}')

    def get_cache(self, key):
        """
        spider_id: str,
        instance_id: str,
        key: str,
        """
        url = f'http://{self.cjzt_url}/client/data/cache'
        method = 'GET'
        params = {
            "key": key,
            "spider_id": self.spider_id,
            "instance_id": self.instance_id
        }
        while 1:
            try:
                r = requests.request(
                    method=method, url=url,
                    params=params, timeout=self.TIMEOUT
                )
                if 200 <= r.status_code < 300:
                    logging.debug(f'【get_cache】 code is 200 {r.text}')
                    return r.json().get('data')
                else:
                    logging.error(f'【get_cache】服务器异常：{r.text}')
            except OSError as e:
                logging.error(f'【get_cache】 客户端异常 : {e}')

    def set_cache(self, key: str, value: str):
        """
        spider_id: str,
        instance_id: str,
        key: str,
        value: str
        """
        url = f'http://{self.cjzt_url}/client/data/cache'
        method = 'POST'
        params = {
            "key": key,
            "value": value,
            "spider_id": self.spider_id,
            "instance_id": self.instance_id
        }
        while 1:
            try:
                r = requests.request(
                    method=method, url=url,
                    json=params, timeout=self.TIMEOUT
                )
                if 200 <= r.status_code < 300:
                    logging.debug(f'【set_cache】 code is 200 {r.text}')
                    return
                else:
                    logging.error(f'【set_cache】服务器异常：{r.text}')
            except OSError as e:
                logging.error(f'【set_cache】 客户端异常 : {e}')

    def del_cache(self, key):
        """
        spider_id: str,
        instance_id: str,
        key: str,
        """
        url = f'http://{self.cjzt_url}/client/data/cache'
        method = 'DELETE'
        params = {
            "key": key,
            "spider_id": self.spider_id,
            "instance_id": self.instance_id
        }
        while 1:
            try:
                r = requests.request(
                    method=method, url=url,
                    params=params, timeout=self.TIMEOUT
                )
                if 200 <= r.status_code < 300:
                    logging.debug(f'【get_cache】 code is 200 {r.text}')
                    return r.json().get('data')
                else:
                    logging.error(f'【get_cache】服务器异常：{r.text}')
            except OSError as e:
                logging.error(f'【get_cache】 客户端异常 : {e}')

    def send_stats(self, stats):
        pass
