# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 16:38
# @Author  : navysummer
# @Email   : navysummer@yeah.net
import datetime
import json
import logging
import traceback

import requests
from requests.auth import HTTPBasicAuth
from tornado.options import options

from lesscode.utils.json import JSONEncoder


def es_record_log(request, message="", level="info", status_code=200):
    request_headers = dict(request.headers)
    request_params = dict(request.query_arguments)
    content_type = request.headers.get('Content-Type')
    request_body = request.body
    log_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "request": {
            "id": request.headers.get("Request-Id", ""),
            "header": request_headers,
            "params": request_params,
            "url": request.path,
            "Content-Type": content_type,
            "method": request.method,
            "body": request_body,
            "real_ip": request.remote_ip
        },
        "status_code": status_code,
        "message": message
    }
    send_es(log_data)


def send_es(body):
    try:
        log_es_config = options.log_es_config if options.log_es_config else {}
        if log_es_config.get("enable"):
            url = f"{log_es_config.get('protocol', 'http')}://{log_es_config.get('host')}:" \
                  f"{log_es_config.get('port')}/{log_es_config.get('index')}/_doc/"
            res = requests.post(
                url,
                data=json.dumps(body, ensure_ascii=False, cls=JSONEncoder).encode('utf-8'),
                headers={'content-type': "application/json"},
                auth=HTTPBasicAuth(log_es_config.get("user"), log_es_config.get("password"))
            )
            if res.ok:
                logging.info(f"send es url={url} success")
            else:
                logging.info(f"send es url={url} fail")
    except Exception as e:
        logging.info(traceback.format_exc())
